# Trading Economics API 연동 가이드

## 📋 개요

Trading Economics API는 300,000개 이상의 경제 지표, 환율, 주식 시장 지수, 정부 채권 수익률, 상품 가격 등에 직접 액세스할 수 있는 API입니다.

### 주요 데이터
- 경제 지표 (Economic Indicators)
- 환율 (Exchange Rates)
- 주식 시장 지수 (Stock Market Indexes)
- 정부 채권 수익률 (Government Bond Yields)
- 상품 가격 (Commodity Prices)
- 기업 재무 정보 (Company Financials)
- 실시간 경제 캘린더 (Economic Calendar)
- 수익 발표 캘린더 (Earnings Releases Calendar)

---

## 🔑 인증 (Authentication)

### API 키 발급
Trading Economics 웹사이트에서 API 키를 발급받아야 합니다.
- 테스트용: `guest:guest`
- 프로덕션: 유료 플랜 가입 후 발급

### 인증 방법

#### 1. URL 파라미터 방식
```
https://api.tradingeconomics.com/country/mexico?c=YOUR_API_KEY
```

#### 2. HTTP 헤더 방식
```
Authorization: YOUR_API_KEY
```

---

## 🌐 API 연동 방식

### 1. REST API 엔드포인트 (직접 HTTP 요청)

#### Python 예제
```python
import requests

api_key = 'YOUR_API_KEY'
url = f'https://api.tradingeconomics.com/country/mexico?c={api_key}'
data = requests.get(url).json()
print(data)
```

#### 헤더 방식 인증
```python
import requests

response = requests.get(
    'https://api.tradingeconomics.com/country/mexico',
    headers={'Authorization': 'YOUR_API_KEY'}
)
print(response.json())
```

#### JavaScript/Node.js 예제
```javascript
const axios = require('axios');

(async () => {
    const api_key = 'YOUR_API_KEY';
    const response = await axios.get(
        `https://api.tradingeconomics.com/country/mexico?c=${api_key}`
    );
    console.log(response.data);
})();
```

#### 헤더 방식 인증
```javascript
const url = 'https://api.tradingeconomics.com/country/mexico';
const headers = { 'Authorization': 'YOUR_API_KEY' };

const response = await fetch(url, {
    method: 'GET',
    headers
});
const data = await response.text();
console.log(data);
```

#### C# 예제
```csharp
using (var httpClient = new HttpClient())
{
    using (var request = new HttpRequestMessage(
        new HttpMethod("GET"),
        "https://api.tradingeconomics.com/country/mexico?c=YOUR_API_KEY"))
    {
        request.Headers.TryAddWithoutValidation("Upgrade-Insecure-Requests", "1");
        var response = await httpClient.SendAsync(request);
        
        if (response.IsSuccessStatusCode)
        {
            var content = await response.Content.ReadAsStringAsync();
            Console.WriteLine(content);
        }
    }
}
```

---

### 2. 공식 패키지 사용

#### Python 패키지

##### 설치
```bash
pip install tradingeconomics
```

##### 환경 변수 설정 (권장)
```bash
# Windows
set apikey='YOUR_API_KEY'

# Linux/Mac
export apikey='YOUR_API_KEY'
```

##### 사용법
```python
import tradingeconomics as te

# 환경 변수로 인증 (권장)
te.login()

# 또는 직접 인증
te.login('YOUR_API_KEY')

# 데이터 조회 (기본: 리스트)
data = te.getIndicatorData(country='mexico')

# Pandas DataFrame으로 조회
data = te.getIndicatorData(country='mexico', output_type='df')

# 여러 국가 조회
data = te.getIndicatorData(country=['mexico', 'sweden'], output_type='df')

# 캘린더 데이터
calendar = te.getCalendarData()

# 마켓 데이터
markets = te.getMarketsData(marketsField='commodities')

# 특정 심볼 조회
symbol_data = te.getMarketsBySymbol(symbols='aapl:us')

# 재무 데이터
financials = te.getFinancialsData(symbol='aapl:us', output_type='df')

# 히스토리컬 데이터
historical = te.getHistoricalData(country='mexico', indicator='gdp')
```

#### Node.js 패키지

##### 설치
```bash
npm install tradingeconomics
# 또는 글로벌 설치
npm install -g tradingeconomics
```

##### 환경 변수 설정 (권장)
```bash
apikey="YOUR_API_KEY" node app.js
```

##### 사용법
```javascript
const te = require('tradingeconomics');

// 환경 변수로 인증 (권장)
// 또는 직접 인증
te.login('YOUR_API_KEY');

// 히스토리컬 데이터
te.getHistoricalData(country='mexico', indicator='gdp')
    .then(function(data) {
        console.log(data);
    });

// 캘린더 데이터
te.getCalendar()
    .then(function(data) {
        console.log(data);
    });

// 수익 데이터
te.getEarnings(
    symbol='aapl:us',
    start_date='2016-01-01',
    end_date='2017-12-31'
)
.then((data) => {
    console.log(data);
})
.catch((err) => console.log(err));
```

---

## 📊 응답 데이터 포맷

API는 다양한 형식으로 데이터를 반환할 수 있습니다.

### 포맷 지정 방법
URL에 `&f=` 파라미터 추가:
- `&f=json` - JSON (기본값)
- `&f=csv` - CSV
- `&f=xml` - XML

### 예제
```
https://api.tradingeconomics.com/country/mexico?c=YOUR_API_KEY&f=xml
https://api.tradingeconomics.com/country/mexico?c=YOUR_API_KEY&f=csv
```

### JSON 응답 예제
```json
[
    {
        "Country": "Mexico",
        "Category": "Auto Exports",
        "Title": "Mexico Auto Exports",
        "LatestValueDate": "2023-08-31T00:00:00",
        "LatestValue": 287.85,
        "Source": "Instituto Nacional de Estadística y Geografía (INEGI)",
        "SourceURL": "https://www.inegi.org.mx/",
        "Unit": "Thousand Units",
        "URL": "/mexico/auto-exports",
        "CategoryGroup": "Trade",
        "Adjustment": "NSA",
        "Frequency": "Monthly",
        "HistoricalDataSymbol": "MEXICOAUTEXP",
        "CreateDate": "2019-07-23T12:20:00",
        "FirstValueDate": "1988-01-31T00:00:00",
        "PreviousValue": 275.77,
        "PreviousValueDate": "2023-07-31T00:00:00"
    }
]
```

### CSV 응답 예제
```csv
Country,Category,Title,LatestValueDate,LatestValue,Source,SourceURL,Unit,URL,CategoryGroup,Adjustment,Frequency,HistoricalDataSymbol,CreateDate,FirstValueDate,PreviousValue,PreviousValueDate
Mexico,Auto Exports,Mexico Auto Exports,8/31/2023 12:00:00 AM,287.85,Instituto Nacional de Estadística y Geografía (INEGI),https://www.inegi.org.mx/,Thousand Units,/mexico/auto-exports,Trade,NSA,Monthly,MEXICOAUTEXP,7/23/2019 12:20:00 PM,1/31/1988 12:00:00 AM,275.77,7/31/2023 12:00:00 AM
```

---

## 🔗 전체 엔드포인트 목록

### 1. 지표 (Indicators)

#### 국가별 지표 조회
```
GET /country/{country}
GET /country/{country}/{indicator}
GET /indicators
```
**예제:**
```python
# Python
te.getIndicatorData(country='mexico')
te.getIndicatorData(country=['mexico', 'sweden'], indicators='gdp')
te.getIndicatorData(calendar=1)  # 캘린더 이벤트가 있는 지표만
```

#### 신용 등급
```
GET /ratings
GET /ratings/{country}
```
**예제:**
```python
te.getRatings(country='united states')
te.getCreditRatings(country='portugal')
te.getHistoricalCreditRatings(country='spain')
```

#### 지표 변경사항
```
GET /changes
GET /changes/{start_date}
```
**예제:**
```python
te.getIndicatorChanges()
te.getIndicatorChanges(start_date='2024-10-01')
```

#### 최신 업데이트
```
GET /updates
GET /updates/country/{country}
GET /updates/country/{country}/{date}
GET /updates/{date}
```
**예제:**
```python
te.getLatestUpdates()
te.getLatestUpdates(country='united states')
te.getLatestUpdates(init_date='2021-06-01', time='15:20')
```

#### 중단된 지표
```
GET /country/all/discontinued
GET /country/{country}/discontinued
```
**예제:**
```python
te.getDiscontinuedIndicator()
te.getDiscontinuedIndicator(country=['united states', 'china'])
```

#### 카테고리별 지표
```
GET /country/{country}?group={category_group}
```
**예제:**
```python
te.getIndicatorByCategoryGroup(country='united states', category_group='gdp')
te.getIndicatorByCategoryGroup(country=['us', 'china'], category_group='markets')
```

#### 티커별 지표
```
GET /country/ticker/{ticker}
```
**예제:**
```python
te.getIndicatorByTicker(ticker='USURTOT')
te.getIndicatorByTicker(ticker=['WGDPCHIN', 'USURTOT'])
```

#### 피어 비교
```
GET /peers/{ticker}
GET /peers/country/{country}
GET /peers/country/{country}/{category}
```
**예제:**
```python
te.getPeers(ticker='CPI YOY')
te.getPeers(country='united states')
te.getPeers(country='united states', category='money')
```

#### 국가 목록
```
GET /country
```
**예제:**
```python
te.getAllCountries()
```

---

### 2. 히스토리컬 데이터 (Historical)

#### 국가/지표별 히스토리컬 데이터
```
GET /historical/country/{country}
GET /historical/country/{country}/indicator/{indicator}
GET /historical/country/{country}/indicator/{indicator}/{start_date}/{end_date}
```
**예제:**
```python
te.getHistoricalData(country='mexico', indicator='gdp')
te.getHistoricalData(country='mexico', indicator='gdp', 
                     initDate='2015-01-01', endDate='2020-01-01')
