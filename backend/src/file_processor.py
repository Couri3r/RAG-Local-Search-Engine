import os
import re
import csv
import PyPDF2
from typing import Iterator, Tuple


try:
    import textract
except ImportError:
    textract = None

def clean_text(text: str) -> str:
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_text_from_txt(filepath: str) -> str:
    with open(filepath,"r", encoding="utf-8", errors="ignore") as f:
        return f.read()
    

def extract_text_from_pdf(filepath: str) -> str:
    text =[]

    with open(filepath, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        if reader.is_encrypted:
            try:
                reader.decrypt('')
            except Exception:
                return f"[Skipping encrypted PDF: {os.path.basename(filepath)}]"
        for page in reader.pages:
            text.append(page.extract_text() or "")
    return " ".join(text)

def extract_text_from_csv(filepath: str) -> str:
    with open (filepath, "r", encoding="utf-8", errors="ignore") as f:
        return f.read().replace("\n", " ").replace(","," ")
    

def extract_text_from_doc(filepath:str) -> str:
    if not textract:
        raise ImportError("textract is required.")
    return textract.process(filepath).decode("utf-8",errors="ignore")

FILE_HANDLERS = {
    ".txt": extract_text_from_txt,
    ".pdf": extract_text_from_pdf,
    ".csv": extract_text_from_csv,
    ".doc": extract_text_from_doc,
    ".docx": extract_text_from_doc,
}



def extract_text(filepath: str) -> str:
    ext = os.path.splitext(filepath)[1].lower()
    handler = FILE_HANDLERS.get(ext)

    if not handler:
        return f"[INFO] Skipping unsupported file type:{ext}"

    try:
        return clean_text(handler(filepath))
    except ImportError as e:
        return f"[WARN] Missing dependancy for {ext}: {e}"
    except Exception as e:
        return f"[ERROR] Could not read {filepath}: {e}"
    

def process_directory(directory: str) -> Iterator[Tuple[str, str]]:

    for root, _, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            text = extract_text(filepath)

            if not text.startswith("[INFO]") and not text.startswith("[ERROR]"):
                yield filepath, text



if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="process files")
    parser.add_argument("directory", help="Path to directory")
    args = parser.parse_args()

    print(f"Scanning directory: {args.directory}")
    for path, text in process_directory(args.directory):
        print(f"\n--- {path} ---\n{text[:500]}...")


