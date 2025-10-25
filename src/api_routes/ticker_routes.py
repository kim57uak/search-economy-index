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

@router.post("/multiple-overseas-quotes")
def get_multiple_overseas_quotes(symbols: list) -> Dict[str, Any]:
    """복수 해외 주식 정보 조회"""
    try:
        from core.service_manager import service_manager
        result = service_manager.get_multiple_stock_quotes(symbols)
        return {
            "symbols": symbols,
            "quotes": result
        }
    except Exception as e:
        return {"error": str(e)}

@router.post("/multiple-domestic-quotes")
def get_multiple_domestic_quotes(tickers: list) -> Dict[str, Any]:
    """복수 국내 주식 정보 조회"""
    try:
        from core.service_manager import service_manager
        result = service_manager.get_multiple_domestic_stock_quotes(tickers)
        return {
            "tickers": tickers,
            "quotes": result
        }
    except Exception as e:
        return {"error": str(e)}

@router.post("/multiple-crypto-quotes")
def get_multiple_crypto_quotes(symbols: list) -> Dict[str, Any]:
    """복수 암호화폐 정보 조회"""
    try:
        from core.service_manager import service_manager
        result = service_manager.get_multiple_crypto_quotes(symbols)
        return {
            "symbols": symbols,
            "quotes": result
        }
    except Exception as e:
        return {"error": str(e)}