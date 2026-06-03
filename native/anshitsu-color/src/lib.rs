use std::cmp::max;
use std::slice;

#[derive(Clone, Copy)]
struct Sample {
    x: usize,
    y: usize,
    rgb: [f32; 3],
}

/// Apply Automatic Color Equalization to an interleaved RGB u8 buffer.
///
/// The implementation follows the Retinex-like ACE shape used by
/// Rizzi, Gatta, and Marini: each pixel is compared with a deterministic
/// set of image samples, contrast contribution is slope-limited, distance
/// weighted, then stretched per channel to the display range.
pub fn automatic_color_equalization_rgb(
    data: &mut [u8],
    width: usize,
    height: usize,
    sample_limit: usize,
    slope: f32,
    limit: f32,
) -> Result<(), &'static str> {
    let pixels = width
        .checked_mul(height)
        .ok_or("image dimensions overflow")?;
    if pixels == 0 {
        return Ok(());
    }
    if data.len() != pixels.checked_mul(3).ok_or("image buffer overflow")? {
        return Err("buffer length does not match RGB image dimensions");
    }

    let samples = collect_samples(data, width, height, sample_limit);
    if samples.is_empty() {
        return Ok(());
    }

    let mut response = vec![0.0_f32; data.len()];
    let mut min_values = [f32::INFINITY; 3];
    let mut max_values = [f32::NEG_INFINITY; 3];
    let slope = if slope.is_finite() {
        slope.max(0.0)
    } else {
        10.0
    };
    let limit = if limit.is_finite() {
        limit.max(0.0)
    } else {
        1000.0
    };

    for y in 0..height {
        for x in 0..width {
            let pixel_index = (y * width + x) * 3;
            for channel in 0..3 {
                let value = data[pixel_index + channel] as f32;
                let mut total = 0.0_f32;
                let mut weight_total = 0.0_f32;

                for sample in &samples {
                    let distance = distance_weight(x, y, sample.x, sample.y);
                    let delta = (value - sample.rgb[channel]) * slope;
                    total += delta.clamp(-limit, limit) / distance;
                    weight_total += 1.0 / distance;
                }

                let adjusted = if weight_total > 0.0 {
                    total / weight_total
                } else {
                    value
                };
                response[pixel_index + channel] = adjusted;
                min_values[channel] = min_values[channel].min(adjusted);
                max_values[channel] = max_values[channel].max(adjusted);
            }
        }
    }

    for y in 0..height {
        for x in 0..width {
            let pixel_index = (y * width + x) * 3;
            for channel in 0..3 {
                let range = max_values[channel] - min_values[channel];
                if range <= f32::EPSILON {
                    continue;
                }
                let normalized =
                    (response[pixel_index + channel] - min_values[channel]) * 255.0 / range;
                data[pixel_index + channel] = normalized.round().clamp(0.0, 255.0) as u8;
            }
        }
    }

    Ok(())
}

/// Apply gray-world white balance followed by per-channel color stretching.
pub fn color_stretch_rgb(data: &mut [u8], width: usize, height: usize) -> Result<(), &'static str> {
    let pixels = width
        .checked_mul(height)
        .ok_or("image dimensions overflow")?;
    if pixels == 0 {
        return Ok(());
    }
    if data.len() != pixels.checked_mul(3).ok_or("image buffer overflow")? {
        return Err("buffer length does not match RGB image dimensions");
    }

    apply_grey_world(data, pixels);
    apply_stretch(data);
    Ok(())
}

fn apply_grey_world(data: &mut [u8], pixels: usize) {
    let mut sums = [0_u64; 3];
    for pixel in data.chunks_exact(3) {
        sums[0] += pixel[0] as u64;
        sums[1] += pixel[1] as u64;
        sums[2] += pixel[2] as u64;
    }

    let green_average = sums[1] as f32 / pixels as f32;
    let red_average = sums[0] as f32 / pixels as f32;
    let blue_average = sums[2] as f32 / pixels as f32;
    let red_scale = channel_scale(green_average, red_average);
    let blue_scale = channel_scale(green_average, blue_average);

    for pixel in data.chunks_exact_mut(3) {
        pixel[0] = ((pixel[0] as f32) * red_scale).min(255.0) as u8;
        pixel[2] = ((pixel[2] as f32) * blue_scale).min(255.0) as u8;
    }
}

fn channel_scale(target_average: f32, channel_average: f32) -> f32 {
    if channel_average <= f32::EPSILON {
        1.0
    } else {
        target_average / channel_average
    }
}

fn apply_stretch(data: &mut [u8]) {
    let mut min_values = [u8::MAX; 3];
    let mut max_values = [0_u8; 3];

    for pixel in data.chunks_exact(3) {
        for channel in 0..3 {
            min_values[channel] = min_values[channel].min(pixel[channel]);
        }
    }

    for pixel in data.chunks_exact_mut(3) {
        for channel in 0..3 {
            pixel[channel] = pixel[channel].saturating_sub(min_values[channel]);
            max_values[channel] = max_values[channel].max(pixel[channel]);
        }
    }

    for pixel in data.chunks_exact_mut(3) {
        for channel in 0..3 {
            let channel_max = max_values[channel];
            if channel_max == 0 {
                continue;
            }
            let stretched = (pixel[channel] as f32) * (256.0 / channel_max as f32);
            pixel[channel] = stretched.min(255.0) as u8;
        }
    }
}

