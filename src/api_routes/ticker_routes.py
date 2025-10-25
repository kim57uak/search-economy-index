"""
티커 검색 관련 API 라우트
"""
from fastapi import APIRouter
from typing import Dict, Any
from parsers.ticker_parser import TickerParser

router = APIRouter(prefix="/search", tags=["ticker"])
ticker_parser = TickerParser()

@router.get("/domestic/{query}")
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

@router.get("/overseas/{query}")
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