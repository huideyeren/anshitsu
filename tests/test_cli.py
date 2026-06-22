import fire
import pytest
from PIL import ExifTags, Image, ImageCms

from anshitsu.__version__ import version
from anshitsu.cli import cli
from anshitsu.image_io import create_png_metadata_info


def test_main_for_dir(capsys, setup):
    fire.Fire(cli, [str(setup), "--tosaka=2.4", "--outputrgb"])
    captured = capsys.readouterr()
    result = captured.out
    assert "The cli was completed successfully." in result


def test_main_for_image_file(capsys, setup):
    fire.Fire(cli, [str(setup / "dog.jpg")])
    captured = capsys.readouterr()
    result = captured.out
    assert "The cli was completed successfully." in result


@pytest.mark.parametrize("extension", ["jpg", "png"])
def test_main_preserves_standard_image_exif(tmp_path, extension):
    """CLI output must retain EXIF, ICC, and XMP from JPEG and PNG inputs."""
    source = tmp_path / f"input.{extension}"
    exif = Image.Exif()
    exif_ifd = exif.get_ifd(ExifTags.IFD.Exif)
    exif_ifd[ExifTags.Base.LensMake] = "Example Lens Maker"
    exif_ifd[ExifTags.Base.LensModel] = "Example 35mm F2"
    icc_profile = ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB")).tobytes()
    xmp = b'<x:xmpmeta xmlns:x="adobe:ns:meta/">metadata</x:xmpmeta>'
    save_options = {"exif": exif.tobytes(), "icc_profile": icc_profile}
    if extension == "jpg":
        save_options["xmp"] = xmp
    else:
        save_options["pnginfo"] = create_png_metadata_info(
            {
                "Comment": "日本語の説明",
                "Description": "VRChat screenshot metadata",
                "Make": "Example Application",
                "Raw profile type iptc": "IPTC profile data",
            },
            xmp,
        )
    Image.new("RGB", (2, 2), (1, 2, 3)).save(source, **save_options)

    cli(str(source))

    output = next((tmp_path / "anshitsu_out").glob("*.png"))
    with Image.open(output) as saved_image:
        saved_exif_ifd = saved_image.getexif().get_ifd(ExifTags.IFD.Exif)
        assert saved_exif_ifd[ExifTags.Base.LensMake] == "Example Lens Maker"
        assert saved_exif_ifd[ExifTags.Base.LensModel] == "Example 35mm F2"
        assert saved_image.info["icc_profile"] == icc_profile
        assert saved_image.info["xmp"] == xmp
        if extension == "png":
            assert saved_image.text["Comment"] == "日本語の説明"
            assert saved_image.text["Description"] == "VRChat screenshot metadata"
            assert saved_image.text["Make"] == "Example Application"
            assert saved_image.text["Raw profile type iptc"] == "IPTC profile data"


def test_main_for_vignette(capsys, setup):
    fire.Fire(cli, [str(setup / "dog.jpg"), "--vignette=0.8"])
    captured = capsys.readouterr()
    result = captured.out
    assert "The cli was completed successfully." in result


def test_main_for_rochester(capsys, setup):
    fire.Fire(cli, [str(setup / "dog.jpg"), "--rochester"])
    captured = capsys.readouterr()
    result = captured.out
    assert "The cli was completed successfully." in result


def test_main_for_ashigara(capsys, setup):
    fire.Fire(cli, [str(setup / "dog.jpg"), "--ashigara"])
    captured = capsys.readouterr()
    result = captured.out
    assert "The cli was completed successfully." in result


def test_main_for_crossprocess(capsys, setup):
    fire.Fire(cli, [str(setup / "dog.jpg"), "--crossprocess"])
    captured = capsys.readouterr()
    result = captured.out
    assert "The cli was completed successfully." in result


def test_main_for_apocalypse(capsys, setup):
    fire.Fire(cli, [str(setup / "dog.jpg"), "--apocalypse"])
    captured = capsys.readouterr()
    result = captured.out
    assert "The cli was completed successfully." in result


def test_main_for_orthochromatic(capsys, setup):
    fire.Fire(cli, [str(setup / "dog.jpg"), "--orthochromatic"])
    captured = capsys.readouterr()
    result = captured.out
    assert "The cli was completed successfully." in result


def test_main_for_roppongi(capsys, setup):
    fire.Fire(cli, [str(setup / "dog.jpg"), "--roppongi"])
    captured = capsys.readouterr()
    result = captured.out
    assert "The cli was completed successfully." in result


def test_main_for_classic(capsys, setup):
    fire.Fire(cli, [str(setup / "dog.jpg"), "--classic"])
    captured = capsys.readouterr()
    result = captured.out
    assert "The cli was completed successfully." in result


def test_main_for_invalid_directory(capfd, setup):
    with pytest.raises(SystemExit):
        fire.Fire(cli, ["./src/anshitsu/"])
    captured = capfd.readouterr()
    error = captured.err

    assert "There are no JPEG, PNG, or RAW files in this directory." in error


def test_main_for_raw_file(monkeypatch, capsys, setup):
    raw_path = setup / "input.dng"
    raw_path.write_bytes(b"raw")

    def open_image(path):
        assert path == str(raw_path)
        return Image.new("RGB", (1, 1), (1, 2, 3))

    monkeypatch.setattr("anshitsu.cli.open_image", open_image)

    fire.Fire(cli, [str(raw_path)])
    captured = capsys.readouterr()
    result = captured.out

    assert "The cli was completed successfully." in result


def test_main_for_invalid_file(capfd, setup):
    with pytest.raises(SystemExit):
        fire.Fire(cli, ["./README.md"])
    captured = capfd.readouterr()
    error = captured.err

    assert "cannot identify image file" in error


def test_main_for_string_not_path(capfd, setup):
    with pytest.raises(SystemExit):
        fire.Fire(cli, ["pic"])
    captured = capfd.readouterr()
    error = captured.err

    assert "A non-path string was passed." in error


def test_main_for_creating_directory_by_default(capfd, setup):
    fire.Fire(cli, [str(setup / "dog.jpg")])
    captured = capfd.readouterr()
    error = captured.err

    assert (setup / "anshitsu_out").exists()


def test_main_for_creating_directory_by_overwrite_mode(capfd, setup):
    fire.Fire(cli, [str(setup / "dog.jpg"), "--overwrite", "--tosaka=2.4"])
    captured = capfd.readouterr()
    error = captured.err

    assert (setup / "anshitsu_orig").exists()


def test_main_for_saving_original_files_by_overwrite_mode(capfd, setup):
    fire.Fire(cli, [str(setup / "dog.jpg"), "--overwrite", "--tosaka=2.4"])
    captured = capfd.readouterr()
    error = captured.err

    assert (setup / "anshitsu_orig/dog.jpg").exists()


def test_main_for_exist_converted_files_by_overwrite_mode(capfd, setup):
    fire.Fire(cli, [str(setup / "dog.jpg"), "--overwrite", "--tosaka=2.4"])
    captured = capfd.readouterr()
    error = captured.err

    assert (setup / "dog.png").exists()


def test_main_for_show_version(capfd, setup):
    fire.Fire(cli, ["--version"])
    captured = capfd.readouterr()
    result = captured.out

    assert "Anshitsu version {0}".format(version) in result


def test_main_for_no_path(capfd, setup):
    with pytest.raises(SystemExit):
        fire.Fire(cli, [])
    captured = capfd.readouterr()
    error = captured.err

    assert "No path specified!" in error
