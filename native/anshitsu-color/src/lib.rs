use std::cmp::max;
use std::slice;

const ACE_WORKING_LONG_EDGE: usize = 96;
const ACE_CORRECTION_STRENGTH: f32 = 0.68;
const ACE_CORRECTION_LIMIT: f32 = 42.0;
const ACE_NEGATIVE_CORRECTION_SCALE: f32 = 0.38;

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

    if sample_limit >= pixels && max(width, height) > ACE_WORKING_LONG_EDGE {
        return automatic_color_equalization_with_correction_map(data, width, height, slope, limit);
    }

    automatic_color_equalization_direct(data, width, height, sample_limit, slope, limit)
}

fn automatic_color_equalization_direct(
    data: &mut [u8],
    width: usize,
    height: usize,
    sample_limit: usize,
    slope: f32,
    limit: f32,
) -> Result<(), &'static str> {
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

fn automatic_color_equalization_with_correction_map(
    data: &mut [u8],
    width: usize,
    height: usize,
    slope: f32,
    limit: f32,
) -> Result<(), &'static str> {
    let (map_width, map_height) = working_size(width, height, ACE_WORKING_LONG_EDGE);
    let source_map = resize_rgb(data, width, height, map_width, map_height);
    let mut adjusted_map = source_map.clone();
    automatic_color_equalization_direct(
        &mut adjusted_map,
        map_width,
        map_height,
        map_width * map_height,
        slope,
        limit,
    )?;

    let mut correction_map = correction_map(&source_map, &adjusted_map);
    smooth_correction_map(&mut correction_map, map_width, map_height);
    apply_correction_map(data, width, height, &correction_map, map_width, map_height);
    Ok(())
}

fn working_size(width: usize, height: usize, long_edge: usize) -> (usize, usize) {
    let current_long_edge = max(width, height);
    if current_long_edge <= long_edge {
        return (width, height);
    }

    if width >= height {
        let map_width = long_edge;
        let map_height = max(1, (height * long_edge + width / 2) / width);
        (map_width, map_height)
    } else {
        let map_height = long_edge;
        let map_width = max(1, (width * long_edge + height / 2) / height);
        (map_width, map_height)
    }
}

fn resize_rgb(
    data: &[u8],
    width: usize,
    height: usize,
    target_width: usize,
    target_height: usize,
) -> Vec<u8> {
    let mut resized = vec![0_u8; target_width * target_height * 3];
    let x_scale = width as f32 / target_width as f32;
    let y_scale = height as f32 / target_height as f32;

    for y in 0..target_height {
        let y_start = y as f32 * y_scale;
        let y_end = (y + 1) as f32 * y_scale;
        let source_y_start = y_start.floor() as usize;
        let source_y_end = y_end.ceil().min(height as f32) as usize;
        for x in 0..target_width {
            let x_start = x as f32 * x_scale;
            let x_end = (x + 1) as f32 * x_scale;
            let source_x_start = x_start.floor() as usize;
            let source_x_end = x_end.ceil().min(width as f32) as usize;
            let target_index = (y * target_width + x) * 3;
            let mut total = [0.0_f32; 3];
            let mut weight_total = 0.0_f32;

            for source_y in source_y_start..source_y_end {
                let pixel_y_start = source_y as f32;
                let pixel_y_end = pixel_y_start + 1.0;
                let y_weight = (y_end.min(pixel_y_end) - y_start.max(pixel_y_start)).max(0.0);
                if y_weight <= 0.0 {
                    continue;
                }

                for source_x in source_x_start..source_x_end {
                    let pixel_x_start = source_x as f32;
                    let pixel_x_end = pixel_x_start + 1.0;
                    let x_weight = (x_end.min(pixel_x_end) - x_start.max(pixel_x_start)).max(0.0);
                    if x_weight <= 0.0 {
                        continue;
                    }

                    let weight = x_weight * y_weight;
                    let source_index = (source_y * width + source_x) * 3;
                    for channel in 0..3 {
                        total[channel] += data[source_index + channel] as f32 * weight;
                    }
                    weight_total += weight;
                }
            }

            if weight_total > 0.0 {
                for channel in 0..3 {
                    resized[target_index + channel] =
                        (total[channel] / weight_total).round().clamp(0.0, 255.0) as u8;
                }
            }
        }
    }

    resized
}

fn correction_map(source: &[u8], adjusted: &[u8]) -> Vec<f32> {
    source
        .iter()
        .zip(adjusted)
        .map(|(before, after)| *after as f32 - *before as f32)
        .collect()
}

