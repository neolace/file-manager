import os

FILE_TYPES_TO_KEEP = ["jpg", "jpeg", "png", "gif", "pdf", "doc", "docx", "xls", "xlsx", "txt"]
FOLDERS_TO_REMOVE = ["node_modules"]

DEFAULT_SRC_PATH = os.getenv("DEFAULT_SRC_PATH", "C:/Users/terti/Downloads/test")
DEFAULT_DST_PATH = os.getenv("DEFAULT_DST_PATH", "")
DEFAULT_LOG_PATH = os.getenv("DEFAULT_LOG_PATH", "file_manager.log")

DEFAULT_FONT = "slant"
