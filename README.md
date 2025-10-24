# search-economy-index
경제 지표 검색을 위한 MCP 서버 및 HTTP API 서버

## 개요
이 프로젝트는 두 가지 서버를 제공합니다:
1. **MCP 서버**: Model Context Protocol을 사용한 AI 도구 서버
2. **Simple API 서버**: 일반적인 HTTP REST API 서버

## 기능

### 네이버 금융 검색
- 국내 티커 검색 (KOSPI, KOSDAQ)
- 해외 티커 검색 (NYSE, NASDAQ 등)
- 실적속보 정보 조회
- 거래소공시 정보 조회

### FnGuide 분석 도구
- 종합 주식 스냅샷
- 기업 개요 및 사업 정보
- 재무제표 (손익계산서, 대차대조표, 현금흐름표)
- 재무비율 분석
- 투자지표 (PER, PBR, 배당수익률)
- 애널리스트 컨센서스
- 주주구조 및 지분 분석
- 업종 분석
- 경쟁사 비교
- 거래소 공시
- 실적 보고서

## 시스템 요구사항
- **Python 3.12+** (MCP SDK 요구사항)
- macOS/Linux 환경

## 설치 및 실행

### 1. 가상환경 설정 (Python 3.12)
```bash
# 자동 설정 스크립트 실행
bash setup_venv.sh

# 또는 수동 설정
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. 서버 선택 및 실행

#### Option A: MCP 서버 (AI 도구용)
```bash
source venv/bin/activate
python run_server.py
```

#### Option B: Simple API 서버 (HTTP REST API)
```bash
source venv/bin/activate
python simple_server.py
```

## 사용법

### MCP 서버 사용법

**MCP 서버는 AI 도구로 사용됩니다. Claude Desktop, MCP Inspector 등에서 활용 가능합니다.**

#### MCP 도구 함수 목록

**네이버 금융 검색**
- `search_domestic_ticker(query)` - 국내 티커 검색
- `search_overseas_ticker(query)` - 해외 티커 검색

**FnGuide 분석 (티커 코드 사용)**
- `get_stock_snapshot(ticker)` - 종합 스냅샷
- `get_company_overview(ticker)` - 기업 개요
- `get_financial_statements(ticker)` - 재무제표
- `get_financial_ratios(ticker)` - 재무비율
- `get_investment_indicators(ticker)` - 투자지표
- `get_analyst_consensus(ticker)` - 애널리스트 컨센서스
- `get_ownership_analysis(ticker)` - 지분 분석
- `get_industry_analysis(ticker)` - 업종 분석
- `get_competitor_comparison(ticker)` - 경쟁사 비교
- `get_exchange_disclosures(ticker)` - 거래소 공시
- `get_earnings_reports(ticker)` - 실적 보고서

#### MCP 도구 사용 예시
```python
# AI가 이 도구들을 사용하여 주식 분석을 수행
search_domestic_ticker("삼성전자")  # 삼성전자 검색
get_stock_snapshot("005930")        # 삼성전자 스냅샷
get_financial_statements("005930")  # 삼성전자 재무제표
```

### Simple API 서버 사용법

**Simple API 서버는 일반적인 HTTP REST API입니다. 웹 애플리케이션, 모바일 앱 등에서 활용 가능합니다.**

#### 서버 정보
- **URL**: `http://localhost:8000`
- **포트**: 8000
- **형식**: JSON 응답

#### HTTP API 엔드포인트 목록

**네이버 금융 검색**
- `GET /search/domestic/{query}` - 국내 티커 검색
- `GET /search/overseas/{query}` - 해외 티커 검색

**FnGuide 분석**
- `GET /fnguide/snapshot/{ticker}` - 종합 스냅샷
- `GET /fnguide/overview/{ticker}` - 기업 개요
- `GET /fnguide/financials/{ticker}` - 재무제표
- `GET /fnguide/ratios/{ticker}` - 재무비율
- `GET /fnguide/indicators/{ticker}` - 투자지표
- `GET /fnguide/consensus/{ticker}` - 애널리스트 컨센서스
- `GET /fnguide/ownership/{ticker}` - 지분 분석
- `GET /fnguide/industry/{ticker}` - 업종 분석
- `GET /fnguide/competitors/{ticker}` - 경쟁사 비교
- `GET /fnguide/disclosures/{ticker}` - 거래소 공시
- `GET /fnguide/earnings/{ticker}` - 실적 보고서

#### HTTP API 사용 예시
```bash
# curl을 사용한 API 호출 예시
curl "http://localhost:8000/search/domestic/삼성전자"
curl "http://localhost:8000/fnguide/snapshot/005930"
curl "http://localhost:8000/fnguide/financials/005930"
```

```javascript
// JavaScript fetch 예시
fetch('http://localhost:8000/search/domestic/삼성전자')
  .then(response => response.json())
  .then(data => console.log(data));

fetch('http://localhost:8000/fnguide/snapshot/005930')
  .then(response => response.json())
  .then(data => console.log(data));
```

## 서버 비교

| 구분 | MCP 서버 | Simple API 서버 |
|------|----------|----------------|
| **용도** | AI 도구, Claude Desktop | 웹앱, 모바일앱 |
| **프로토콜** | MCP (SSE) | HTTP REST |
| **포트** | 자동 할당 | 8000 |
| **클라이언트** | MCP 호환 AI | 모든 HTTP 클라이언트 |
| **응답 형식** | MCP 메시지 | JSON |
| **사용 예시** | AI 주식 분석 | 웹 대시보드 |

## MCP 함수 상세 설명

### 네이버 금융 검색 함수