fn smooth_correction_map(correction_map: &mut [f32], width: usize, height: usize) {
    if width <= 1 || height <= 1 {
        return;
    }

    let original = correction_map.to_vec();
    for y in 0..height {
        for x in 0..width {
            for channel in 0..3 {
                let mut total = 0.0_f32;
                let mut weight_total = 0.0_f32;

                for offset_y in -1_i32..=1 {
                    for offset_x in -1_i32..=1 {
                        let sample_x = clamp_offset(x, offset_x, width);
                        let sample_y = clamp_offset(y, offset_y, height);
                        let weight = if offset_x == 0 && offset_y == 0 {
                            4.0
                        } else if offset_x == 0 || offset_y == 0 {
                            2.0
                        } else {
                            1.0
                        };
                        total += correction_value(&original, width, sample_x, sample_y, channel)
                            * weight;
                        weight_total += weight;
                    }
                }

                correction_map[(y * width + x) * 3 + channel] = total / weight_total;
            }
        }
    }
}

fn clamp_offset(position: usize, offset: i32, limit: usize) -> usize {
    if offset < 0 {
        position.saturating_sub(offset.unsigned_abs() as usize)
    } else {
        (position + offset as usize).min(limit - 1)
    }
}

fn apply_correction_map(
    data: &mut [u8],
    width: usize,
    height: usize,
    correction_map: &[f32],
    map_width: usize,
    map_height: usize,
) {
    let source = data.to_vec();
    for y in 0..height {
        let (y0, y1, y_weight) = interpolation_axis(y, height, map_height);
        for x in 0..width {
            let (x0, x1, x_weight) = interpolation_axis(x, width, map_width);
            let pixel_index = (y * width + x) * 3;
            let luminance = pixel_luminance(&source, width, x, y);
            let shadow_weight = shadow_correction_weight(luminance);
            let edge_weight = local_edge_weight(&source, width, height, x, y, luminance);

            for channel in 0..3 {
                let top_left = correction_value(correction_map, map_width, x0, y0, channel);
                let top_right = correction_value(correction_map, map_width, x1, y0, channel);
                let bottom_left = correction_value(correction_map, map_width, x0, y1, channel);
                let bottom_right = correction_value(correction_map, map_width, x1, y1, channel);
                let top = top_left + (top_right - top_left) * x_weight;
                let bottom = bottom_left + (bottom_right - bottom_left) * x_weight;
                let mut correction = (top + (bottom - top) * y_weight)
                    .clamp(-ACE_CORRECTION_LIMIT, ACE_CORRECTION_LIMIT);
                if correction < 0.0 {
                    correction *= ACE_NEGATIVE_CORRECTION_SCALE
                        * local_darkening_weight(&source, width, height, x, y, luminance);
                }
                correction *= ACE_CORRECTION_STRENGTH * shadow_weight * edge_weight;
                let value = source[pixel_index + channel] as f32 + correction;
                data[pixel_index + channel] = value.round().clamp(0.0, 255.0) as u8;
            }
        }
    }
}

fn shadow_correction_weight(luminance: f32) -> f32 {
    let normalized = (luminance / 255.0).clamp(0.0, 1.0);
    0.35 + 0.65 * smoothstep(0.08, 0.42, normalized)
}

fn local_darkening_weight(
    data: &[u8],
    width: usize,
    height: usize,
    x: usize,
    y: usize,
    luminance: f32,
) -> f32 {
    let x_start = x.saturating_sub(1);
    let y_start = y.saturating_sub(1);
    let x_end = (x + 1).min(width - 1);
    let y_end = (y + 1).min(height - 1);
    let mut total = 0.0_f32;
    let mut count = 0.0_f32;
    let mut min_luminance = luminance;
    let mut max_luminance = luminance;

    for sample_y in y_start..=y_end {
        for sample_x in x_start..=x_end {
            if sample_x == x && sample_y == y {
                continue;
            }
            let value = pixel_luminance(data, width, sample_x, sample_y);
            total += value;
            count += 1.0;
            min_luminance = min_luminance.min(value);
            max_luminance = max_luminance.max(value);
        }
    }

    if count <= 0.0 {
        return 1.0;
    }

    let average = total / count;
    let contrast = max_luminance - min_luminance;
    let dark_gap = (average - luminance).max(0.0);
    let edge_strength = smoothstep(18.0, 72.0, contrast) * smoothstep(6.0, 32.0, dark_gap);
    1.0 - 0.78 * edge_strength
}

fn local_edge_weight(
    data: &[u8],
    width: usize,
    height: usize,
    x: usize,
    y: usize,
    luminance: f32,
) -> f32 {
    let (_, _, min_luminance, max_luminance) = local_luminance_stats(data, width, height, x, y);
    let contrast = (max_luminance - min_luminance).max((luminance - min_luminance).abs());
    1.0 - 0.42 * smoothstep(24.0, 96.0, contrast)
}

