"""
FnGuide 분석 관련 MCP 도구들
"""
from typing import Dict, Any
from core.service_manager import service_manager

def register_fnguide_tools(mcp):
    """FnGuide 분석 관련 도구들을 MCP 서버에 등록"""
    
    @mcp.tool(description="Get comprehensive Korean domestic stock snapshot with price, volume, and key metrics")
    def get_stock_snapshot(ticker: str) -> Dict[str, Any]:
        try:
            result = service_manager.get_stock_snapshot(ticker)
            return {"ticker": ticker, "snapshot": result}
        except Exception as e:
            return {"error": str(e)}

    @mcp.tool(description="Get detailed Korean company overview and business information")
    def get_company_overview(ticker: str) -> Dict[str, Any]:
        try:
            result = service_manager.get_company_overview(ticker)
            return {"ticker": ticker, "company_overview": result}
        except Exception as e:
            return {"error": str(e)}

    @mcp.tool(description="Get Korean company financial statements including income statement, balance sheet, and cash flow")
    def get_financial_statements(ticker: str) -> Dict[str, Any]:
        try:
            result = service_manager.get_financial_statements(ticker)
            return {"ticker": ticker, "financial_statements": result}
        except Exception as e:
            return {"error": str(e)}

    @mcp.tool(description="Get key financial ratios and metrics for Korean stock analysis")
    def get_financial_ratios(ticker: str) -> Dict[str, Any]:
        try:
            result = service_manager.get_financial_ratios(ticker)
            return {"ticker": ticker, "financial_ratios": result}
        except Exception as e:
            return {"error": str(e)}

    @mcp.tool(description="Get Korean stock investment indicators and valuation metrics like P/E, P/B ratios")
    def get_investment_indicators(ticker: str) -> Dict[str, Any]:
        try:
            result = service_manager.get_investment_indicators(ticker)
            return {"ticker": ticker, "investment_indicators": result}
        except Exception as e:
            return {"error": str(e)}

    @mcp.tool(description="Get Korean stock analyst consensus, ratings, and price targets")
    def get_analyst_consensus(ticker: str) -> Dict[str, Any]:
        try:
            result = service_manager.get_analyst_consensus(ticker)
            return {"ticker": ticker, "analyst_consensus": result}
        except Exception as e:
            return {"error": str(e)}

    @mcp.tool(description="Get Korean company shareholding structure and ownership analysis")
    def get_ownership_analysis(ticker: str) -> Dict[str, Any]:
        try:
            result = service_manager.get_ownership_analysis(ticker)
            return {"ticker": ticker, "ownership_analysis": result}
        except Exception as e:
            return {"error": str(e)}

    @mcp.tool(description="Get Korean industry sector analysis and trends comparison")
    def get_industry_analysis(ticker: str) -> Dict[str, Any]:
        try:
            result = service_manager.get_industry_analysis(ticker)
            return {"ticker": ticker, "industry_analysis": result}
        except Exception as e:
            return {"error": str(e)}

    @mcp.tool(description="Get Korean company competitor comparison and peer analysis")
    def get_competitor_comparison(ticker: str) -> Dict[str, Any]:
        try:
            result = service_manager.get_competitor_comparison(ticker)
            return {"ticker": ticker, "competitor_comparison": result}
        except Exception as e:
            return {"error": str(e)}

    @mcp.tool(description="Get Korean stock exchange disclosures and regulatory filings")
    def get_exchange_disclosures(ticker: str) -> Dict[str, Any]:
        try:
            result = service_manager.get_exchange_disclosures(ticker)
            return {"ticker": ticker, "exchange_disclosures": result}
        except Exception as e:
            return {"error": str(e)}

    @mcp.tool(description="Get latest Korean company earnings reports and financial results")
    def get_earnings_reports(ticker: str) -> Dict[str, Any]:
        try:
            result = service_manager.get_earnings_reports(ticker)
            return {"ticker": ticker, "earnings_reports": result}
        except Exception as e:
            return {"error": str(e)}