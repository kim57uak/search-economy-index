"""
FnGuide 분석 관련 API 라우트
"""
from fastapi import APIRouter
from typing import Dict, Any
from parsers.fnguide_parser import FnGuideParser

router = APIRouter(prefix="/fnguide", tags=["fnguide"])
fnguide_parser = FnGuideParser()

@router.get("/snapshot/{ticker}")
def get_snapshot(ticker: str) -> Dict[str, Any]:
    try:
        result = fnguide_parser.get_snapshot(ticker)
        return {"ticker": ticker, "snapshot": result}
    except Exception as e:
        return {"error": str(e)}

@router.get("/overview/{ticker}")
def get_overview(ticker: str) -> Dict[str, Any]:
    try:
        result = fnguide_parser.get_company_overview(ticker)
        return {"ticker": ticker, "company_overview": result}
    except Exception as e:
        return {"error": str(e)}

@router.get("/financials/{ticker}")
def get_financials(ticker: str) -> Dict[str, Any]:
    try:
        result = fnguide_parser.get_financial_statement(ticker)
        return {"ticker": ticker, "financial_statements": result}
    except Exception as e:
        return {"error": str(e)}

@router.get("/ratios/{ticker}")
def get_ratios(ticker: str) -> Dict[str, Any]:
    try:
        result = fnguide_parser.get_financial_ratio(ticker)
        return {"ticker": ticker, "financial_ratios": result}
    except Exception as e:
        return {"error": str(e)}

@router.get("/indicators/{ticker}")
def get_indicators(ticker: str) -> Dict[str, Any]:
    try:
        result = fnguide_parser.get_investment_indicator(ticker)
        return {"ticker": ticker, "investment_indicators": result}
    except Exception as e:
        return {"error": str(e)}

@router.get("/consensus/{ticker}")
def get_consensus(ticker: str) -> Dict[str, Any]:
    try:
        result = fnguide_parser.get_consensus(ticker)
        return {"ticker": ticker, "analyst_consensus": result}
    except Exception as e:
        return {"error": str(e)}

@router.get("/ownership/{ticker}")
def get_ownership(ticker: str) -> Dict[str, Any]:
    try:
        result = fnguide_parser.get_share_analysis(ticker)
        return {"ticker": ticker, "ownership_analysis": result}
    except Exception as e:
        return {"error": str(e)}

@router.get("/industry/{ticker}")
def get_industry(ticker: str) -> Dict[str, Any]:
    try:
        result = fnguide_parser.get_industry_analysis(ticker)
        return {"ticker": ticker, "industry_analysis": result}
    except Exception as e:
        return {"error": str(e)}

@router.get("/competitors/{ticker}")
def get_competitors(ticker: str) -> Dict[str, Any]:
    try:
        result = fnguide_parser.get_competitor_comparison(ticker)
        return {"ticker": ticker, "competitor_comparison": result}
    except Exception as e:
        return {"error": str(e)}

@router.get("/disclosures/{ticker}")
def get_disclosures(ticker: str) -> Dict[str, Any]:
    try:
        result = fnguide_parser.get_disclosure(ticker)
        return {"ticker": ticker, "exchange_disclosures": result}
    except Exception as e:
        return {"error": str(e)}

@router.get("/earnings/{ticker}")
def get_earnings(ticker: str) -> Dict[str, Any]:
    try:
        result = fnguide_parser.get_earnings_report(ticker)
        return {"ticker": ticker, "earnings_reports": result}
    except Exception as e:
        return {"error": str(e)}