import base64
import csv
import hashlib
import io
import platform
import shutil
import subprocess
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NATIVE_CRATE = ROOT / "native" / "anshitsu-color" / "Cargo.toml"
NATIVE_PACKAGE_DIR = ROOT / "src" / "anshitsu" / "_native"
DIST_DIR = ROOT / "dist"


def main() -> None:
    """
    Build a platform-specific wheel with the Rust color backend bundled.
    """
    platform_tag = _platform_tag()
    library_name = _library_name()
    library_path = (
        ROOT / "native" / "anshitsu-color" / "target" / "release" / library_name
    )

    _run(["cargo", "build", "--release", "--manifest-path", str(NATIVE_CRATE)])
    if not library_path.exists():
        raise RuntimeError(f"Native library was not built: {library_path}")

    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)

    NATIVE_PACKAGE_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy2(library_path, NATIVE_PACKAGE_DIR / library_name)

    _run(["poetry", "build", "-f", "wheel"])
    wheel_path = _single_wheel()
    _retag_wheel(wheel_path, platform_tag)
    wheel_path.unlink()


def _platform_tag() -> str:
    system = platform.system()
    machine = platform.machine().lower()

    if system == "Darwin":
        if machine == "arm64":
            return "macosx_11_0_arm64"
        return "macosx_10_15_x86_64"

    if system == "Windows":
        if machine in {"amd64", "x86_64"}:
            return "win_amd64"
        raise RuntimeError(f"Unsupported Windows architecture: {machine}")

    if system == "Linux":
        if machine in {"amd64", "x86_64"}:
            return "manylinux_2_28_x86_64"
        if machine in {"aarch64", "arm64"}:
            return "manylinux_2_28_aarch64"
        raise RuntimeError(f"Unsupported Linux architecture: {machine}")

    raise RuntimeError(f"Unsupported platform: {system}")


def _library_name() -> str:
    system = platform.system()
    if system == "Darwin":
        return "libanshitsu_color.dylib"
    if system == "Windows":
        return "anshitsu_color.dll"
    return "libanshitsu_color.so"


def _single_wheel() -> Path:
    wheels = sorted(DIST_DIR.glob("*.whl"))
    if len(wheels) != 1:
        raise RuntimeError(f"Expected exactly one wheel in dist, found {len(wheels)}")
    return wheels[0]


def _retag_wheel(wheel_path: Path, platform_tag: str) -> Path:
    python_tag = "py3"
    abi_tag = "none"
    old_tag = f"{python_tag}-{abi_tag}-any"
    new_tag = f"{python_tag}-{abi_tag}-{platform_tag}"
    new_wheel_path = wheel_path.with_name(wheel_path.name.replace(old_tag, new_tag))
    record_path = ""
    files: dict[str, bytes] = {}

    with zipfile.ZipFile(wheel_path, "r") as wheel:
        for name in wheel.namelist():
            files[name] = wheel.read(name)
            if name.endswith(".dist-info/RECORD"):
                record_path = name

    if not record_path:
        raise RuntimeError(f"RECORD file was not found in {wheel_path}")

    for name, content in list(files.items()):
        if name.endswith(".dist-info/WHEEL"):
            files[name] = content.replace(
                f"Tag: {old_tag}\n".encode(),
                f"Tag: {new_tag}\n".encode(),
            )

    files[record_path] = _build_record(files, record_path)

    with zipfile.ZipFile(new_wheel_path, "w", zipfile.ZIP_DEFLATED) as wheel:
        for name, content in files.items():
            wheel.writestr(name, content)

    return new_wheel_path


def _build_record(files: dict[str, bytes], record_path: str) -> bytes:
    output = io.StringIO()
    writer = csv.writer(output, lineterminator="\n")

    for name in sorted(files):
        if name == record_path:
            writer.writerow([name, "", ""])
            continue
        content = files[name]
        digest = base64.urlsafe_b64encode(hashlib.sha256(content).digest())
        hash_value = digest.rstrip(b"=").decode("ascii")
        writer.writerow([name, f"sha256={hash_value}", str(len(content))])

    return output.getvalue().encode()


def _run(command: list[str]) -> None:
    subprocess.run(command, cwd=ROOT, check=True)


if __name__ == "__main__":
    main()
