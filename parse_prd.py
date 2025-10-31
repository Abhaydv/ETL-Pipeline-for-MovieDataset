"""
Simple PDF -> text extractor for the PRD file in the repo.
Writes extracted text to `prd_extracted.md` and prints a short summary.
"""
import os
from pathlib import Path

from PyPDF2 import PdfReader

PDF_NAME = "make prd document for ETL Pipeline for Movie Datas.pdf"
OUT_NAME = "prd_extracted.md"

p = Path(PDF_NAME)
if not p.exists():
    print(f"PDF not found at {p.resolve()}. Make sure the file is present in the repo root.")
    raise SystemExit(1)

reader = PdfReader(str(p))
all_text = []
for i, page in enumerate(reader.pages):
    text = page.extract_text() or ""
    all_text.append(text)

full = "\n\n".join(all_text)
with open(OUT_NAME, "w", encoding="utf-8") as f:
    f.write("# Extracted PRD Text\n\n")
    f.write(full)

print(f"✅ Extracted {len(reader.pages)} pages from '{PDF_NAME}' and wrote to '{OUT_NAME}'")
# Print first 800 chars as quick preview
preview = full.strip()[:800]
print("--- Preview ---\n")
print(preview)
print("\n--- End preview ---")
