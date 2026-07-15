
from langchain_community.vectorstores import Chroma

def get_retriever(vectorstore:Chroma,k:int=5):
    
    return vectorstore.as_retriever(search_type="similarity",search_kwargs={"k":k})

def retrieve_context(vectorstore:Chroma,query:str,k:int=5) -> str:

    retriever = get_retriever(vectorstore,k=k)
    docs = retriever.invoke(query)

    if not docs:
        return "No relevant information found in the report. "
    
    formatted_chunks = []
    for d in docs:
        page = d.metadata.get("page","?")
        source = d.metadata.get("source","report")
        formatted_chunks.append(f"[Source:{source}, Page {page}]\n{d.page_content}")
    return "\n\n ---\n\n".join(formatted_chunks)
