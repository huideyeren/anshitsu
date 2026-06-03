import ctypes
import os
import platform
from pathlib import Path
from typing import Optional

from PIL import Image


def automatic_color_equalization(
    image: Image,
    samples: int = 500,
    slope: float = 10.0,
    limit: float = 1000.0,
) -> Optional[Image]:
    """
    Apply the Rust Automatic Color Equalization backend when available.

    Args:
        image: RGB image to process.
        samples: Maximum number of spatial samples used for ACE comparison.
        slope: Slope applied to channel differences before clipping.
        limit: Maximum absolute contrast contribution.

    Returns:
        Processed RGB image, or None when the native backend is unavailable.
    """
    library = _load_library()
    if library is None:
        return None

    rgb_image = image.convert("RGB")
    width, height = rgb_image.size
    buffer = bytearray(rgb_image.tobytes())
    array_type = ctypes.c_ubyte * len(buffer)
    c_buffer = array_type.from_buffer(buffer)

    result = library.anshitsu_ace_rgb(
        c_buffer,
        ctypes.c_size_t(len(buffer)),
        ctypes.c_size_t(width),
        ctypes.c_size_t(height),
        ctypes.c_size_t(samples),
        ctypes.c_float(slope),
        ctypes.c_float(limit),
    )
    if result != 0:
        return None

    return Image.frombytes("RGB", rgb_image.size, bytes(buffer))


def color_stretch(image: Image) -> Optional[Image]:
    """
    Apply the Rust gray-world and color stretching backend when available.

    Args:
        image: RGB image to process.

    Returns:
        Processed RGB image, or None when the native backend is unavailable.
    """
    library = _load_library()
    if library is None:
        return None

    rgb_image = image.convert("RGB")
    width, height = rgb_image.size
    buffer = bytearray(rgb_image.tobytes())
    array_type = ctypes.c_ubyte * len(buffer)
    c_buffer = array_type.from_buffer(buffer)

    result = library.anshitsu_color_stretch_rgb(
        c_buffer,
        ctypes.c_size_t(len(buffer)),
        ctypes.c_size_t(width),
        ctypes.c_size_t(height),
    )
    if result != 0:
        return None

    return Image.frombytes("RGB", rgb_image.size, bytes(buffer))


def _load_library() -> Optional[ctypes.CDLL]:
    path = _find_library_path()
    if path is None:
        return None

    try:
        library = ctypes.CDLL(str(path))
    except OSError:
        return None

    try:
        library.anshitsu_ace_rgb.argtypes = [
            ctypes.POINTER(ctypes.c_ubyte),
            ctypes.c_size_t,
            ctypes.c_size_t,
            ctypes.c_size_t,
            ctypes.c_size_t,
            ctypes.c_float,
            ctypes.c_float,
        ]
        library.anshitsu_ace_rgb.restype = ctypes.c_int
        library.anshitsu_color_stretch_rgb.argtypes = [
            ctypes.POINTER(ctypes.c_ubyte),
            ctypes.c_size_t,
            ctypes.c_size_t,
            ctypes.c_size_t,
        ]
        library.anshitsu_color_stretch_rgb.restype = ctypes.c_int
    except AttributeError:
        return None
    return library


def _find_library_path() -> Optional[Path]:
    env_path = os.environ.get("ANSHITSU_COLOR_LIB")
    if env_path:
        path = Path(env_path)
        if path.exists():
            return path

    library_name = _library_name()
    candidates = [
        Path(__file__).resolve().parents[1] / "_native" / library_name,
    ]
    repository_root = _repository_root()
    if repository_root is not None:
        candidates.append(
            repository_root
            / "native"
            / "anshitsu-color"
            / "target"
            / "release"
            / library_name
        )
        candidates.append(
            repository_root
            / "native"
            / "anshitsu-color"
            / "target"
            / "debug"
            / library_name
        )

    for candidate in candidates:
        if candidate.exists():
            return candidate

    return None


def _library_name() -> str:
    system = platform.system()
    if system == "Darwin":
        return "libanshitsu_color.dylib"
    if system == "Windows":
        return "anshitsu_color.dll"
    return "libanshitsu_color.so"


def _repository_root() -> Optional[Path]:
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    return None
