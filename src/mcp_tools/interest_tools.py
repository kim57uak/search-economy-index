"""
금리 및 채권 관련 MCP 도구들
"""
from typing import Dict, Any
from core.service_manager import service_manager


def register_interest_tools(mcp):
    """금리 및 채권 관련 도구들을 MCP 서버에 등록"""
    
    @mcp.tool(description="Get Korean interest rates including base rate, CD rate, and call rate")
    def get_interest_rates() -> Dict[str, Any]:
        try:
            result = service_manager.get_interest_rates()
            return {"interest_rates": result}
        except Exception as e:
            return {"error": str(e)}

    @mcp.tool(description="Get Korean government bond yields and treasury securities information")
    def get_bond_yields() -> Dict[str, Any]:
        try:
            result = service_manager.get_bond_yields()
            return {"bond_yields": result}
        except Exception as e:
            return {"error": str(e)}

    @mcp.tool(description="Get Certificate of Deposit (CD) rates in Korean market")
    def get_cd_rates() -> Dict[str, Any]:
        try:
            result = service_manager.get_cd_rates()
            return {"cd_rates": result}
        except Exception as e:
            return {"error": str(e)}

    @mcp.tool(description="Get corporate bond yields and credit spreads information")
    def get_corporate_bonds() -> Dict[str, Any]:
        try:
            result = service_manager.get_corporate_bonds()
            return {"corporate_bonds": result}
        except Exception as e:
            return {"error": str(e)}