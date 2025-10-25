"""
시장 지표 관련 MCP 도구들
"""
from typing import Dict, Any
from core.service_manager import service_manager


def register_market_tools(mcp):
    """시장 지표 관련 도구들을 MCP 서버에 등록"""
    
    @mcp.tool(description="Get major Korean stock market indices (KOSPI, KOSDAQ, KOSPI200)")
    def get_market_indices() -> Dict[str, Any]:
        try:
            result = service_manager.get_market_indices()
            return {"market_indices": result}
        except Exception as e:
            return {"error": str(e)}

    @mcp.tool(description="Get sector performance and industry group rankings")
    def get_sector_performance() -> Dict[str, Any]:
        try:
            result = service_manager.get_sector_performance()
            return {"sector_performance": result}
        except Exception as e:
            return {"error": str(e)}

    @mcp.tool(description="Get top gaining stocks with highest price increases")
    def get_top_gainers() -> Dict[str, Any]:
        try:
            result = service_manager.get_top_gainers()
            return {"top_gainers": result}
        except Exception as e:
            return {"error": str(e)}

    @mcp.tool(description="Get top losing stocks with highest price decreases")
    def get_top_losers() -> Dict[str, Any]:
        try:
            result = service_manager.get_top_losers()
            return {"top_losers": result}
        except Exception as e:
            return {"error": str(e)}

    @mcp.tool(description="Get stocks with highest trading volume")
    def get_volume_leaders() -> Dict[str, Any]:
        try:
            result = service_manager.get_volume_leaders()
            return {"volume_leaders": result}
        except Exception as e:
            return {"error": str(e)}