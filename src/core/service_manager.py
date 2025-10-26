"""
서비스 매니저 - 의존성 주입 및 서비스 관리
"""
from typing import Dict, Any, List
from core.base_parser import ParserFactory
from core.interfaces import HttpClientInterface
from parsers.http_client import HttpClient
# 파서들을 import하여 팩토리에 등록되도록 함
from parsers import ticker_parser, fnguide_parser, crypto_parser, market_parser, interest_parser, yahoo_parser, stock_quote_parser, crypto_ticker_parser, marketwatch_parser


class ServiceManager:
    """서비스 의존성 관리 클래스"""
    
    def __init__(self):
        self._http_client = HttpClient()
        self._parsers = {}
    
    @property
    def http_client(self) -> HttpClientInterface:
        return self._http_client
    
    def get_parser(self, parser_type: str):
        """파서 인스턴스 반환 (싱글톤)"""
        if parser_type not in self._parsers:
            self._parsers[parser_type] = ParserFactory.create_parser(
                parser_type, self._http_client
            )
        return self._parsers[parser_type]
    
    def search_domestic_ticker(self, query: str) -> Dict[str, Any]:
        """국내 티커 검색"""
        parser = self.get_parser('ticker')
        return parser.search_domestic(query)
    
    def search_overseas_ticker(self, query: str) -> List[Dict[str, str]]:
        """해외 티커 검색 (Yahoo Finance)"""
        parser = self.get_parser('yahoo')
        return parser.search_overseas_ticker(query)
    
    def search_multiple_domestic_tickers(self, queries: List[str]) -> Dict[str, List[Dict[str, str]]]:
        """복수 국내 티커 검색"""
        results = {}
        for query in queries:
            results[query] = self.search_domestic_ticker(query)
        return results
    
    def search_multiple_overseas_tickers(self, queries: List[str]) -> Dict[str, List[Dict[str, str]]]:
        """복수 해외 티커 검색"""
        results = {}
        for query in queries:
            results[query] = self.search_overseas_ticker(query)
        return results
    
    def search_multiple_crypto_tickers(self, queries: List[str]) -> Dict[str, List[Dict[str, str]]]:
        """복수 암호화폐 티커 검색"""
        results = {}
        for query in queries:
            results[query] = self.search_crypto_ticker(query)
        return results
    
    def get_stock_snapshot(self, ticker: str) -> str:
        """주식 스냅샷 조회"""
        parser = self.get_parser('fnguide')
        return parser.get_snapshot(ticker)
    
    def get_company_overview(self, ticker: str) -> str:
        """기업 개요 조회"""
        parser = self.get_parser('fnguide')
        return parser.get_company_overview(ticker)
    
    def get_financial_statements(self, ticker: str) -> str:
        """재무제표 조회"""
        parser = self.get_parser('fnguide')
        return parser.get_financial_statements(ticker)
    
    def get_financial_ratios(self, ticker: str) -> str:
        """재무비율 조회"""
        parser = self.get_parser('fnguide')
        return parser.get_financial_ratios(ticker)
    
    def get_investment_indicators(self, ticker: str) -> str:
        """투자지표 조회"""
        parser = self.get_parser('fnguide')
        return parser.get_investment_indicators(ticker)
    
    def get_analyst_consensus(self, ticker: str) -> str:
        """애널리스트 컨센서스 조회"""
        parser = self.get_parser('fnguide')
        return parser.get_analyst_consensus(ticker)
    
    def get_ownership_analysis(self, ticker: str) -> str:
        """지분 분석 조회"""
        parser = self.get_parser('fnguide')
        return parser.get_ownership_analysis(ticker)
    
    def get_industry_analysis(self, ticker: str) -> str:
        """업종 분석 조회"""
        parser = self.get_parser('fnguide')
        return parser.get_industry_analysis(ticker)
    
    def get_competitor_comparison(self, ticker: str) -> str:
        """경쟁사 비교 조회"""
        parser = self.get_parser('fnguide')
        return parser.get_competitor_comparison(ticker)
    
    def get_exchange_disclosures(self, ticker: str) -> str:
        """거래소 공시 조회"""
        parser = self.get_parser('fnguide')
        return parser.get_exchange_disclosures(ticker)
    
    def get_earnings_reports(self, ticker: str) -> str:
        """실적 보고서 조회"""
        parser = self.get_parser('fnguide')
        return parser.get_earnings_reports(ticker)
    
    def get_crypto_data(self) -> str:
        """암호화폐 데이터 조회"""
        parser = self.get_parser('crypto')
        return parser.get_crypto_data()
    
    def get_market_indices(self) -> str:
        """주요 지수 정보 조회"""
        parser = self.get_parser('market')
        return parser.get_market_indices()
    
    def get_sector_performance(self) -> str:
        """업종별 등락률 조회"""
        parser = self.get_parser('market')
        return parser.get_sector_performance()
    
    def get_top_gainers(self) -> str:
        """상승률 상위 종목 조회"""
        parser = self.get_parser('market')
        return parser.get_top_gainers()
    
    def get_top_losers(self) -> str:
        """하락률 상위 종목 조회"""
        parser = self.get_parser('market')
        return parser.get_top_losers()
    
    def get_volume_leaders(self) -> str:
        """거래량 상위 종목 조회"""
        parser = self.get_parser('market')
        return parser.get_volume_leaders()
    
    def get_interest_rates(self) -> str:
        """기준금리 및 주요 금리 조회"""
        parser = self.get_parser('interest')
        return parser.get_interest_rates()
    
    def get_bond_yields(self) -> str:
        """국고채 수익률 조회"""
        parser = self.get_parser('interest')
        return parser.get_bond_yields()
    
    def get_cd_rates(self) -> str:
        """CD금리 조회"""
        parser = self.get_parser('interest')
        return parser.get_cd_rates()
    
    def get_corporate_bonds(self) -> str:
        """회사채 수익률 조회"""
        parser = self.get_parser('interest')
        return parser.get_corporate_bonds()
    
    def get_global_indices(self) -> str:
        """글로벌 주요 지수 조회"""
        parser = self.get_parser('yahoo')
        return parser.get_global_indices()
    
    def get_us_treasury_yields(self) -> str:
        """미국 국채 수익률 조회"""
        parser = self.get_parser('yahoo')
        return parser.get_us_treasury_yields()
    
    def get_vix_data(self) -> str:
        """VIX 공포지수 조회"""
        parser = self.get_parser('yahoo')
        return parser.get_vix_data()
    
    def get_commodities(self) -> str:
        """글로벌 원자재 가격 조회"""
        parser = self.get_parser('yahoo')
        return parser.get_commodities()
    
    def get_forex_majors(self) -> str:
        """주요 환율 조회"""
        parser = self.get_parser('yahoo')
        return parser.get_forex_majors()
    
    def get_asian_indices(self) -> str:
        """아시아 주요 지수 조회"""
        parser = self.get_parser('yahoo')
        return parser.get_asian_indices()
    
    def get_european_indices(self) -> str:
        """유럽 주요 지수 조회"""
        parser = self.get_parser('yahoo')
        return parser.get_european_indices()
    
    def get_yahoo_sector_performance(self) -> str:
        """섹터별 성과 조회"""
        parser = self.get_parser('yahoo')
        return parser.get_sector_performance()
    
    def get_stock_quote(self, symbol: str) -> str:
        """개별 주식 정보 조회 (Yahoo Finance)"""
        parser = self.get_parser('yahoo')
        return parser.get_stock_quote(symbol)
    
    def get_domestic_stock_quote(self, ticker: str) -> str:
        """국내 개별 주식 정보 조회"""
        parser = self.get_parser('stock_quote')
        return parser.get_domestic_stock_quote(ticker)
    
    def get_crypto_quote(self, symbol: str) -> str:
        """개별 암호화폐 정보 조회"""
        parser = self.get_parser('yahoo')
        return parser.get_crypto_quote(symbol)
    
    def get_multiple_stock_quotes(self, symbols: List[str]) -> Dict[str, str]:
        """복수 해외 주식 정보 조회"""
        parser = self.get_parser('yahoo')
        return parser.get_multiple_stock_quotes(symbols)
    
    def get_multiple_domestic_stock_quotes(self, tickers: List[str]) -> Dict[str, str]:
        """복수 국내 주식 정보 조회"""
        parser = self.get_parser('stock_quote')
        return parser.get_multiple_domestic_stock_quotes(tickers)
    
    def get_multiple_crypto_quotes(self, symbols: List[str]) -> Dict[str, str]:
        """복수 암호화폐 정보 조회"""
        parser = self.get_parser('yahoo')
        return parser.get_multiple_crypto_quotes(symbols)
    
    def search_crypto_ticker(self, query: str) -> List[Dict[str, str]]:
        """암호화폐 티커 검색"""
        parser = self.get_parser('crypto_ticker')
        return parser.search_crypto_ticker(query)
    
    def get_top_cryptos(self, limit: int = 20, currency: str = 'krw') -> List[Dict[str, str]]:
        """상위 암호화폐 목록 조회"""
        parser = self.get_parser('crypto_ticker')
        return parser.get_top_cryptos(limit, currency)
    
    def get_overseas_disclosures(self, symbol: str) -> str:
        """해외주식 공시정보 조회 (MarketWatch)"""
        parser = self.get_parser('marketwatch')
        return parser.get_overseas_disclosures(symbol)


# 전역 서비스 매니저 인스턴스
service_manager = ServiceManager()