import pdfplumber
import fitz  # PyMuPDF
import camelot
import os
import json
import pandas as pd


def extract_text(pdf_path):
    """Extract text per page using pdfplumber"""
    text_pages = {}
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            text_pages[i] = page.extract_text() or ""
    return text_pages


def extract_tables(pdf_path):
    """Extract tables using Camelot and pdfplumber"""
    tables_pages = {}

    # Try Camelot (works only on vector PDFs)
    try:
        camelot_tables = camelot.read_pdf(pdf_path, pages="all", flavor="lattice")
        for t in camelot_tables:
            page_no = int(t.parsing_report["page"])
            if page_no not in tables_pages:
                tables_pages[page_no] = []
            tables_pages[page_no].append(t.df.to_dict(orient="list"))
    except Exception as e:
        print(f"Camelot failed: {e}")

    # Fallback with pdfplumber
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            try:
                tables = page.extract_tables()
                if tables:
                    if i not in tables_pages:
                        tables_pages[i] = []
                    for t in tables:
                        df = pd.DataFrame(t)
                        tables_pages[i].append(df.to_dict(orient="list"))
            except Exception:
                continue

    return tables_pages


def extract_images(pdf_path, out_dir="outputs/images"):
    """Extract images using PyMuPDF"""
    os.makedirs(out_dir, exist_ok=True)
    doc = fitz.open(pdf_path)
    image_refs = []
    for i, page in enumerate(doc, start=1):
        for img_index, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            pix = fitz.Pixmap(doc, xref)
            img_path = os.path.join(out_dir, f"page{i}_img{img_index}.png")
            if pix.n - pix.alpha < 4:  # RGB or Gray
                pix.save(img_path)
            else:  # CMYK: convert to RGB
                pix0 = fitz.Pixmap(fitz.csRGB, pix)
                pix0.save(img_path)
                pix0 = None
            image_refs.append({"page": i, "file": img_path})
    return image_refs


def pipeline(pdf_path, out_dir="outputs"):
    """Run the full extraction pipeline and save JSON output"""
    os.makedirs(out_dir, exist_ok=True)

    text = extract_text(pdf_path)
    tables = extract_tables(pdf_path)
    images = extract_images(pdf_path, os.path.join(out_dir, "images"))

    result = {
        "pdf": pdf_path,
        "text": text,
        "tables": tables,
        "images": images,
    }

    out_file = os.path.join(out_dir, os.path.basename(pdf_path) + ".json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    return result
