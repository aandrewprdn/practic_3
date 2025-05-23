from pathlib import Path

from pypdf import PdfReader


def extract_pages(path: Path) -> list[str]:
    """
    Args:
        path: pathlib.Path to pdf file
    Returns:
         List of str by pages
    """
    reader = PdfReader(path)

    pages_text: list[str] = []
    for page in reader.pages:
        pages_text.append(page.extract_text())

    return pages_text