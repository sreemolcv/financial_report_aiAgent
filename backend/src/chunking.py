from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from src.config import CHUNK_SIZE, CHUNK_OVERLAP

def split_documents(documents:list[Document]) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = CHUNK_SIZE,
        chunk_overlap = CHUNK_OVERLAP,
        separators=["\n\n","\n","."," ",""],
    )
    chunks = splitter.split_documents(documents)

    for i, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = i
    return chunks

if __name__=="__main__":
    from src.pdf_loader import pdf_to_documents

    docs = pdf_to_documents("reports/meta_q1_2024.pdf")
    chunks = split_documents(docs)
    print(f"Cerated {len(chunks)} chunks from {len(docs)} pages.")
    print(chunks[0])