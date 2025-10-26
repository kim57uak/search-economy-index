#!/usr/bin/env python3
"""
MCP 해외주식 공시정보 도구 테스트
"""
import asyncio
import sys
sys.path.append('src')

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_mcp_overseas_disclosure():
    """MCP 해외주식 공시정보 도구 테스트"""
    server_params = StdioServerParameters(
        command="python",
        args=["run_server.py"],
        env=None
    )
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                # 사용 가능한 도구 확인
                tools = await session.list_tools()
                overseas_tools = [tool for tool in tools.tools if 'overseas' in tool.name.lower()]
                
                print(f"해외 관련 도구 수: {len(overseas_tools)}")
                for tool in overseas_tools:
                    print(f"- {tool.name}: {tool.description}")
                
                # 해외주식 공시정보 도구 테스트
                if overseas_tools:
                    print(f"\n=== {overseas_tools[0].name} 테스트 ===")
                    result = await session.call_tool(overseas_tools[0].name, {"symbol": "AAPL"})
                    
                    if result.content:
                        content = result.content[0].text if hasattr(result.content[0], 'text') else str(result.content[0])
                        print(f"결과 길이: {len(content)} 문자")
                        print(f"결과 미리보기: {content[:300]}...")
                    else:
                        print("결과 없음")
                else:
                    print("해외 공시정보 도구를 찾을 수 없습니다.")
                    
    except Exception as e:
        print(f"MCP 테스트 오류: {e}")

if __name__ == "__main__":
    asyncio.run(test_mcp_overseas_disclosure())