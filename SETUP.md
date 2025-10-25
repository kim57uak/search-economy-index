# 설치 및 실행 가이드

## 🚀 빠른 시작

### 1. 시스템 요구사항
- **Python 3.12+** (필수)
- macOS/Linux 환경
- Git

### 2. 프로젝트 클론
```bash
git clone <repository-url>
cd search-economy-index
```

### 3. 가상환경 설정

#### 자동 설정 (권장)
```bash
bash setup_venv.sh
```

#### 수동 설정
```bash
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 🖥️ 서버 실행

### MCP 서버 (AI 도구용)
```bash
# 가상환경 활성화
source venv/bin/activate

# MCP 서버 실행
python run_server.py
```

**사용 대상**: Claude Desktop, MCP Inspector 등 AI 도구

### HTTP API 서버 (웹앱용)
```bash
# 가상환경 활성화
source venv/bin/activate

# API 서버 실행
python run_api_server.py
```

**접속 URL**: http://localhost:8000
**API 문서**: http://localhost:8000/docs

## 🧪 테스트 실행

### 전체 테스트
```bash
source venv/bin/activate
./run_tests.sh
```

### 개별 테스트

#### MCP 서버 테스트
```bash
source venv/bin/activate
python test_mcp_server.py
```

#### HTTP API 서버 테스트
```bash
# 터미널 1: 서버 시작
source venv/bin/activate
python run_api_server.py

# 터미널 2: 테스트 실행
source venv/bin/activate
python test_simple_server.py
```

## 📡 API 사용 예시

### curl 명령어
```bash
# 국내 티커 검색
curl "http://localhost:8000/search/domestic/삼성전자"

# 주식 스냅샷 조회
curl "http://localhost:8000/fnguide/snapshot/005930"

# 암호화폐 데이터 조회
curl "http://localhost:8000/crypto/data"
```

### Python 코드
```python
import requests

# 국내 티커 검색
response = requests.get("http://localhost:8000/search/domestic/삼성전자")
print(response.json())

# 재무제표 조회
response = requests.get("http://localhost:8000/fnguide/financials/005930")
print(response.json())
```

### JavaScript 코드
```javascript
// 국내 티커 검색
fetch('http://localhost:8000/search/domestic/삼성전자')
  .then(response => response.json())
  .then(data => console.log(data));

// 기업 개요 조회
fetch('http://localhost:8000/fnguide/overview/005930')
  .then(response => response.json())
  .then(data => console.log(data));
```

## 🔧 개발 환경 설정

### IDE 설정
```bash
# VS Code 설정 (선택사항)
code .
```

### 환경 변수 (필요시)
```bash
# .env 파일 생성
echo "DEBUG=True" > .env
echo "LOG_LEVEL=INFO" >> .env
```

### 로그 확인
```bash
# 로그 파일 위치
tail -f logs/app.log
```

## 🐛 문제 해결

### 일반적인 문제들

#### Python 버전 문제
```bash
# Python 3.12 설치 확인
python3.12 --version

# 가상환경 재생성
rm -rf venv
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 의존성 설치 실패
```bash
# pip 업그레이드
pip install --upgrade pip

# 의존성 재설치
pip install -r requirements.txt --force-reinstall
```

#### 포트 충돌
```bash
# 포트 8000 사용 중인 프로세스 확인
lsof -i :8000

# 프로세스 종료
kill -9 <PID>
```

#### 인코딩 문제
```bash
# 시스템 로케일 확인
locale

# UTF-8 설정
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
```

### 로그 레벨 조정
```python
# src/core/service_manager.py에서 로그 레벨 변경
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📊 성능 모니터링

### 메모리 사용량 확인
```bash
# 프로세스 메모리 사용량
ps aux | grep python

# 시스템 메모리 상태
free -h  # Linux
vm_stat  # macOS
```

### API 응답 시간 측정
```bash
# curl로 응답 시간 측정
curl -w "@curl-format.txt" -o /dev/null -s "http://localhost:8000/fnguide/snapshot/005930"
```

curl-format.txt 파일:
```
     time_namelookup:  %{time_namelookup}\n
        time_connect:  %{time_connect}\n
     time_appconnect:  %{time_appconnect}\n
    time_pretransfer:  %{time_pretransfer}\n
       time_redirect:  %{time_redirect}\n
  time_starttransfer:  %{time_starttransfer}\n
                     ----------\n
          time_total:  %{time_total}\n
```

## 🔄 업데이트 및 배포

### 코드 업데이트
```bash
git pull origin main
source venv/bin/activate
pip install -r requirements.txt --upgrade
```

### 서버 재시작
```bash
# 기존 프로세스 종료
pkill -f "python run_api_server.py"

# 새 서버 시작
source venv/bin/activate
python run_api_server.py
```

## 📞 지원

문제가 발생하면:
1. 로그 파일 확인
2. 가상환경 재생성 시도
3. 의존성 재설치
4. GitHub Issues에 문제 보고