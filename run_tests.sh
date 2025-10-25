#!/bin/bash
# 전체 테스트 실행 스크립트

echo "=== 경제 지표 검색 서버 테스트 스위트 ==="

# 가상환경 확인
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  가상환경이 활성화되지 않았습니다."
    echo "다음 명령어로 가상환경을 활성화하세요:"
    echo "source venv/bin/activate"
    exit 1
fi

echo "✓ 가상환경 활성화됨: $VIRTUAL_ENV"

# Python 버전 확인
python_version=$(python --version)
echo "✓ Python 버전: $python_version"

echo ""
echo "1. MCP 서버 테스트"
echo "2. Simple API 서버 테스트"
echo "3. 전체 테스트"
echo ""

read -p "선택하세요 (1-3): " choice

case $choice in
    1)
        echo "=== MCP 서버 테스트 실행 ==="
        python test_mcp_server.py
        ;;
    2)
        echo "=== Simple API 서버 테스트 실행 ==="
        echo "먼저 별도 터미널에서 서버를 시작하세요:"
        echo "python run_api_server.py"
        echo ""
        read -p "서버가 시작되었으면 Enter를 누르세요..."
        python test_simple_server.py
        ;;
    3)
        echo "=== 전체 테스트 실행 ==="
        echo ""
        echo "1단계: MCP 서버 테스트"
        python test_mcp_server.py
        
        echo ""
        echo "2단계: Simple API 서버 테스트"
        echo "Simple API 서버를 백그라운드에서 시작합니다..."
        
        # Simple API 서버를 백그라운드에서 시작
        python run_api_server.py &
        SERVER_PID=$!
        
        # 서버 시작 대기
        echo "서버 시작 대기 중..."
        sleep 3
        
        # API 테스트 실행
        python test_simple_server.py
        
        # 서버 종료
        echo "서버를 종료합니다..."
        kill $SERVER_PID 2>/dev/null
        ;;
    *)
        echo "잘못된 선택입니다."
        exit 1
        ;;
esac

echo ""
echo "=== 테스트 완료 ==="