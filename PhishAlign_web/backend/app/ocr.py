from pathlib import Path
import io

from PIL import Image
import pytesseract


TESSERACT_CMD = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD


def _run_ocr(image: Image.Image) -> dict:
    try:
        text = pytesseract.image_to_string(
            image,
            lang="eng",
            config="--psm 6",
            timeout=30,
        ).strip()

        return {
            "text": text,
            "status": "ok",
            "error": "",
        }

    except Exception as exc:
        return {
            "text": "",
            "status": "error",
            "error": str(exc),
        }


def ocr_image(image: Image.Image) -> dict:
    return _run_ocr(image.convert("RGB"))


def ocr_from_path(image_path: str | Path) -> dict:
    try:
        with Image.open(image_path) as image:
            return ocr_image(image)

    except Exception as exc:
        return {
            "text": "",
            "status": "error",
            "error": str(exc),
        }


def ocr_from_bytes(image_bytes: bytes) -> dict:
    try:
        with Image.open(io.BytesIO(image_bytes)) as image:
            return ocr_image(image)

    except Exception as exc:
        return {
            "text": "",
            "status": "error",
            "error": str(exc),
        }