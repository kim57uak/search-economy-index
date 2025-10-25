"""
환율 정보 관련 MCP 도구들
"""
from typing import Dict, Any
from parsers.exchange_parser import ExchangeParser

exchange_parser = ExchangeParser()

def register_exchange_tools(mcp):
    """환율 관련 도구들을 MCP 서버에 등록"""
    
    @mcp.tool(description="Get domestic exchange rates information")
    def get_domestic_exchange() -> Dict[str, Any]:
        try:
            result = exchange_parser.get_domestic_exchange()
            return {"domestic_exchange": result}
        except Exception as e:
            return {"error": str(e)}

    @mcp.tool(description="Get international market exchange rates information")
    def get_world_exchange() -> Dict[str, Any]:
        try:
            result = exchange_parser.get_world_exchange()
            return {"world_exchange": result}
        except Exception as e:
            return {"error": str(e)}