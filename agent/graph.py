from langchain.agents import create_agent
from langchain.tools import tool
from langchain_groq import ChatGroq

from mcp_server.tools.compute_metrics import get_delivery_kpis
from mcp_server.tools.root_cause import get_seller_risk_segments


# Wrap tools
@tool
def fetch_kpis():
    """Get overall delivery performance metrics"""
    return get_delivery_kpis()


@tool
def fetch_seller_risk():
    """Get seller-level risk analysis"""
    return get_seller_risk_segments()


#  LLM
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)


# CREATE AGENT (IMPORTANT: variable must be named 'agent')
agent = create_agent(
    model=llm,
    tools=[fetch_kpis, fetch_seller_risk],
    system_prompt="""
You are a senior data analyst.

Strict Rules:
- Do NOT mix metrics (percent vs time)
- Always identify whether the problem is SYSTEMIC or CONCENTRATED
- Prioritize severity over frequency
- Highlight extreme values (outliers)

Output format:

1. Key Insight
- Must clearly state if issue is concentrated or system-wide

2. Supporting Evidence
- Use correct metrics (%, days)
- Mention top 1-2 extreme sellers

3. Business Impact
- Focus on customer experience + operational risk

4. Recommendation
- Must be specific (not generic like “improve performance”)
"""
)