```

#### 티커별 히스토리컬 데이터
```
GET /historical/ticker/{ticker}
```
**예제:**
```python
te.getHistoricalByTicker(ticker='USURTOT')
```

#### 최신 히스토리컬 데이터
```
GET /historical/updates
```
**예제:**
```python
te.getHistoricalLatest()
```

#### 히스토리컬 등급
```
GET /historical/ratings/{country}
```
**예제:**
```python
te.getHistoricalRatings(country='portugal')
```

---

### 3. 경제 캘린더 (Calendar)

#### 캘린더 이벤트
```
GET /calendar
GET /calendar/country/{country}
GET /calendar/country/{country}/indicator/{indicator}
GET /calendar/country/{country}/{start_date}/{end_date}
GET /calendar/ticker/{ticker}
GET /calendar/country/{country}/event/{event}
```
**예제:**
```python
te.getCalendarData()
te.getCalendarData(country='united states')
te.getCalendarData(country='united states', indicator='initial jobless claims')
te.getCalendarData(initDate='2021-01-01', endDate='2021-01-03')
te.getCalendarData(importance='2')  # 중요도 필터
te.getCalendarData(ticker=['IJCUSA','SPAINFACORD'])
te.getCalendarData(country='united states', event='GDP Growth Rate QoQ Final GDP')
```

#### 캘린더 ID로 조회
```
GET /calendar/calendarid/{id}
```
**예제:**
```python
te.getCalendarId(id='174108')
te.getCalendarId(id=['174108','160025','160030'])
```

#### 캘린더 업데이트
```
GET /calendar/updates
```
**예제:**
```python
te.getCalendarUpdates()
```

#### 그룹별 캘린더 이벤트
```
GET /calendar/group/{group}
GET /calendar/country/{country}/group/{group}
```
**예제:**
```python
te.getCalendarEventsByGroup(group='bond')
te.getCalendarEventsByGroup(country='china', group='inflation')
```

#### 모든 캘린더 이벤트
```
GET /calendar/events
GET /calendar/events/country/{country}
```
**예제:**
```python
te.getCalendarEvents()
te.getCalendarEvents(country='china')
te.getCalendarEvents(country=['china', 'canada'])
```

---

### 4. 예측 (Forecasts)

#### 국가별 예측
```
GET /forecast/country/{country}
GET /forecast/country/{country}/indicator/{indicator}
```
**예제:**
```python
te.getForecastData(country='mexico')
te.getForecastData(country='mexico', indicator='gdp')
```

#### 티커별 예측
```
GET /forecast/ticker/{ticker}
```
**예제:**
```python
te.getForecastByTicker(ticker='USURTOT')
```

#### 예측 업데이트
```
GET /forecast/updates
```
**예제:**
```python
te.getForecastUpdates()
```

---

### 5. 마켓 데이터 (Markets)

#### 마켓 카테고리별 조회
```
GET /markets/commodities
GET /markets/currency
GET /markets/index
GET /markets/bond
GET /markets/crypto
```
**예제:**
```python
te.getMarketsData(marketsField='commodities')
te.getMarketsData(marketsField='currency')
te.getMarketsData(marketsField='bond', type='10Y')  # 채권 타입: 2Y, 5Y, 10Y, 15Y, 20Y, 30Y
```

#### 통화 크로스
```
GET /markets/currency?cross={cross}
```
**예제:**
```python
te.getCurrencyCross(cross='EUR')
```

#### 심볼별 마켓 데이터
```
GET /markets/symbol/{symbol}
```
**예제:**
```python
te.getMarketsBySymbol(symbols='aapl:us')
te.getMarketsBySymbol(symbols=['aapl:us', 'indu:ind'])
```

#### 인트라데이 데이터
```
GET /markets/intraday/{symbol}
GET /markets/intraday/{symbol}?d1={start}&d2={end}
GET /markets/intraday/{symbol}?agr={interval}
```
**예제:**
```python
te.getMarketsIntraday(symbols='indu:ind')
te.getMarketsIntraday(symbols='aapl:us', initDate='2022-01-01', endDate='2022-12-31')
te.getMarketsIntradayByInterval(symbol='CL1:COM', interval='1m', 
                                 initDate='2022-01-01', endDate='2022-12-01')
