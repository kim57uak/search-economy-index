# search-economy-index
경제 지표 검색을 위한 SOLID 원칙 기반 MCP 서버 및 HTTP API 서버

## 🎯 개요
이 프로젝트는 SOLID 원칙과 디자인 패턴을 적용한 확장 가능한 경제 데이터 분석 플랫폼입니다:

1. **MCP 서버**: Model Context Protocol을 사용한 AI 도구 서버
2. **HTTP API 서버**: RESTful API 서버
3. **모듈화된 아키텍처**: 인터페이스 기반 확장 가능한 구조

## 🚀 주요 기능

### 📈 네이버 금융 검색
- 국내 티커 검색 (KOSPI, KOSDAQ)
- 해외 티커 검색 (NYSE, NASDAQ 등)

### 📊 FnGuide 분석 도구
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

### 🪙 암호화폐 데이터
- Investing.com 암호화폐 시장 데이터

## 🏗️ 아키텍처 특징

### SOLID 원칙 준수
- **SRP**: 각 클래스가 단일 책임만 담당
- **OCP**: 새로운 파서 추가 시 기존 코드 수정 불필요
- **LSP**: 인터페이스 기반 다형성 지원
- **ISP**: 역할별 인터페이스 분리
- **DIP**: 추상화에 의존하는 구조

### 디자인 패턴 적용
- **팩토리 패턴**: 파서 생성 및 관리
- **의존성 주입**: 서비스 매니저를 통한 중앙화된 관리
- **싱글톤 패턴**: 리소스 효율적 관리

## ⚙️ 시스템 요구사항
- **Python 3.12+** (MCP SDK 요구사항)
- macOS/Linux 환경

## 🚀 빠른 시작

자세한 설치 및 실행 방법은 [SETUP.md](SETUP.md)를 참조하세요.

## 📚 사용법

### 🤖 MCP 서버 (AI 도구)

**MCP 도구 함수 목록**

```python
# 네이버 금융 검색
search_domestic_ticker(query)    # 국내 티커 검색
search_overseas_ticker(query)    # 해외 티커 검색

# FnGuide 분석
get_stock_snapshot(ticker)       # 종합 스냅샷
get_company_overview(ticker)     # 기업 개요
get_financial_statements(ticker) # 재무제표
get_financial_ratios(ticker)     # 재무비율
get_investment_indicators(ticker)# 투자지표
get_analyst_consensus(ticker)    # 애널리스트 컨센서스
get_ownership_analysis(ticker)   # 지분 분석
get_industry_analysis(ticker)    # 업종 분석
get_competitor_comparison(ticker)# 경쟁사 비교
get_exchange_disclosures(ticker) # 거래소 공시
get_earnings_reports(ticker)     # 실적 보고서

# 암호화폐
get_crypto_data()               # 암호화폐 시장 데이터

# 거래소 정보
get_exchange_data()             # 거래소 데이터

# 원자재 정보
get_materials_data()            # 원자재 시장 데이터
```

### 🌐 HTTP API 서버

**주요 엔드포인트**

```bash
# 네이버 금융 검색
GET /search/domestic/{query}     # 국내 티커 검색
GET /search/overseas/{query}     # 해외 티커 검색

# FnGuide 분석
GET /fnguide/snapshot/{ticker}   # 종합 스냅샷
GET /fnguide/overview/{ticker}   # 기업 개요
GET /fnguide/financials/{ticker} # 재무제표
GET /fnguide/ratios/{ticker}     # 재무비율
GET /fnguide/indicators/{ticker} # 투자지표
GET /fnguide/consensus/{ticker}  # 애널리스트 컨센서스
GET /fnguide/ownership/{ticker}  # 지분 분석
GET /fnguide/industry/{ticker}   # 업종 분석
GET /fnguide/competitors/{ticker}# 경쟁사 비교
GET /fnguide/disclosures/{ticker}# 거래소 공시
GET /fnguide/earnings/{ticker}   # 실적 보고서

# 암호화폐
GET /crypto/data                 # 암호화폐 시장 데이터

# 거래소
GET /exchange/data               # 거래소 데이터

# 원자재
GET /materials/data              # 원자재 시장 데이터
```

