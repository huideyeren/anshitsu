# Output format selection design

## Goal

Keep PNG as Anshitsu's default output format, while allowing callers to request
JPEG output explicitly with a `--jpeg` command-line option.

## Command-line behavior

`cli` will accept a new boolean `jpeg` argument, exposed by Python Fire as
`--jpeg`.

| Invocation | Output format | Output filename extension |
| --- | --- | --- |
| no format option | PNG | `.png` |
| `--jpeg` | JPEG | `.jpg` |

There is intentionally no `--png` option: omitting `--jpeg` is the explicit
and documented way to select PNG output. The rule applies to standard images
and RAW images alike.

## Saving behavior

A single format-selection path will determine both the filename extension and
the Pillow save parameters, so ordinary output and `--overwrite` output cannot
diverge.

PNG output will continue to preserve EXIF, ICC profiles, PNG text chunks, and
XMP using the existing metadata helpers. JPEG output will preserve EXIF, ICC
profiles, and XMP, but will not attempt to write PNG-only text chunks.

JPEG cannot encode alpha. Before saving a processed image as JPEG, Anshitsu
will composite any transparency over white and save an RGB image. Images
without alpha remain unchanged apart from any existing processor output.

## Errors and compatibility

No mutually exclusive format flags exist, so no new command-line conflict
case is introduced. Existing invocations retain their PNG output and naming
behavior. RAW development remains unchanged; only the chosen final container
format controls how its processed pixels are written.

## Verification

Tests will verify default PNG output, `--jpeg` output and extension, JPEG
conversion of transparent images, metadata appropriate to each format, and
the same format selection when `--overwrite` is used. The focused tests and
the full test suite will be run after the change.