# 인터벌: 1m, 5m, 10m, 15m, 30m, 1h, 2h, 4h
```

#### 히스토리컬 마켓 데이터
```
GET /markets/historical/{symbol}
```
**예제:**
```python
te.fetchMarkets(symbol='aapl:us', initDate='2020-01-01', endDate='2021-01-01')
```

#### 마켓 피어
```
GET /markets/peers/{symbol}
```
**예제:**
```python
te.getMarketsPeers(symbols='indu:ind')
te.getMarketsPeers(symbols=['aapl:us', 'indu:ind'])
```

#### 마켓 컴포넌트
```
GET /markets/components/{symbol}
```
**예제:**
```python
te.getMarketsComponents(symbols='psi20:ind')
te.getMarketsComponents(symbols=['psi20:ind', 'indu:ind'])
```

#### 마켓 검색
```
GET /markets/search/{country}
GET /markets/search/{country}?category={category}
```
**예제:**
```python
te.getMarketsSearch(country='japan')
te.getMarketsSearch(country='japan', category='index')
te.getMarketsSearch(country='japan', category=['index', 'markets'], page=1)
```

#### 마켓 예측
```
GET /markets/forecasts
GET /markets/forecasts/{category}
GET /markets/forecasts/symbol/{symbol}
```
**예제:**
```python
te.getMarketsForecasts(category='bond')
te.getMarketsForecasts(symbol='indu:ind')
te.getMarketsForecasts(symbol=['psi20:ind', 'indu:ind'])
```

#### 주식 설명
```
GET /markets/stockdescriptions/symbol/{symbol}
GET /markets/stockdescriptions/country/{country}
```
**예제:**
```python
te.getMarketsStockDescriptions(symbol='AAPL:US')
te.getMarketsStockDescriptions(symbol=['AAPL:US','FB:US'])
te.getMarketsStockDescriptions(country='france')
```

#### 심볼로지 (Symbol Mapping)
```
GET /markets/symbology/symbol/{symbol}
GET /markets/symbology/ticker/{ticker}
GET /markets/symbology/isin/{isin}
GET /markets/symbology/country/{country}
```
**예제:**
```python
te.getMarketsSymbology(symbol='AAPL:US')
te.getMarketsSymbology(ticker='aapl')
te.getMarketsSymbology(isin='US0378331005')
te.getMarketsSymbology(country='United States')
```

#### 국가별 주식/마켓
```
GET /markets/stocks/country/{country}
GET /markets/country/{country}
```
**예제:**
```python
te.getStocksByCountry(country='United States')
te.getMarketsByCountry(country='United States')
```

---

### 6. 재무 데이터 (Financials)

#### 심볼별 재무 데이터
```
GET /financials/symbol/{symbol}
```
**예제:**
```python
te.getFinancialsData(symbol='aapl:us')
```

#### 카테고리별 재무 데이터
```
GET /financials/symbol/{symbol}/category/{category}
```
**예제:**
```python
te.getFinancialsDataByCategory(symbol='aapl:us', category='assets')
```

#### 재무 카테고리 목록
```
GET /financials/categories
```
**예제:**
```python
te.getFinancialsCategoryList()
```

#### 섹터 정보
```
GET /financials/sectors
```
**예제:**
```python
te.getSectors()
```

#### 히스토리컬 재무 데이터
```
GET /financials/historical/{symbol}
```
**예제:**
```python
te.getFinancialsHistorical(symbol='aapl:us')
```

---

### 7. 수익 (Earnings)

#### 수익 데이터
```
GET /earnings
GET /earnings/symbol/{symbol}
GET /earnings/symbol/{symbol}/{start_date}/{end_date}
```
**예제:**
```python
te.getEarnings()
te.getEarnings(symbol='aapl:us')
te.getEarnings(symbol='aapl:us', start_date='2016-01-01', end_date='2017-12-31')
```

#### 수익 타입별
```
GET /earnings/type/{type}
```
**예제:**
```python
te.getEarningsType(type='earnings')
```

---

### 8. 배당 (Dividends)

```
GET /dividends
GET /dividends/symbol/{symbol}
```
**예제:**
```python
te.getDividends()
te.getDividends(symbol='aapl:us')
```

---

### 9. IPO

```
GET /ipo
GET /ipo/country/{country}
```
**예제:**
```python
te.getIpo()
te.getIpo(country='united states')
```

---

### 10. 주식 분할 (Stock Splits)

```
GET /stock-splits
GET /stock-splits/symbol/{symbol}
```
**예제:**
```python
te.getStockSplits()
te.getStockSplits(symbol='aapl:us')
```

---

### 11. 뉴스 (News)

#### 뉴스 조회
```
GET /news
GET /news/country/{country}
GET /news/indicator/{indicator}
```
**예제:**
```python
te.getNews()
te.getNews(country='united states')
te.getNews(indicator='inflation')
```

#### 기사 조회
```
GET /articles
```
**예제:**
```python
te.getArticles()
```

#### 기사 ID로 조회
```
GET /articles/id/{id}
```
**예제:**
```python
te.getArticleId(id='12345')
```

---

### 12. 검색 (Search)

```
GET /search/{query}
```
**예제:**
```python
te.getSearch(query='inflation')
```

---

### 13. 세계은행 데이터 (World Bank)

#### 카테고리
```
GET /worldbank/categories
```
**예제:**
```python
te.getWBCategories()
```

#### 지표
```
GET /worldbank/indicator
```
**예제:**
```python
te.getWBIndicator()
```

#### 국가
```
GET /worldbank/country/{country}
```
**예제:**
```python
te.getWBCountry(country='mexico')
```

#### 히스토리컬 데이터
```
GET /worldbank/historical/{indicator}/{country}
```
**예제:**
```python
te.getWBHistorical(indicator='FR.INR.RINR', country='mexico')
```

---

### 14. UN Comtrade 데이터

#### 카테고리
```
GET /comtrade/categories
```
**예제:**
```python
te.getCmtCategories()
```

#### 국가
```
GET /comtrade/country/{country}
```
**예제:**
```python
te.getCmtCountry(country='portugal')
```

#### 히스토리컬 데이터
```
GET /comtrade/historical/{symbol}
```
**예제:**
```python
te.getCmtHistorical(symbol='PRTESP24031')
```

#### 두 국가 간 무역
```
GET /comtrade/country/{country1}/{country2}
```
**예제:**
```python
te.getCmtTwoCountries(country1='portugal', country2='spain')
```

#### 업데이트
```
GET /comtrade/updates
```
**예제:**
```python
te.getCmtUpdates()
```

#### 카테고리별 국가
```
GET /comtrade/country/{country}/category/{category}
```
**예제:**
```python
te.getCmtCountryByCategory(country='portugal', category='live animals')
```

#### 타입별 총계
```
GET /comtrade/type/{type}
```
**예제:**
```python
te.getCmtTotalByType(type='import')
```

#### 타입별 필터
```
GET /comtrade/country/{country}/type/{type}
```
**예제:**
```python
te.getCmtCountryFilterByType(country='portugal', type='import')
```

#### 스냅샷
```
GET /comtrade/snapshot/type/{type}
```
**예제:**
```python
te.getCmtSnapshotByType(type='import')
```

#### 최근 업데이트
```
GET /comtrade/lastupdates
```
**예제:**
```python
te.getCmtLastUpdates()
```

---

### 15. 연방준비제도 (Federal Reserve)

#### 주별 데이터
```
GET /federalreserve/states
```
**예제:**
```python
te.getFedRStates()
```

#### 스냅샷
```
GET /federalreserve/snapshots
```
**예제:**
```python
te.getFedRSnaps()
```

#### 히스토리컬 데이터
```
GET /federalreserve/historical/{symbol}
```
**예제:**
```python
te.getFedRHistorical(symbol='CCSA')
```

#### 카운티별 데이터
```
GET /federalreserve/county
```
**예제:**
```python
te.getFedRCounty()
```

---

### 16. Eurostat 데이터

#### Eurostat 데이터
```
GET /eurostat
```
**예제:**
```python
te.getEurostatData()
```

#### 국가 목록
```
GET /eurostat/countries
```
**예제:**
```python
te.getEurostatCountries()
```

#### 카테고리 그룹
```
GET /eurostat/categories
```
**예제:**
```python
te.getEurostatCategoryGroups()
```

#### 히스토리컬 데이터
```
GET /eurostat/historical/{symbol}
```
**예제:**
```python
te.getHistoricalEurostat(symbol='EUROSTAT_SYMBOL')
```

---

### 17. 스트리밍 (Streaming)

#### 실시간 데이터 스트리밍
```python
# Python
te.subscribe('calendar')  # 캘린더 이벤트 구독
te.run()
```

---

## 🐳 Docker 지원

### Python Docker
```bash
docker run -it --name te-python tradingeconomics-python:latest
```

### Node.js Docker
```bash
docker run --rm -it --init --name te-nodejs \
    -e apikey='YOUR_API_KEY' \
    tradingeconomics/nodejs:latest sh

