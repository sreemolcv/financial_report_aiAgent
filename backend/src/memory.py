from langchain.memory import ConversationBufferMemory

def get_memory() -> ConversationBufferMemory:
    return ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="output",
    )