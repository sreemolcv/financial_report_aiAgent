import shutil
import os

from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

from src.config import CHROMA_DB_DIR
from src.embeddings import get_embedding_function

def build_vectorstore(chunks: list[Document],collection_name:str="financila_reports") -> Chroma:
    if os.path.exists(CHROMA_DB_DIR):
        shutil.rmtree(CHROMA_DB_DIR)
    os.makedirs(CHROMA_DB_DIR,exist_ok=True)

    embedding_fn = get_embedding_function()
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding = embedding_fn,
        collection_name=collection_name,
        persist_directory=CHROMA_DB_DIR,
    )
    return vectorstore
def load_vectorstore(collection_name:str="financial_reports") -> Chroma:
    embedding_fn = get_embedding_function()
    return Chroma(
        collection_name=collection_name,
        embedding_function=embedding_fn,
        persist_directory=CHROMA_DB_DIR,
    )