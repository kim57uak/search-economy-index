#!/usr/bin/env python3
"""
MCP 서버 실행 스크립트
"""
import sys
import os

# src 디렉토리를 Python 경로에 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from mcp_server import mcp

if __name__ == "__main__":
    mcp.run()