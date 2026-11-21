from pathlib import Path

from pypdf import PdfReader
from pypdf.errors import PyPdfError

SUPPORTED_TYPES = [".md", ".txt", ".pdf"]


class ReadError(Exception):
    """A file problem with a readable message, meant to be shown in the UI."""


def _read_text_file(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as error:
        raise ReadError("The file is not valid UTF-8 text.") from error


def _read_pdf(path: Path) -> str:
    try:
        reader = PdfReader(path)
        if reader.is_encrypted:
            raise ReadError("The PDF is password-protected.")
        pages = [page.extract_text() or "" for page in reader.pages]
    except PyPdfError as error:
        raise ReadError("Could not read the PDF. It may be damaged.") from error

    text = "\n\n".join(pages).strip()
    if not text:
        raise ReadError(
            "No text found in the PDF. Scanned PDFs are images, which are not supported yet."
        )
    return text


def read_document(file_path: str) -> str:
    path = Path(file_path)
    suffix = path.suffix.lower()

    if suffix in (".md", ".txt"):
        return _read_text_file(path)
    if suffix == ".pdf":
        return _read_pdf(path)
    raise ReadError(f"Unsupported file type: {suffix or 'unknown'}")