**search_domestic_ticker(query: str)**
- **기능**: 한국 국내 주식 티커 검색 (KOSPI, KOSDAQ)
- **입력**: 종목명 또는 티커 (예: "삼성전자", "005930")
- **출력**: 국내 티커 목록, 실적속보, 거래소공시 정보
- **사용 시점**: 한국 주식 정보가 필요할 때

**search_overseas_ticker(query: str)**
- **기능**: 해외/국제 주식 티커 검색 (NYSE, NASDAQ, 유럽 등)
- **입력**: 종목명 또는 티커 (예: "Apple", "AAPL", "Tesla")
- **출력**: 해외 티커 목록, 관련 시장 정보
- **사용 시점**: 해외 주식 정보가 필요할 때

### FnGuide 분석 함수

**get_stock_snapshot(ticker: str)**
- **기능**: 종합적인 주식 스냅샷 (주가, 거래량, 핵심 지표)
- **입력**: 주식 티커 (예: "005930")
- **출력**: 실시간 주가, 거래량, 재무지표 종합 정보

**get_company_overview(ticker: str)**
- **기능**: 기업 개요 및 사업 정보
- **입력**: 주식 티커 (예: "005930")
- **출력**: 기업 프로필, 사업 설명, 임원진, 기업 구조

**get_financial_statements(ticker: str)**
- **기능**: 재무제표 (손익계산서, 대차대조표, 현금흐름표)
- **입력**: 주식 티커 (예: "005930")
- **출력**: 매출, 이익, 자산, 부채, 현금흐름 상세 데이터

**get_financial_ratios(ticker: str)**
- **기능**: 재무비율 및 지표 분석
- **입력**: 주식 티커 (예: "005930")
- **출력**: 수익성, 유동성, 효율성, 레버리지 비율

**get_investment_indicators(ticker: str)**
- **기능**: 투자지표 및 밸류에이션 지표
- **입력**: 주식 티커 (예: "005930")
- **출력**: PER, PBR, 배당수익률, 기타 투자 지표

**get_analyst_consensus(ticker: str)**
- **기능**: 애널리스트 컨센서스 및 추천 의견
- **입력**: 주식 티커 (예: "005930")
- **출력**: 애널리스트 등급, 목표주가, 컨센서스 전망

**get_ownership_analysis(ticker: str)**
- **기능**: 주주구조 및 지분 분석
- **입력**: 주식 티커 (예: "005930")
- **출력**: 주요 주주, 기관 투자자 지분율, 주주구조 변화

**get_industry_analysis(ticker: str)**
- **기능**: 업종 섹터 분석 및 트렌드 비교
- **입력**: 주식 티커 (예: "005930")
- **출력**: 업종 트렌드, 섹터 성과, 동종업계 비교

**get_competitor_comparison(ticker: str)**
- **기능**: 경쟁사 비교 및 동종업계 분석
- **입력**: 주식 티커 (예: "005930")
- **출력**: 재무지표, 성과, 시장 지위 비교 분석

**get_exchange_disclosures(ticker: str)**
- **기능**: 공식 거래소 공시 및 규제 신고서
- **입력**: 주식 티커 (예: "005930")
- **출력**: 공식 발표, 규제 신고서, 중요 기업 공시

**get_earnings_reports(ticker: str)**
- **기능**: 최신 실적 보고서 및 재무 결과
- **입력**: 주식 티커 (예: "005930")
- **출력**: 분기별/연간 실적, 재무 결과, 성과 업데이트

## 프로젝트 구조
```
search-economy-index/
├── src/
│   ├── __init__.py
│   ├── ticker_parser.py      # 네이버 금융 파싱
│   ├── fnguide_parser.py     # FnGuide 파싱
│   ├── mcp_server.py         # MCP 서버 메인
│   └── simple_mcp_server.py  # MCP 없는 서버 클래스
├── requirements.txt          # 의존성 (Python 3.12+)
├── run_server.py            # MCP 서버 실행 스크립트
├── simple_server.py         # HTTP API 서버 실행 스크립트
├── setup_venv.sh            # 가상환경 설정 (Python 3.12)
└── README.md
```

## 파일 설명
- **run_server.py**: MCP 서버 실행 (AI 도구용)
- **simple_server.py**: HTTP API 서버 실행 (웹앱용)
- **src/mcp_server.py**: MCP 프로토콜 서버 구현
- **src/simple_mcp_server.py**: 일반 클래스 기반 서버
- **src/ticker_parser.py**: 네이버 금융 데이터 파싱
- **src/fnguide_parser.py**: FnGuide 데이터 파싱

## 의존성
- **mcp[cli]>=1.19.0** - MCP SDK
- **requests>=2.31.0** - HTTP 요청
- **lxml>=4.9.0** - XML/HTML 파싱
- **beautifulsoup4>=4.12.0** - HTML 파싱
- **fastapi>=0.68.0** - HTTP API 서버
- **uvicorn>=0.15.0** - ASGI 서버

## 테스트

### 전체 테스트 실행
```bash
# 가상환경 활성화 후
source venv/bin/activate

# 테스트 스위트 실행
./run_tests.sh
```

### 개별 테스트

#### MCP 서버 테스트
```bash
python test_mcp_server.py
```

#### Simple API 서버 테스트
```bash
# 서버 시작 (별도 터미널)
python simple_server.py

# 테스트 실행 (다른 터미널)
python test_simple_server.py
```

## 주의사항
- MCP SDK는 Python 3.10+ 요구
- 웹 스크래핑이므로 사이트 정책 준수 필요
- 과도한 요청 시 IP 차단 가능성