fn collect_samples(data: &[u8], width: usize, height: usize, sample_limit: usize) -> Vec<Sample> {
    let pixels = width * height;
    let sample_limit = sample_limit.clamp(1, pixels);
    if sample_limit == pixels {
        return (0..height)
            .flat_map(|y| (0..width).map(move |x| sample_at(data, width, x, y)))
            .collect();
    }

    let aspect = width as f32 / height as f32;
    let columns = max(
        1,
        ((sample_limit as f32 * aspect).sqrt().round() as usize).min(width),
    );
    let rows = max(
        1,
        ((sample_limit as f32 / columns as f32).ceil() as usize).min(height),
    );
    let mut samples = Vec::with_capacity(columns * rows);

    for row in 0..rows {
        let y = if rows == 1 {
            height / 2
        } else {
            (row * (height - 1) + (rows - 1) / 2) / (rows - 1)
        };
        for column in 0..columns {
            let x = if columns == 1 {
                width / 2
            } else {
                (column * (width - 1) + (columns - 1) / 2) / (columns - 1)
            };
            samples.push(sample_at(data, width, x, y));
        }
    }

    samples
}

fn sample_at(data: &[u8], width: usize, x: usize, y: usize) -> Sample {
    let index = (y * width + x) * 3;
    Sample {
        x,
        y,
        rgb: [
            data[index] as f32,
            data[index + 1] as f32,
            data[index + 2] as f32,
        ],
    }
}

fn distance_weight(x: usize, y: usize, sample_x: usize, sample_y: usize) -> f32 {
    let dx = x.abs_diff(sample_x) as f32;
    let dy = y.abs_diff(sample_y) as f32;
    (dx.mul_add(dx, dy * dy)).sqrt().max(1.0)
}

/// C ABI entry point for Python ctypes callers.
///
/// Returns 0 on success and a negative value for invalid input.
#[no_mangle]
pub unsafe extern "C" fn anshitsu_ace_rgb(
    data: *mut u8,
    data_len: usize,
    width: usize,
    height: usize,
    samples: usize,
    slope: f32,
    limit: f32,
) -> i32 {
    if data.is_null() {
        return -1;
    }

    let buffer = slice::from_raw_parts_mut(data, data_len);
    match automatic_color_equalization_rgb(buffer, width, height, samples, slope, limit) {
        Ok(()) => 0,
        Err(_) => -2,
    }
}

/// C ABI entry point for Python ctypes callers.
///
/// Returns 0 on success and a negative value for invalid input.
#[no_mangle]
pub unsafe extern "C" fn anshitsu_color_stretch_rgb(
    data: *mut u8,
    data_len: usize,
    width: usize,
    height: usize,
) -> i32 {
    if data.is_null() {
        return -1;
    }

    let buffer = slice::from_raw_parts_mut(data, data_len);
    match color_stretch_rgb(buffer, width, height) {
        Ok(()) => 0,
        Err(_) => -2,
    }
}

#[cfg(test)]
mod tests {
    use super::{automatic_color_equalization_rgb, color_stretch_rgb};

    #[test]
    fn keeps_constant_images_stable() {
        let mut data = vec![128_u8; 4 * 3];
        automatic_color_equalization_rgb(&mut data, 2, 2, 4, 10.0, 1000.0).unwrap();
        assert_eq!(data, vec![128_u8; 4 * 3]);
    }

    #[test]
    fn stretches_channel_contrast() {
        let mut data = vec![24, 64, 96, 32, 64, 104, 224, 192, 160, 240, 200, 176];
        automatic_color_equalization_rgb(&mut data, 2, 2, 4, 10.0, 1000.0).unwrap();
        assert_eq!(data.len(), 12);
        assert_eq!(data.iter().min(), Some(&0));
        assert_eq!(data.iter().max(), Some(&255));
    }

    #[test]
    fn rejects_invalid_buffer_lengths() {
        let mut data = vec![0_u8; 5];
        let result = automatic_color_equalization_rgb(&mut data, 2, 1, 2, 10.0, 1000.0);
        assert!(result.is_err());
    }

    #[test]
    fn color_stretch_balances_and_stretches_rgb_channels() {
        let mut data = vec![20, 60, 120, 40, 90, 150, 160, 180, 210, 180, 220, 240];
        color_stretch_rgb(&mut data, 2, 2).unwrap();
        assert_eq!(data.len(), 12);
        assert_eq!(data.iter().min(), Some(&0));
        assert_eq!(data.iter().max(), Some(&255));
    }

    #[test]
    fn color_stretch_rejects_invalid_buffer_lengths() {
        let mut data = vec![0_u8; 5];
        let result = color_stretch_rgb(&mut data, 2, 1);
        assert!(result.is_err());
    }
}
