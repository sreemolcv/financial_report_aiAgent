import os
import fitz  # PyMuPDF
from langchain_core.documents import Document

from src.config import DATA_DIR



def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extracts text from a PDF file.

    Args:
        pdf_path (str): The path to the PDF file.
    returns:
        A list of dicts: [{"page": int, "text": str}, ...]
    """
    print("Current Working Directory:", os.getcwd())
    print("PDF Path:", pdf_path)
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF not found at:{pdf_path}")
    
    pages_content = []
    with fitz.open(pdf_path) as doc:
        for page_num, page in enumerate(doc,start=1):
            text = page.get_text()
            if text:
                pages_content.append({"page":page_num, "text": text})
    if not pages_content:
        raise ValueError(
            "No extractable text found in PDF. It may be a scanned/image-only "
            "document that requires OCR."
        )
    return pages_content

def save_extracted_text(pages_content:list[dict],filename:str="extracted_text.txt")-> str:
    out_path = os.path.join(DATA_DIR,filename)
    with open(out_path,"w", encoding="utf-8") as f:
        for p in pages_content:
            f.write(f"\n--- Page {p['page']} ---\n")
            f.write(p["text"])
    return out_path

def pdf_to_documents(pdf_path:str)->list[Document]:
    pages_content = extract_text_from_pdf(pdf_path)
    save_extracted_text(pages_content)

    source_name = os.path.basename(pdf_path)
    docuemts = [
        Document(
            page_content=p["text"],
            metadata={"source": source_name, "page": p["page"]},
        )
        for p in pages_content
    ]
    return docuemts

if __name__== "__main__":
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else "reports/meta_q1_2024.pdf"
    docs = pdf_to_documents(path)
    print(f"Extracted {len(docs)} pages. First page preview:\n")
    print(docs[0].page_content[:500])
    
