from langchain_community.embeddings import HuggingFaceEmbeddings
from src.config import EMBEDDING_MODEL_NAME


def get_embedding_function() -> HuggingFaceEmbeddings:
    return HuggingFaceEmbeddings(
        model_name = EMBEDDING_MODEL_NAME,
        model_kwargs={"device":"cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )