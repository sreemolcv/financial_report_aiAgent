from langchain.agents import create_tool_calling_agent, AgentExecutor

from src.pdf_loader import pdf_to_documents
from src.chunking import split_documents
from src.vectorstore import build_vectorstore
from src.llm import get_llm
from src.prompt import build_agent_prompt
from src.memory import get_memory
from src.tools import get_all_tools,set_vectorstore
from src.utils import timed

class FinancialReportAgent:
    def __init__(self):
        self.llm = get_llm()
        self.tools = get_all_tools()
        self.prompt = build_agent_prompt()
        self.memory = get_memory()
        self.vectorstore = None
        self.executor: AgentExecutor | None = None
        self._report_loaded = False
    @timed("PDF processing + indexing")
    def load_report(self,pdf_path:str) -> int:
        """
        Process a PDF report: extract text, chunk it, embed it, and
        build the vector store. Must be called before ask().

        Returns:
            Number of chunks indexed.
        """
        documents = pdf_to_documents(pdf_path)
        chunks = split_documents(documents)
        self.vectorstore = build_vectorstore(chunks)
        set_vectorstore(self.vectorstore)
        agent = create_tool_calling_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt
        )
        self.executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            memory=self.memory,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=8,
        )
        self._report_loaded = True
        return len(chunks)
    
    def ask(self,question:str) -> str:
        """
        Ask the agent a question about the currently loaded report.

        Args:
            question: Natural language question.

        Returns:
            The agent's answer as a string.
        """
        if not self._report_loaded or self.executor is None:
            raise RuntimeError("No report loaded. Call load_report(pdf_path) first. ")
        
        result = self.executor.invoke({"input": question})
        return result["output"]
    def reset_memory(self):
        """Clear conversation history while keeping the loaded report."""
        self.memory.clear()


if __name__ == "__main__":
    agent = FinancialReportAgent()
    num_chunks = agent.load_report("reports/meta_q1_2024.pdf")
    print(f"Indexed {num_chunks} chunks.\n")
    print(agent.ask("summarize this report's overall financial performance."))
    print("\n---\n")
    print(agent.ask("What was total revenue, and hoe does it compare to the prior year?"))