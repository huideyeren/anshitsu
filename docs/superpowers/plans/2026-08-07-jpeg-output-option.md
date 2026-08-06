# JPEG Output Option Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Keep PNG as the default output format and add `--jpeg` to save processed images as JPEG.

**Architecture:** `cli` owns the output filename and Pillow save call, so it will also select the format. A small JPEG-preparation helper will flatten transparency over white. The existing PNG metadata path remains intact, while JPEG receives only metadata its writer supports.

**Tech Stack:** Python 3.10+, Python Fire, Pillow, pytest.

## Global Constraints

- Omitting `--jpeg` must produce PNG for JPEG, PNG, and RAW inputs.
- `--jpeg` must produce JPEG with a `.jpg` output filename; do not add `--png`.
- Keep existing PNG EXIF, ICC profile, XMP, and text metadata behavior.
- Preserve EXIF, ICC profile, and XMP in JPEG output where Pillow supports them.
- Composite JPEG output with alpha over white.
- Apply the selected extension in both normal and `--overwrite` modes.

## File Structure

- `src/anshitsu/cli.py`: CLI option, format selection, JPEG image preparation, and writer-specific arguments.
- `tests/test_cli.py`: End-to-end CLI tests for default PNG, JPEG, alpha flattening, metadata, and overwrite naming.
- `README.md`: CLI reference, default behavior, and invocation examples.

### Task 1: Implement and test format-aware output

**Files:**
- Modify: `src/anshitsu/cli.py:1-183`
- Modify: `tests/test_cli.py:1-260`

**Interfaces:**
- Consumes: `cli(path: Optional[str] = None, ..., vignette: Optional[float] = None) -> str`.
- Produces: `cli(path: Optional[str] = None, ..., vignette: Optional[float] = None, jpeg: bool = False) -> str`.
- Produces: `_prepare_image_for_jpeg(image: Image.Image) -> Image.Image`.

- [ ] **Step 1: Read test-writing guidance**

Read `superpowers:test-driven-development/writing-good-tests.md`. Identify the production changes each test detects: absent `jpeg` option, wrong `.jpg` naming, and missing alpha flattening.

- [ ] **Step 2: Write a failing JPEG-output test**

Add to `tests/test_cli.py`:

```python
def test_main_saves_jpeg_when_jpeg_option_is_given(tmp_path):
    source = tmp_path / "input.png"
    Image.new("RGB", (2, 2), (1, 2, 3)).save(source)

    cli(str(source), jpeg=True)

    output = next((tmp_path / "anshitsu_out").glob("*.jpg"))
    assert output.suffix == ".jpg"
    with Image.open(output) as saved_image:
        assert saved_image.format == "JPEG"
```

- [ ] **Step 3: Verify the first test is red**

Run `pytest tests/test_cli.py::test_main_saves_jpeg_when_jpeg_option_is_given -v`.

Expected: FAIL because `cli()` has no `jpeg` parameter.

- [ ] **Step 4: Write a failing transparent-image JPEG test**

Add to `tests/test_cli.py`:

```python
def test_main_flattens_transparent_pixels_over_white_for_jpeg(tmp_path):
    source = tmp_path / "transparent.png"
    Image.new("RGBA", (1, 1), (0, 0, 0, 0)).save(source)

    cli(str(source), jpeg=True, keep_alpha=True)

    output = next((tmp_path / "anshitsu_out").glob("*.jpg"))
    with Image.open(output) as saved_image:
        red, green, blue = saved_image.convert("RGB").getpixel((0, 0))
    assert red > 245
    assert green > 245
    assert blue > 245
```

- [ ] **Step 5: Verify the second test is red**

Run `pytest tests/test_cli.py::test_main_flattens_transparent_pixels_over_white_for_jpeg -v`.

Expected: FAIL because `cli()` has no `jpeg` parameter.

- [ ] **Step 6: Add the smallest production change**

Import `Image` from `PIL`, then add:

```python
def _prepare_image_for_jpeg(image: Image.Image) -> Image.Image:
    if image.mode in ("RGBA", "LA") or "transparency" in image.info:
        rgba = image.convert("RGBA")
        flattened = Image.new("RGB", rgba.size, "white")
        flattened.alpha_composite(rgba)
        return flattened
    return image.convert("RGB") if image.mode != "RGB" else image
```

Add `jpeg: bool = False` and its docstring entry to `cli`. Use `"jpg" if jpeg else "png"` when building normal and overwrite filenames. In the JPEG branch, call `_prepare_image_for_jpeg(saved_image).save()` with `quality=100`, `subsampling=0`, EXIF, ICC profile, and XMP. In the PNG branch, keep the current save call, including `create_png_metadata_info`.

- [ ] **Step 7: Verify the two tests are green**

Run `pytest tests/test_cli.py::test_main_saves_jpeg_when_jpeg_option_is_given tests/test_cli.py::test_main_flattens_transparent_pixels_over_white_for_jpeg -v`.

Expected: PASS.

- [ ] **Step 8: Add default and overwrite regression tests**

Add to `tests/test_cli.py`:

```python
def test_main_uses_png_by_default(tmp_path):
    source = tmp_path / "input.jpg"
    Image.new("RGB", (2, 2), (1, 2, 3)).save(source)

    cli(str(source))

    output = next((tmp_path / "anshitsu_out").glob("*.png"))
    with Image.open(output) as saved_image:
        assert saved_image.format == "PNG"


def test_main_uses_jpeg_extension_in_overwrite_mode(tmp_path):
    source = tmp_path / "input.png"
    Image.new("RGB", (2, 2), (1, 2, 3)).save(source)

    cli(str(source), jpeg=True, overwrite=True)

    assert (tmp_path / "input.jpg").is_file()
    assert (tmp_path / "anshitsu_orig" / "input.png").is_file()
```

Extend the existing metadata test with JPEG output assertions for EXIF, ICC, and XMP only; do not assert PNG text chunks in the JPEG case.

- [ ] **Step 9: Verify the CLI test module**

Run `pytest tests/test_cli.py -v`.

Expected: PASS, including default-PNG compatibility, JPEG metadata, and overwrite naming.

- [ ] **Step 10: Commit Task 1**

Run `git add src/anshitsu/cli.py tests/test_cli.py` and `git commit -m "feat: add JPEG output option"`.

### Task 2: Document the option

**Files:**
- Modify: `README.md:26-162`

**Interfaces:**
- Consumes: `anshitsu <path> [--jpeg]`.
- Produces: documentation that states PNG is default and `--jpeg` selects JPEG for all supported inputs.

- [ ] **Step 1: Add the help reference entry**

After `--overwrite` in the README usage reference, add:

```text
    --jpeg=JPEG
        Type: bool
        Default: False
        Save the processed image as JPEG instead of the default PNG.
```

- [ ] **Step 2: Replace always-PNG prose and add examples**

State that PNG is the default and `--jpeg` selects JPEG for JPEG, PNG, and RAW inputs. Add:

```shell
anshitsu photo.png
anshitsu photo.png --jpeg
```

- [ ] **Step 3: Check help matches the README**

Run `python -m anshitsu.main --help`.

Expected: `--jpeg` appears with default `False` and wording consistent with the README.

- [ ] **Step 4: Commit Task 2**

Run `git add README.md` and `git commit -m "docs: describe JPEG output option"`.

### Task 3: Verify the completed feature

**Files:**
- Verify: `src/anshitsu/cli.py`, `tests/test_cli.py`, `README.md`

**Interfaces:**
- Consumes: completed Tasks 1 and 2.
- Produces: tested command-line output selection and matching documentation.

- [ ] **Step 1: Run the full suite**

Run `pytest -v`.

Expected: PASS with no failures, including RAW-image tests.

- [ ] **Step 2: Run project quality checks**

Run `black --check src tests`, `isort --check-only src tests`, `flake8 src tests`, and `mypy src`.

Expected: each command succeeds. If a tool is only available via Poetry, rerun it as `poetry run <command>` and report that substitution.

- [ ] **Step 3: Check the final worktree**

Run `git diff HEAD~2..HEAD --check` and `git status --short`.

Expected: no whitespace errors and no uncommitted changes.
