#!/bin/bash
# 가상환경 설정 스크립트 (Python 3.12)

echo "기존 가상환경 삭제 중..."
rm -rf venv

echo "Python 3.12로 가상환경 생성 중..."
python3.12 -m venv venv

echo "가상환경 활성화 중..."
source venv/bin/activate

echo "pip 업그레이드 중..."
pip install --upgrade pip

echo "의존성 설치 중..."
pip install -r requirements.txt

echo "설정 완료!"
echo "Python 버전: $(python --version)"
echo "가상환경을 활성화하려면: source venv/bin/activate"
echo "MCP 서버 실행: python run_server.py"
echo "HTTP 서버 실행: python simple_server.py"