# 예제 실행
node Calendar/events.js
node Indicators/historical.js
node Markets/marketForecast.js
```

---

## 📚 추가 리소스

### GitHub 저장소
- **API 예제**: https://github.com/tradingeconomics/tradingeconomics
- **Python 패키지**: https://github.com/tradingeconomics/tradingeconomics-python
- **Node.js 패키지**: https://github.com/tradingeconomics/tradingeconomics-js
- **Jupyter Notebooks**: https://github.com/tradingeconomics/notebooks

### 공식 문서
- **메인 문서**: https://docs.tradingeconomics.com/
- **API 정보**: https://tradingeconomics.com/analytics/api.aspx

### 지원 언어
- Python
- JavaScript/Node.js
- C#
- R
- Ruby
- Rust
- Go
- Java
- PHP
- TypeScript
- MATLAB

### 통합 도구
- Excel Add-In
- Google Sheets Add-On
- Tableau Plugin
- MATLAB Integration
- Chainlink Oracle (Blockchain)

---

## 🔒 보안 권장사항

### 1. 환경 변수 사용
API 키를 코드에 하드코딩하지 말고 환경 변수로 관리:

```python
import os
api_key = os.getenv('TRADINGECONOMICS_API_KEY')
```

```javascript
const api_key = process.env.TRADINGECONOMICS_API_KEY;
```

### 2. .gitignore 설정
API 키가 포함된 파일을 버전 관리에서 제외:
```
.env
config.json
credentials.json
```

### 3. 키 로테이션
정기적으로 API 키를 갱신하여 보안 유지

---

## 💡 사용 예시

### 여러 국가의 GDP 비교
```python
import tradingeconomics as te
te.login()

