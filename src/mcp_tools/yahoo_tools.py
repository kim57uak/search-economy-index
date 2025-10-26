"""
Yahoo Finance 글로벌 데이터 관련 MCP 도구들
"""
from typing import Dict, Any
from core.service_manager import service_manager


def register_yahoo_tools(mcp):
    """Yahoo Finance 관련 도구들을 MCP 서버에 등록"""
    
    @mcp.tool(description="Get global major stock indices from Yahoo Finance (S&P500, Dow Jones, NASDAQ, etc.)")
    def get_global_indices() -> Dict[str, Any]:
        try:
            result = service_manager.get_global_indices()
            return {"global_indices": result}
        except Exception as e:
            return {"error": str(e)}

    @mcp.tool(description="Get US Treasury bond yields and rates from Yahoo Finance")
    def get_us_treasury_yields() -> Dict[str, Any]:
        try:
            result = service_manager.get_us_treasury_yields()
            return {"us_treasury_yields": result}
        except Exception as e:
            return {"error": str(e)}

    @mcp.tool(description="Get VIX volatility index (fear index) from Yahoo Finance")
    def get_vix_data() -> Dict[str, Any]:
        try:
            result = service_manager.get_vix_data()
            return {"vix_data": result}
        except Exception as e:
            return {"error": str(e)}

    @mcp.tool(description="Get global commodities prices (gold, oil, copper, etc.) from Yahoo Finance")
    def get_commodities() -> Dict[str, Any]:
        try:
            result = service_manager.get_commodities()
            return {"commodities": result}
        except Exception as e:
            return {"error": str(e)}

    @mcp.tool(description="Get major forex currency pairs (EUR/USD, GBP/USD, etc.) from Yahoo Finance")
    def get_forex_majors() -> Dict[str, Any]:
        try:
            result = service_manager.get_forex_majors()
            return {"forex_majors": result}
        except Exception as e:
            return {"error": str(e)}

    @mcp.tool(description="Get Asian major stock indices (Nikkei, Hang Seng, Shanghai, etc.) from Yahoo Finance")
    def get_asian_indices() -> Dict[str, Any]:
        try:
            result = service_manager.get_asian_indices()
            return {"asian_indices": result}
        except Exception as e:
            return {"error": str(e)}

    @mcp.tool(description="Get European major stock indices (FTSE, DAX, CAC40, etc.) from Yahoo Finance")
    def get_european_indices() -> Dict[str, Any]:
        try:
            result = service_manager.get_european_indices()
            return {"european_indices": result}
        except Exception as e:
            return {"error": str(e)}

    @mcp.tool(description="Get sector performance data from Yahoo Finance")
    def get_yahoo_sector_performance() -> Dict[str, Any]:
        try:
            result = service_manager.get_yahoo_sector_performance()
            return {"sector_performance": result}
        except Exception as e:
            return {"error": str(e)}

    # @mcp.tool(description="Get individual stock quote from Yahoo Finance (US/Global stocks). For multiple stocks, use get_multiple_stock_quotes instead.")
    # def get_stock_quote(symbol: str) -> Dict[str, Any]:
    #     try:
    #         result = service_manager.get_stock_quote(symbol)
    #         return {"stock_quote": result}
    #     except Exception as e:
    #         return {"error": str(e)}

    # @mcp.tool(description="Get individual Korean domestic stock quote from Naver Finance. For multiple stocks, use get_multiple_domestic_stock_quotes instead.")
    # def get_domestic_stock_quote(ticker: str) -> Dict[str, Any]:
    #     try:
    #         result = service_manager.get_domestic_stock_quote(ticker)
    #         return {"domestic_stock_quote": result}
    #     except Exception as e:
    #         return {"error": str(e)}

    # @mcp.tool(description="Get individual cryptocurrency price from Yahoo Finance (e.g., BTC, ETH). For multiple cryptos, use get_multiple_crypto_quotes instead.")
    # def get_crypto_quote(symbol: str) -> Dict[str, Any]:
    #     try:
    #         result = service_manager.get_crypto_quote(symbol)
    #         return {"crypto_quote": result}
    #     except Exception as e:
    #         return {"error": str(e)}

    @mcp.tool(description="Get multiple overseas stock quotes from Yahoo Finance. Provide list of symbols like ['AAPL', 'TSLA', 'MSFT'].")
    def get_multiple_stock_quotes(symbols: list) -> Dict[str, Any]:
        try:
            result = service_manager.get_multiple_stock_quotes(symbols)
            return {"multiple_stock_quotes": result}
        except Exception as e:
            return {"error": str(e)}

    @mcp.tool(description="Get multiple Korean domestic stock quotes from Naver Finance. Provide list of tickers like ['005930', '000660', '035420'].")
    def get_multiple_domestic_stock_quotes(tickers: list) -> Dict[str, Any]:
        try:
            result = service_manager.get_multiple_domestic_stock_quotes(tickers)
            return {"multiple_domestic_stock_quotes": result}
        except Exception as e:
            return {"error": str(e)}

    @mcp.tool(description="Get multiple cryptocurrency quotes from Yahoo Finance. Provide list of symbols like ['BTC-USD', 'ETH-USD', 'ADA-USD'].")
    def get_multiple_crypto_quotes(symbols: list) -> Dict[str, Any]:
        try:
            result = service_manager.get_multiple_crypto_quotes(symbols)
            return {"multiple_crypto_quotes": result}
        except Exception as e:
            return {"error": str(e)}

    @mcp.tool(description="Get overseas stock disclosure information from Yahoo Finance and SEC filings. Provide stock symbol (e.g., 'AAPL', 'TSLA').")
    def get_overseas_disclosures(symbol: str) -> Dict[str, Any]:
        try:
            result = service_manager.get_overseas_disclosures(symbol)
            return {"symbol": symbol, "overseas_disclosures": result}
        except Exception as e:
            return {"error": str(e)}