import os
from enum import Enum
from typing import List


class FileType(Enum):
    """Supported file types for processing."""

    # Images
    JPG = "jpg"
    JPEG = "jpeg"
    PNG = "png"
    GIF = "gif"
    BMP = "bmp"
    TIFF = "tiff"
    SVG = "svg"
    WEBP = "webp"
    ICO = "ico"

    # Documents
    PDF = "pdf"
    DOC = "doc"
    DOCX = "docx"
    XLS = "xls"
    XLSX = "xlsx"
    TXT = "txt"

    # Archives
    ZIP = "zip"
    RAR = "rar"
    TAR = "tar"
    GZ = "gz"
    BZ2 = "bz2"
    SZ = "7z"

    # Audio
    MP3 = "mp3"
    WAV = "wav"
    OGG = "ogg"
    FLAC = "flac"

    # Media
    MP4 = "mp4"
    AVI = "avi"
    MKV = "mkv"
    MOV = "mov"
    FLV = "flv"
    WMV = "wmv"
    M4A = "m4a"
    AAC = "aac"
    OPUS = "opus"

    # Web
    JSON = "json"
    XML = "xml"
    HTML = "html"
    CSS = "css"
    JS = "js"


class Config:
    """Application configuration settings."""

    EXCLUDED_FOLDERS: List[str] = ["node_modules"]
    DEFAULT_FONT: str = "slant"

    # Environment-dependent paths with defaults
    DEFAULT_SRC_PATH: str = os.getenv("DEFAULT_SRC_PATH", "")
    DEFAULT_DST_PATH: str = os.getenv("DEFAULT_DST_PATH", "")
    DEFAULT_LOG_PATH: str = os.getenv("DEFAULT_LOG_PATH", "")

    @classmethod
    def get_supported_extensions(cls) -> List[str]:
        """Returns a list of all supported file extensions."""
        return [ft.value for ft in FileType]