### 💻 서비스 매니저 (프로그래밍)

```python
from src.core.service_manager import service_manager

# 통합된 서비스 인터페이스
tickers = service_manager.search_domestic_ticker("삼성전자")
snapshot = service_manager.get_stock_snapshot("005930")
crypto = service_manager.get_crypto_data()
```

## 🔄 서버 비교

| 구분 | MCP 서버 | HTTP API 서버 |
|------|----------|---------------|
| **용도** | AI 도구, Claude Desktop | 웹앱, 모바일앱 |
| **프로토콜** | MCP (SSE) | HTTP REST |
| **포트** | 자동 할당 | 8000 |
| **클라이언트** | MCP 호환 AI | 모든 HTTP 클라이언트 |
| **응답 형식** | MCP 메시지 | JSON |
| **사용 예시** | AI 주식 분석 | 웹 대시보드 |

## 🏛️ 아키텍처 구조

```
src/
├── core/                    # 핵심 아키텍처
│   ├── interfaces.py        # 추상 인터페이스
│   ├── base_parser.py       # 기본 클래스 및 팩토리
│   └── service_manager.py   # 의존성 주입 관리
├── parsers/                 # 데이터 파서들
│   ├── http_client.py       # HTTP 클라이언트
│   ├── ticker_parser.py     # 네이버 금융 파서
│   ├── fnguide_parser.py    # FnGuide 파서
│   └── crypto_parser.py     # 암호화폐 파서
├── mcp_tools/              # MCP 도구들
├── api_routes/             # HTTP API 라우트들
├── mcp_server.py           # MCP 서버
└── simple_server.py        # HTTP API 서버
```

## 🔧 확장 방법

새로운 데이터 소스 추가:

1. **파서 인터페이스 구현**
```python
class NewParser(WebParserBase, ParserInterface):
    def parse(self, *args, **kwargs):
        # 구현
        pass
```

2. **팩토리에 등록**
```python
ParserFactory.register_parser('new_parser', NewParser)
```

3. **서비스 매니저에 메서드 추가**
```python
def get_new_data(self):
    parser = self.get_parser('new_parser')
    return parser.parse()
```

## 📋 주요 파일 설명

### 실행 파일
- **run_server.py**: MCP 서버 실행
- **run_api_server.py**: HTTP API 서버 실행
- **setup_venv.sh**: 가상환경 자동 설정

### 핵심 아키텍처
- **src/core/service_manager.py**: 통합 서비스 관리
- **src/core/interfaces.py**: 추상 인터페이스 정의
- **src/core/base_parser.py**: 기본 클래스 및 팩토리

### 데이터 파서
- **src/parsers/**: 각종 데이터 소스 파서들
- **src/mcp_tools/**: MCP 도구 함수들
- **src/api_routes/**: HTTP API 엔드포인트들

## 📦 주요 의존성
- **mcp[cli]>=1.19.0** - MCP SDK
- **requests>=2.31.0** - HTTP 요청
- **lxml>=4.9.0** - XML/HTML 파싱
- **markdownify>=0.11.0** - HTML → 마크다운 변환
- **fastapi>=0.68.0** - HTTP API 서버
- **uvicorn>=0.15.0** - ASGI 서버

## 🧪 테스트

자세한 테스트 방법은 [SETUP.md](SETUP.md)를 참조하세요.

```bash
# 전체 테스트 실행
./run_tests.sh

# 개별 테스트
python test_mcp_server.py
python test_simple_server.py
```

## ⚠️ 주의사항
- **Python 3.12+** 필수 (MCP SDK 요구사항)
- 웹 스크래핑이므로 사이트 정책 준수 필요
- 과도한 요청 시 IP 차단 가능성
- 가상환경에서 실행 권장

## 📖 추가 문서
- [SETUP.md](SETUP.md) - 상세 설치 및 실행 가이드
- [SOLID_REFACTORING_SUMMARY.md](SOLID_REFACTORING_SUMMARY.md) - 리팩토링 상세 보고서

## 🤝 기여하기

1. 새로운 파서 추가 시 인터페이스 기반으로 구현
2. SOLID 원칙 준수
3. 테스트 코드 작성
4. 문서 업데이트