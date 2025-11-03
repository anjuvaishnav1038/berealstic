from PIL import Image
import pytesseract
import os

def extract_text_from_image(image_path: str) -> str:
    """
    Extract text from an image file using Tesseract OCR.
    Supports PNG, JPG, JPEG.
    """
    try:
        if not os.path.exists(image_path):
            return ""
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return text.strip()
    except Exception as e:
        print(f"OCR error for {image_path}: {e}")
        return ""
