#!/usr/bin/env python3
"""
간단한 HTTP 서버로 MCP 기능 테스트
"""
import sys
import os
from fastapi import FastAPI
from typing import Dict, Any

# src 디렉토리를 Python 경로에 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from ticker_parser import TickerParser
from fnguide_parser import FnGuideParser

app = FastAPI(title="Search Economy Index API")

# 파서 인스턴스
ticker_parser = TickerParser()
fnguide_parser = FnGuideParser()

@app.get("/")
def root():
    return {"message": "Search Economy Index API"}

@app.get("/search/domestic/{query}")
def search_domestic(query: str) -> Dict[str, Any]:
    try:
        result = ticker_parser.search_ticker(query)
        return {
            "query": query,
            "domestic_tickers": result["domestic"],
            "earnings": result["earnings"],
            "disclosure": result["disclosure"]
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/search/overseas/{query}")
def search_overseas(query: str) -> Dict[str, Any]:
    try:
        result = ticker_parser.search_ticker(query)
        return {
            "query": query,
            "overseas_tickers": result["overseas"],
            "other": result["other"]
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/fnguide/snapshot/{ticker}")
def get_snapshot(ticker: str) -> Dict[str, Any]:
    try:
        result = fnguide_parser.get_snapshot(ticker)
        return {"ticker": ticker, "snapshot": result}
    except Exception as e:
        return {"error": str(e)}

@app.get("/fnguide/overview/{ticker}")
def get_overview(ticker: str) -> Dict[str, Any]:
    try:
        result = fnguide_parser.get_company_overview(ticker)
        return {"ticker": ticker, "company_overview": result}
    except Exception as e:
        return {"error": str(e)}

@app.get("/fnguide/financials/{ticker}")
def get_financials(ticker: str) -> Dict[str, Any]:
    try:
        result = fnguide_parser.get_financial_statement(ticker)
        return {"ticker": ticker, "financial_statements": result}
    except Exception as e:
        return {"error": str(e)}

@app.get("/fnguide/ratios/{ticker}")
def get_ratios(ticker: str) -> Dict[str, Any]:
    try:
        result = fnguide_parser.get_financial_ratio(ticker)
        return {"ticker": ticker, "financial_ratios": result}
    except Exception as e:
        return {"error": str(e)}

@app.get("/fnguide/indicators/{ticker}")
def get_indicators(ticker: str) -> Dict[str, Any]:
    try:
        result = fnguide_parser.get_investment_indicator(ticker)
        return {"ticker": ticker, "investment_indicators": result}
    except Exception as e:
        return {"error": str(e)}

@app.get("/fnguide/consensus/{ticker}")
def get_consensus(ticker: str) -> Dict[str, Any]:
    try:
        result = fnguide_parser.get_consensus(ticker)
        return {"ticker": ticker, "analyst_consensus": result}
    except Exception as e:
        return {"error": str(e)}

@app.get("/fnguide/ownership/{ticker}")
def get_ownership(ticker: str) -> Dict[str, Any]:
    try:
        result = fnguide_parser.get_share_analysis(ticker)
        return {"ticker": ticker, "ownership_analysis": result}
    except Exception as e:
        return {"error": str(e)}

@app.get("/fnguide/industry/{ticker}")
def get_industry(ticker: str) -> Dict[str, Any]:
    try:
        result = fnguide_parser.get_industry_analysis(ticker)
        return {"ticker": ticker, "industry_analysis": result}
    except Exception as e:
        return {"error": str(e)}

@app.get("/fnguide/competitors/{ticker}")
def get_competitors(ticker: str) -> Dict[str, Any]:
    try:
        result = fnguide_parser.get_competitor_comparison(ticker)
        return {"ticker": ticker, "competitor_comparison": result}
    except Exception as e:
        return {"error": str(e)}

@app.get("/fnguide/disclosures/{ticker}")
def get_disclosures(ticker: str) -> Dict[str, Any]:
    try:
        result = fnguide_parser.get_disclosure(ticker)
        return {"ticker": ticker, "exchange_disclosures": result}
    except Exception as e:
        return {"error": str(e)}

@app.get("/fnguide/earnings/{ticker}")
def get_earnings(ticker: str) -> Dict[str, Any]:
    try:
        result = fnguide_parser.get_earnings_report(ticker)
        return {"ticker": ticker, "earnings_reports": result}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)