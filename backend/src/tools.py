import re
import json

from langchain_core.tools import tool

from src.retriever import retrieve_context
from src.llm import get_llm

_VECTORSTORE = None

def set_vectorstore(vectorstore):
    global _VECTORSTORE
    _VECTORSTORE = vectorstore

def _require_vectorstore():
    if _VECTORSTORE is None:
        raise RuntimeError(
            "No report has been loaded yet. Process a PDF before querying."
        )
    return _VECTORSTORE

@tool
def search_report(query: str) -> str:
    """
    Search the loaded financial report for text relevant to the query.
    Use this for open-ended questions (e.g. "What did management say about
    the outlook for cloud revenue?"). Returns raw excerpts with page numbers.
    """
    vectorstore = _require_vectorstore()
    return retrieve_context(vectorstore, query, k=5)

@tool
def get_financial_metrics(metric_query: str) -> str:
    """
    Extract specific financial figures (e.g. "total revenue", "net income",
    "operating expenses", "EPS") from the report. Pass the metric name(s)
    you want as a plain string, e.g. "revenue and net income".
    Returns extracted figures with the source page, or notes if not found.
    """
    vectorstore = _require_vectorstore()
    context = retrieve_context(vectorstore,f"{metric_query} figures amount $", k=6)
    llm = get_llm()
    extraction_prompt = f""""extract the following financial metric(s) from the 
    contect below: {metric_query}
    Context:{context}
    intructions:
    - Report exact figures as they appear (with currency and units, e.g. "$36.46 billion").
    - Include the period they refer to (e.g. Q1 2024, prior-year quarter).
    - Include the page number cited in the context, in the form (Page N).
    - If a figure genuinely is not present in the context, say "Not found in retrieved context."
    - Be concise: a short bullet list is fine.
    """
    response = llm.invoke(extraction_prompt)
    return response.content

@tool
def detect_revenue_trend(period_description: str = "recent quaters") -> str:
    """
    Detect and quantify revenue trend/growth mentioned in the report
    (e.g. quarter-over-quarter or year-over-year change). Pass a short
    description of what comparison you want, e.g. "year over year" or
    "compared to Q4 2023". Returns the trend direction and % change if
    stated or computable from the retrieved figures.
    """
    vectorstore = _require_vectorstore()
    context = retrieve_context(
        vectorstore,
        f"revenue growth increase decrease compared {period_description}", k=6
    )

    llm = get_llm()
    trend_prompt = f"""Based on the context below from a financial report,
    identify the revenue trend for: {period_description}
    Context:{context}
    Instructions:
    - State the revenue figures being comapred and their periods.
    - Compute or report the precentage change (year-over-year or 
        quarter-over-quarter, whichever is supported by the context).
    - State clearly whether the trend is an increase, decrease, or flat.
    - Cite the page number(s) in the form (Page N).
    - If the context doesn't support a trend calculation, sy so explicitly.
    """
    response = llm.invoke(trend_prompt)
    return response.content

@tool
def summarize_report(focus_area: str = "overall financial performance") -> str:
    """
    Generate a structured executive summary of the report, optionally
    focused on a specific area (e.g. "profitability", "segment performance",
    "risk factors"). Use this for broad "summarize this report" requests.
    """
    vectorstore = _require_vectorstore()
    context = retrieve_context(vectorstore, focus_area,k=8)
    llm = get_llm()
    summary_prompt = f"""Summarize the following excerpts from a financial
    report, focused on: {focus_area}
    Context:{context}

    produce a structured summary with these sections:
    - Headline Numbers (revenue, Profit/loss, key metrics)
    - Notable Trends
    - Management Commentary / Outlook (if present)
    - Risks or Caveats (if present)

    Cite page numbers in parentheses where relevant. Keep it concise.
    """
    response = llm.invoke(summary_prompt)
    return response.content

def get_all_tools():
    """Returns the list of tools bound to the agent."""
    return [search_report,get_financial_metrics,detect_revenue_trend, summarize_report]