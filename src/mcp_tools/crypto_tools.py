"""
암호화폐 관련 MCP 도구들
"""
from core.service_manager import service_manager


def register_crypto_tools(mcp):
    """암호화폐 관련 도구들을 MCP 서버에 등록"""
    
    @mcp.tool(description="Get cryptocurrency market overview from Investing.com. For individual crypto prices, use get_crypto_quote.")
    def get_crypto_data() -> str:
        """
        암호화폐 시장 데이터를 조회합니다.
        
        Returns:
            str: 암호화폐 시장 데이터 (마크다운 형식)
        """
        try:
            return service_manager.get_crypto_data()
        except Exception as e:
            return f"Error: {str(e)}"