countries = ['mexico', 'united states', 'china', 'germany']
gdp_data = te.getHistoricalData(
    country=countries,
    indicator='gdp',
    output_type='df'
)
print(gdp_data)
```

### 실시간 경제 이벤트 모니터링
```javascript
const te = require('tradingeconomics');
te.login('YOUR_API_KEY');

// 오늘의 경제 이벤트
te.getCalendar()
    .then(events => {
        events.forEach(event => {
            console.log(`${event.Country}: ${event.Event} at ${event.Date}`);
        });
    });
```

### 상품 가격 추적
```python
import tradingeconomics as te
te.login()

# 원유, 금, 은 가격
commodities = te.getMarketsData(marketsField='commodities', output_type='df')
oil = commodities[commodities['Symbol'].str.contains('CL')]
gold = commodities[commodities['Symbol'].str.contains('GC')]
print(f"Oil: {oil['Last'].values[0]}")
print(f"Gold: {gold['Last'].values[0]}")
```

---

## ⚠️ 주의사항

1. **API 사용량 제한**: 플랜에 따라 요청 횟수 제한이 있습니다.
2. **데이터 지연**: 일부 데이터는 실시간이 아닐 수 있습니다.
3. **라이선스**: GPL-3.0 라이선스를 따릅니다.
4. **테스트 키**: `guest:guest`는 샘플 데이터만 반환합니다.

---

## 📞 지원

- **공식 웹사이트**: https://tradingeconomics.com/
- **API 문서**: https://docs.tradingeconomics.com/
- **GitHub Issues**: 각 저장소의 Issues 탭 활용
- **이메일 지원**: API 플랜 가입 시 제공

---

## 📄 라이선스

Trading Economics API 클라이언트 라이브러리는 GPL-3.0 라이선스 하에 배포됩니다.
