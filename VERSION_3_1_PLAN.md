# Anshitsu 3.1.0 Plan

This document records the current plan for Anshitsu 3.1.0.

## Goals

- Resolve dependency update pull requests.
- Add an orthochromatic-style grayscale conversion.
- Add an ACROS-style monochrome preset.
- Reorganize the image processing pipeline.
- Keep room for a film-negative inversion step for orange-mask scans.

## Processing Pipeline

The planned processing order is:

1. Input preparation
   - Save alpha for `keep_alpha`.
   - Remove alpha before processing.
2. Film negative inversion
   - `invert`
   - future negative-film inversion for orange-mask scans
3. Base color correction
   - `color_auto_adjust`
   - `color_stretch`
4. Color presets
   - `rochester`
   - `ashigara`
5. Manual adjustments
   - `color`
   - `brightness`
   - `sharpness`
   - `posterize`
6. Monochrome presets
   - `grayscale`
   - future `orthochromatic`
   - future `acros`
   - `tosaka`
7. Finishing adjustments
   - `contrast`
   - `line_drawing`
   - `noise`
   - `vignette`
8. Toning
   - `sepia`
   - `cyanotype`
9. Output
   - `outputrgb`
   - restore alpha when requested

The pipeline should be deterministic and documented. Options do not need
strict mutual exclusion at this stage; ordering should define the result when
multiple options are specified.

## Color Processing

`invert` should remain early in the pipeline. Anshitsu was originally used for
processing scans from photographic film, so inverting a negative before color
correction is a valid and expected workflow.

The color processing priority is:

1. `color_auto_adjust` and `color_stretch`
2. `rochester` and `ashigara`
3. monochrome presets

This allows a user to correct or grade a color image before converting it to a
monochrome result.

## Monochrome Processing

Monochrome conversions and monochrome presets should normally return `L`.

Planned roles:

- `grayscale`
  - Standard luminance-based conversion.
  - Remains the baseline grayscale conversion.
- `orthochromatic`
  - A separate monochrome conversion path.
  - Red tones should become darker, and blue tones should become lighter.
  - This should model the older orthochromatic look.
- `acros`
  - A full monochrome preset rather than just a conversion.
  - Inspired by Fujifilm ACROS.
  - Should emphasize smooth tone, controlled highlights, firm blacks, and subtle
    grain.
- `tosaka`
  - Remains a distinctive special mode.
  - It is intentionally biased and expressive, aiming for a rough Kodak Tri-X
    monochrome feel.

## Toning

`sepia` and `cyanotype` should be treated as toning steps.

They should work with any `L` output from:

- `grayscale`
- future `orthochromatic`
- future `acros`
- `tosaka`

If `sepia` or `cyanotype` is specified without an explicit monochrome preset,
the processor may keep the current backward-compatible behavior by applying the
standard grayscale conversion first.

When `sepia` or `cyanotype` is used, the final image becomes RGB. Otherwise,
monochrome presets stay as `L` unless `outputrgb` is specified.

## Output Rules

- Monochrome presets return `L`.
- `outputrgb` converts a final `L` image to RGB.
- `sepia` and `cyanotype` convert a final `L` image to RGB through toning.
- Color presets return RGB.

## Future Negative-Film Inversion

A future negative-film inversion mode should be separate from plain `invert`.

The rough goal is to handle orange-mask negative scans:

1. Convert to RGB.
2. Estimate or compensate for the orange film base.
3. Invert the image.
4. Let `color_auto_adjust` or `color_stretch` handle the later color correction.

The first implementation can be approximate. It does not need to solve every
film stock or scanner profile. The important part is to provide a better
starting point than plain RGB inversion for orange-mask negative scans.

## Later Plan: 3.2.0

Anshitsu 3.2.0 may focus on performance work for the heavier color correction
algorithms.

Candidate work:

- Rewrite `color_auto_adjust` in a faster native implementation.
- Rewrite `color_stretch` in a faster native implementation.
- Consider implementing the native library in C#.
- Consider AOT compilation for startup and runtime performance.
- Keep the Python API stable so existing CLI options and `Processor` behavior
  do not change.

The first target should be implementation compatibility with the current
algorithms. Any visual changes should be deliberate and covered by regression
tests or sample-image comparisons.

## Later Plan: RAW Development

RAW development support may be useful in a later release.

Initial target camera ecosystems:

- Canon
- PENTAX
- Apple

Nikon, Sony, and other camera ecosystems can be handled later.

The initial goal should be practical support for the author's current
equipment, not broad RAW compatibility. The RAW development stage should happen
before the normal Anshitsu processing pipeline so that existing presets and
adjustments can operate on the developed image.

Open design points:

- Choose the RAW backend.
- Decide how to expose RAW-specific options in the CLI.
- Decide whether RAW development should output an intermediate RGB image before
  applying normal processing.
- Prepare sample RAW files for regression and visual comparison.
