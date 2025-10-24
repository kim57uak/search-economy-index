#!/usr/bin/env python3
"""
MCP 서버 테스트 코드
"""
import asyncio
import sys
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# src 디렉토리를 Python 경로에 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

async def test_mcp_server():
    """MCP 서버 기능 테스트"""
    
    # MCP 서버 파라미터 설정
    server_params = StdioServerParameters(
        command="python",
        args=["run_server.py"],
        env=os.environ.copy()
    )
    
    print("=== MCP 서버 테스트 시작 ===")
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # 서버 초기화
                await session.initialize()
                print("✓ MCP 서버 연결 성공")
                
                # 도구 목록 조회
                tools = await session.list_tools()
                print(f"✓ 사용 가능한 도구 수: {len(tools.tools)}")
                
                for tool in tools.tools:
                    print(f"  - {tool.name}: {tool.description}")
                
                print("\n=== 네이버 금융 검색 테스트 ===")
                
                # 국내 티커 검색 테스트
                try:
                    result = await session.call_tool(
                        "search_domestic_ticker", 
                        arguments={"query": "삼성전자"}
                    )
                    print("✓ 국내 티커 검색 성공")
                    if result.content and len(result.content) > 0:
                        print(f"  응답 길이: {len(str(result.content[0]))}")
                except Exception as e:
                    print(f"✗ 국내 티커 검색 실패: {e}")
                
                # 해외 티커 검색 테스트
                try:
                    result = await session.call_tool(
                        "search_overseas_ticker", 
                        arguments={"query": "AAPL"}
                    )
                    print("✓ 해외 티커 검색 성공")
                    if result.content and len(result.content) > 0:
                        print(f"  응답 길이: {len(str(result.content[0]))}")
                except Exception as e:
                    print(f"✗ 해외 티커 검색 실패: {e}")
                
                print("\n=== FnGuide 분석 테스트 ===")
                
                # FnGuide 도구들 테스트
                fnguide_tools = [
                    ("get_stock_snapshot", "스냅샷"),
                    ("get_company_overview", "기업개요"),
                    ("get_financial_statements", "재무제표"),
                    ("get_financial_ratios", "재무비율"),
                    ("get_investment_indicators", "투자지표")
                ]
                
                for tool_name, description in fnguide_tools:
                    try:
                        result = await session.call_tool(
                            tool_name, 
                            arguments={"ticker": "005930"}
                        )
                        print(f"✓ {description} 조회 성공")
                        if result.content and len(result.content) > 0:
                            print(f"  응답 길이: {len(str(result.content[0]))}")
                    except Exception as e:
                        print(f"✗ {description} 조회 실패: {e}")
                
                print("\n=== 테스트 완료 ===")
                
    except Exception as e:
        print(f"✗ MCP 서버 연결 실패: {e}")
        print("서버가 실행 중인지 확인하세요: python run_server.py")

async def test_server_startup():
    """서버 시작 테스트"""
    print("=== MCP 서버 시작 테스트 ===")
    
    # 간단한 연결 테스트
    server_params = StdioServerParameters(
        command="python",
        args=["run_server.py"],
        env=os.environ.copy()
    )
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                print("✓ MCP 서버 시작 성공")
                
                # 기본 정보 확인
                tools = await session.list_tools()
                print(f"✓ 도구 로드 완료: {len(tools.tools)}개")
                
                return True
    except Exception as e:
        print(f"✗ MCP 서버 시작 실패: {e}")
        return False

def main():
    """메인 함수"""
    print("MCP 서버 테스트를 시작합니다...")
    
    # 서버 시작 테스트
    startup_success = asyncio.run(test_server_startup())
    
    if startup_success:
        print("\n서버가 정상적으로 시작되었습니다.")
        
        # 사용자 선택
        choice = input("\n전체 기능 테스트를 실행하시겠습니까? (y/n): ")
        
        if choice.lower() == 'y':
            asyncio.run(test_mcp_server())
        else:
            print("테스트를 종료합니다.")
    else:
        print("\n서버 시작에 실패했습니다.")
        print("다음을 확인하세요:")
        print("1. 가상환경이 활성화되어 있는지")
        print("2. 의존성이 설치되어 있는지")
        print("3. run_server.py 파일이 존재하는지")

if __name__ == "__main__":
    main()