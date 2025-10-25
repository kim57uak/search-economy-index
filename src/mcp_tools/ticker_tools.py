"""
티커 검색 관련 MCP 도구들
"""
import logging
from typing import Dict, Any
from core.service_manager import service_manager

logger = logging.getLogger(__name__)

def register_ticker_tools(mcp):
    """티커 검색 관련 도구들을 MCP 서버에 등록"""
    
    @mcp.tool(description="Search for Korean domestic stock ticker information from Naver Finance")
    def search_domestic_ticker(query: str) -> Dict[str, Any]:
        try:
            logger.info(f"국내 티커 검색: {query}")
            result = service_manager.search_domestic_ticker(query)
            return {
                "query": query,
                "domestic_tickers": result
            }
        except Exception as e:
            logger.error(f"국내 티커 검색 실패: {e}")
            return {"error": str(e)}

    @mcp.tool(description="Search for international/overseas stock ticker information from Naver Finance")
    def search_overseas_ticker(query: str) -> Dict[str, Any]:
        try:
            logger.info(f"해외 티커 검색: {query}")
            result = service_manager.search_overseas_ticker(query)
            return {
                "query": query,
                "overseas_tickers": result
            }
        except Exception as e:
            logger.error(f"해외 티커 검색 실패: {e}")
            return {"error": str(e)}