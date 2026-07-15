import os
from langchain_core.prompts import ChatPromptTemplate , MessagesPlaceholder

from src.config import TEMPLATES_DIR

def load_system_prompt() -> str:
    path = os.path.join(TEMPLATES_DIR,"financial_prompt.txt")
    with open(path, "r" , encoding="utf-8") as f:
        return f.read()

def build_agent_prompt() -> ChatPromptTemplate:
    system_prompt = load_system_prompt()
    return ChatPromptTemplate.from_messages(
        [
            ("system",system_prompt),
            MessagesPlaceholder(variable_name="chat_history",optional=True),
            ("human","{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )
