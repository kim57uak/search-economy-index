"""
경제 지표 검색을 위한 MCP 서버
"""
import logging
from mcp.server.fastmcp import FastMCP

# 도메인별 도구 모듈들 import
from .mcp_tools.ticker_tools import register_ticker_tools
from .mcp_tools.fnguide_tools import register_fnguide_tools
from .mcp_tools.crypto_tools import register_crypto_tools
from .mcp_tools.materials_tools import register_materials_tools
from .mcp_tools.exchange_tools import register_exchange_tools

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MCP 서버 생성
mcp = FastMCP("search-economy-index")

# 도메인별 도구들 등록
register_ticker_tools(mcp)      # 티커 검색 (2개 함수)
register_fnguide_tools(mcp)     # 주식 분석 (11개 함수)
register_crypto_tools(mcp)      # 암호화폐 (1개 함수)
register_materials_tools(mcp)   # 원자재/귀금속 (5개 함수)
register_exchange_tools(mcp)    # 환율 (2개 함수)

def main():
    """MCP 서버 메인 함수"""
    mcp.run()

if __name__ == "__main__":
    main()