fn local_luminance_stats(
    data: &[u8],
    width: usize,
    height: usize,
    x: usize,
    y: usize,
) -> (f32, f32, f32, f32) {
    let x_start = x.saturating_sub(1);
    let y_start = y.saturating_sub(1);
    let x_end = (x + 1).min(width - 1);
    let y_end = (y + 1).min(height - 1);
    let mut total = 0.0_f32;
    let mut count = 0.0_f32;
    let mut min_luminance = f32::INFINITY;
    let mut max_luminance = f32::NEG_INFINITY;

    for sample_y in y_start..=y_end {
        for sample_x in x_start..=x_end {
            let value = pixel_luminance(data, width, sample_x, sample_y);
            total += value;
            count += 1.0;
            min_luminance = min_luminance.min(value);
            max_luminance = max_luminance.max(value);
        }
    }

    (total, count, min_luminance, max_luminance)
}

fn pixel_luminance(data: &[u8], width: usize, x: usize, y: usize) -> f32 {
    let index = (y * width + x) * 3;
    data[index] as f32 * 0.299 + data[index + 1] as f32 * 0.587 + data[index + 2] as f32 * 0.114
}

fn smoothstep(edge0: f32, edge1: f32, value: f32) -> f32 {
    if edge0 >= edge1 {
        return 0.0;
    }
    let x = ((value - edge0) / (edge1 - edge0)).clamp(0.0, 1.0);
    x * x * (3.0 - 2.0 * x)
}

fn correction_value(
    correction_map: &[f32],
    map_width: usize,
    x: usize,
    y: usize,
    channel: usize,
) -> f32 {
    correction_map[(y * map_width + x) * 3 + channel]
}

fn interpolation_axis(position: usize, length: usize, map_length: usize) -> (usize, usize, f32) {
    if map_length <= 1 || length <= 1 {
        return (0, 0, 0.0);
    }

    let numerator = position * (map_length - 1);
    let denominator = length - 1;
    let lower = numerator / denominator;
    let upper = (lower + 1).min(map_length - 1);
    let weight = (numerator % denominator) as f32 / denominator as f32;
    (lower, upper, weight)
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
    use super::{
        automatic_color_equalization_rgb, color_stretch_rgb, local_darkening_weight,
        local_edge_weight, resize_rgb,
    };

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
    fn correction_map_path_keeps_large_constant_images_stable() {
        let width = 128;
        let height = 1;
        let mut data = vec![128_u8; width * height * 3];

        automatic_color_equalization_rgb(&mut data, width, height, width * height, 10.0, 1000.0)
            .unwrap();

        assert_eq!(data, vec![128_u8; width * height * 3]);
    }

    #[test]
    fn correction_map_path_processes_large_gradients() {
        let width = 128;
        let height = 1;
        let mut data = Vec::with_capacity(width * height * 3);
        for x in 0..width {
            let value = (x * 255 / (width - 1)) as u8;
            data.extend_from_slice(&[value, value.saturating_div(2), 255 - value]);
        }

        automatic_color_equalization_rgb(&mut data, width, height, width * height, 10.0, 1000.0)
            .unwrap();

        assert_eq!(data.len(), width * height * 3);
        assert_eq!(data.iter().min(), Some(&0));
        assert_eq!(data.iter().max(), Some(&255));
    }

    #[test]
    fn local_darkening_weight_suppresses_dark_edges() {
        let data = vec![
            192, 192, 192, 192, 192, 192, 192, 192, 192, 192, 192, 192, 16, 16, 16, 192, 192, 192,
            192, 192, 192, 192, 192, 192, 192, 192, 192,
        ];

        let weight = local_darkening_weight(&data, 3, 3, 1, 1, 16.0);

        assert!(weight < 0.5);
    }

    #[test]
    fn local_edge_weight_suppresses_high_contrast_edges() {
        let data = vec![
            16, 16, 16, 16, 16, 16, 224, 224, 224, 16, 16, 16, 16, 16, 16, 224, 224, 224, 16, 16,
            16, 16, 16, 16, 224, 224, 224,
        ];

        let weight = local_edge_weight(&data, 3, 3, 1, 1, 16.0);

        assert!(weight < 0.7);
    }

    #[test]
    fn resize_rgb_uses_area_average_when_downscaling() {
        let data = vec![
            0, 0, 0, 10, 20, 30, 20, 40, 60, 30, 60, 90, 40, 80, 120, 50, 100, 150, 60, 120, 180,
            70, 140, 210, 80, 160, 240, 90, 180, 255, 100, 200, 255, 110, 220, 255, 120, 240, 255,
            130, 255, 255, 140, 255, 255, 150, 255, 255,
        ];

        let resized = resize_rgb(&data, 4, 4, 2, 2);

        assert_eq!(
            resized,
            vec![25, 50, 75, 45, 90, 135, 105, 209, 251, 125, 233, 255]
        );
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
