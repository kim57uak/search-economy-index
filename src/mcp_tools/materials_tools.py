"""
원자재 정보 관련 MCP 도구들
"""
from typing import Dict, Any
from parsers.materials_parser import MaterialsParser
from parsers.gold_parser import GoldParser

materials_parser = MaterialsParser()
gold_parser = GoldParser()

def register_materials_tools(mcp):
    """원자재 관련 도구들을 MCP 서버에 등록"""
    
    @mcp.tool(description="Get energy futures prices and information")
    def get_energy_futures() -> Dict[str, Any]:
        try:
            result = materials_parser.get_energy_futures()
            return {"energy_futures": result}
        except Exception as e:
            return {"error": str(e)}

    @mcp.tool(description="Get non-ferrous metals spot prices and information")
    def get_non_ferrous_metals() -> Dict[str, Any]:
        try:
            result = materials_parser.get_non_ferrous_metals()
            return {"non_ferrous_metals": result}
        except Exception as e:
            return {"error": str(e)}

    @mcp.tool(description="Get agriculture futures prices and information")
    def get_agriculture_futures() -> Dict[str, Any]:
        try:
            result = materials_parser.get_agriculture_futures()
            return {"agriculture_futures": result}
        except Exception as e:
            return {"error": str(e)}

    @mcp.tool(description="Get oil prices and petroleum market information")
    def get_oil_prices() -> Dict[str, Any]:
        try:
            result = gold_parser.get_oil_prices()
            return {"oil_prices": result}
        except Exception as e:
            return {"error": str(e)}

    @mcp.tool(description="Get precious metals prices and information")
    def get_precious_metals() -> Dict[str, Any]:
        try:
            result = gold_parser.get_precious_metals()
            return {"precious_metals": result}
        except Exception as e:
            return {"error": str(e)}