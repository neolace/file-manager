from enum import Enum


class fm_FileType(Enum):
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
    MD = "md"

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
    CS = "cs"
    TS = "ts"
