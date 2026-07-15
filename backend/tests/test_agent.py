"""
test_agent.py
-------------
Basic smoke tests. Requires a real GROQ_API_KEY in .env and a sample PDF
at reports/meta_q1_2024.pdf to run end-to-end (these are not pure unit
tests / do not use mocks, since the point is to validate the real pipeline).

Run with:
    pytest tests/test_agent.py -v
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest

from src.pdf_loader import pdf_to_documents
from src.chunking import split_documents

SAMPLE_PDF = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "reports",
    "meta_q1_2024.pdf",
)


def test_pdf_extraction_produces_documents():
    if not os.path.exists(SAMPLE_PDF):
        pytest.skip("Sample PDF not present in reports/. Add one to run this test.")
    docs = pdf_to_documents(SAMPLE_PDF)
    assert len(docs) > 0
    assert all(d.page_content.strip() for d in docs)
    assert all("page" in d.metadata for d in docs)


def test_chunking_splits_into_multiple_pieces():
    if not os.path.exists(SAMPLE_PDF):
        pytest.skip("Sample PDF not present in reports/. Add one to run this test.")
    docs = pdf_to_documents(SAMPLE_PDF)
    chunks = split_documents(docs)
    assert len(chunks) >= len(docs)
    assert all(c.metadata.get("chunk_id") is not None for c in chunks)


def test_agent_end_to_end():
    if not os.path.exists(SAMPLE_PDF):
        pytest.skip("Sample PDF not present in reports/. Add one to run this test.")
    if not os.getenv("GROQ_API_KEY"):
        pytest.skip("GROQ_API_KEY not set; skipping live LLM test.")

    from src.agent import FinancialReportAgent

    agent = FinancialReportAgent()
    num_chunks = agent.load_report(SAMPLE_PDF)
    assert num_chunks > 0

    answer = agent.ask("What is this report about?")
    assert isinstance(answer, str)
    assert len(answer) > 0
