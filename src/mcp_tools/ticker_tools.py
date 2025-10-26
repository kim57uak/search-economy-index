"""
티커 검색 관련 MCP 도구들
"""

import logging
from typing import Dict, Any
from core.service_manager import service_manager

logger = logging.getLogger(__name__)


def register_ticker_tools(mcp):
    """티커 검색 관련 도구들을 MCP 서버에 등록"""

    # @mcp.tool(
    #     description="Search for Korean domestic stock ticker information from Naver Finance"
    # )
    # def search_domestic_ticker(query: str) -> Dict[str, Any]:
    #     try:
    #         logger.info(f"국내 티커 검색: {query}")
    #         result = service_manager.search_domestic_ticker(query)
    #         return {"query": query, "domestic_tickers": result}
    #     except Exception as e:
    #         logger.error(f"국내 티커 검색 실패: {e}")
    #         return {"error": str(e)}

    # @mcp.tool(
    #     description="Search for international/overseas stock ticker information from Yahoo Finance. Use English company names for best results (e.g., 'Apple' instead of '애플', 'Tesla' instead of '테슬라')."
    # )
    # def search_overseas_ticker(query: str) -> Dict[str, Any]:
    #     try:
    #         logger.info(f"해외 티커 검색: {query}")
    #         result = service_manager.search_overseas_ticker(query)
    #         return {"query": query, "overseas_tickers": result}
    #     except Exception as e:
    #         logger.error(f"해외 티커 검색 실패: {e}")
    #         return {"error": str(e)}

    # @mcp.tool(
    #     description="Search cryptocurrency ticker symbols from CoinGecko. For prices, use get_crypto_quote."
    # )
    # def search_crypto_ticker(query: str) -> Dict[str, Any]:
    #     try:
    #         logger.info(f"암호화폐 티커 검색: {query}")
    #         result = service_manager.search_crypto_ticker(query)
    #         return {"query": query, "crypto_tickers": result}
    #     except Exception as e:
    #         logger.error(f"암호화폐 티커 검색 실패: {e}")
    #         return {"error": str(e)}

    @mcp.tool(
        description="Get top cryptocurrencies by market cap. Source: CoinGecko API (must cite). Currency: krw (default) or usd"
    )
    def get_top_cryptos(limit: int = 20, currency: str = 'krw') -> Dict[str, Any]:
        try:
            logger.info(f"상위 암호화폐 조회: {limit}개, 통화: {currency}")
            result = service_manager.get_top_cryptos(limit, currency)
            return {"limit": limit, "currency": currency, "top_cryptos": result}
        except Exception as e:
            logger.error(f"상위 암호화폐 조회 실패: {e}")
            return {"error": str(e)}

    @mcp.tool(
        description="Get multiple overseas stock quotes at once. Provide list like ['AAPL', 'TSLA', 'MSFT']"
    )
    def get_multiple_stock_quotes(symbols: list) -> Dict[str, Any]:
        try:
            logger.info(f"복수 해외 주식 조회: {symbols}")
            result = service_manager.get_multiple_stock_quotes(symbols)
            return {"symbols": symbols, "quotes": result}
        except Exception as e:
            logger.error(f"복수 해외 주식 조회 실패: {e}")
            return {"error": str(e)}

    @mcp.tool(
        description="Get multiple Korean stock quotes at once. Provide list like ['005930', '000660', '035420']"
    )
    def get_multiple_domestic_stock_quotes(tickers: list) -> Dict[str, Any]:
        try:
            logger.info(f"복수 국내 주식 조회: {tickers}")
            result = service_manager.get_multiple_domestic_stock_quotes(tickers)
            return {"tickers": tickers, "quotes": result}
        except Exception as e:
            logger.error(f"복수 국내 주식 조회 실패: {e}")
            return {"error": str(e)}

    @mcp.tool(
        description="Get multiple cryptocurrency quotes at once. Provide list like ['BTC-KRW', 'ETH-KRW', 'ADA-KRW']"
    )
    def get_multiple_crypto_quotes(symbols: list) -> Dict[str, Any]:
        try:
            logger.info(f"복수 암호화폐 조회: {symbols}")
            result = service_manager.get_multiple_crypto_quotes(symbols)
            return {"symbols": symbols, "quotes": result}
        except Exception as e:
            logger.error(f"복수 암호화폐 조회 실패: {e}")
            return {"error": str(e)}
