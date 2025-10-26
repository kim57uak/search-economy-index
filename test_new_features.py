#!/usr/bin/env python3
"""
새로 추가된 기능들 테스트 코드
"""
import asyncio
import sys
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# src 디렉토리를 Python 경로에 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

async def test_new_features():
    """새로 추가된 기능들 테스트"""
    
    server_params = StdioServerParameters(
        command="python",
        args=["run_server.py"],
        env=os.environ.copy()
    )
    
    print("=== 새 기능 테스트 시작 ===")
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                print("✓ MCP 서버 연결 성공")
                
                tools = await session.list_tools()
                print(f"✓ 총 도구 수: {len(tools.tools)}개")
                
                print("\n=== 시장 지표 테스트 ===")
                
                # 시장 지수 테스트
                try:
                    result = await session.call_tool("get_market_indices", arguments={})
                    print("✓ 시장 지수 조회 성공")
                    if result.content and len(result.content) > 0:
                        print(f"  응답 길이: {len(str(result.content[0]))}자")
                except Exception as e:
                    print(f"✗ 시장 지수 조회 실패: {e}")
                
                # 업종별 등락률 테스트
                try:
                    result = await session.call_tool("get_sector_performance", arguments={})
                    print("✓ 업종별 등락률 조회 성공")
                    if result.content and len(result.content) > 0:
                        print(f"  응답 길이: {len(str(result.content[0]))}자")
                except Exception as e:
                    print(f"✗ 업종별 등락률 조회 실패: {e}")
                
                # 상승률 상위 종목 테스트
                try:
                    result = await session.call_tool("get_top_gainers", arguments={})
                    print("✓ 상승률 상위 종목 조회 성공")
                    if result.content and len(result.content) > 0:
                        print(f"  응답 길이: {len(str(result.content[0]))}자")
                except Exception as e:
                    print(f"✗ 상승률 상위 종목 조회 실패: {e}")
                
                print("\n=== 금리/채권 테스트 ===")
                
                # 금리 정보 테스트
                try:
                    result = await session.call_tool("get_interest_rates", arguments={})
                    print("✓ 금리 정보 조회 성공")
                    if result.content and len(result.content) > 0:
                        print(f"  응답 길이: {len(str(result.content[0]))}자")
                except Exception as e:
                    print(f"✗ 금리 정보 조회 실패: {e}")
                
                # 국고채 수익률 테스트
                try:
                    result = await session.call_tool("get_bond_yields", arguments={})
                    print("✓ 국고채 수익률 조회 성공")
                    if result.content and len(result.content) > 0:
                        print(f"  응답 길이: {len(str(result.content[0]))}자")
                except Exception as e:
                    print(f"✗ 국고채 수익률 조회 실패: {e}")
                
                # CD금리 테스트
                try:
                    result = await session.call_tool("get_cd_rates", arguments={})
                    print("✓ CD금리 조회 성공")
                    if result.content and len(result.content) > 0:
                        print(f"  응답 길이: {len(str(result.content[0]))}자")
                except Exception as e:
                    print(f"✗ CD금리 조회 실패: {e}")
                
                print("\n=== 테스트 완료 ===")
                
    except Exception as e:
        print(f"✗ 테스트 실패: {e}")

def main():
    """메인 함수"""
    print("새로 추가된 기능들을 테스트합니다...")
    asyncio.run(test_new_features())

if __name__ == "__main__":
    main()