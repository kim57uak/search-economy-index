"""
서비스 매니저 - 의존성 주입 및 서비스 관리
"""
from typing import Dict, Any
from core.base_parser import ParserFactory
from core.interfaces import HttpClientInterface
from parsers.http_client import HttpClient
# 파서들을 import하여 팩토리에 등록되도록 함
from parsers import ticker_parser, fnguide_parser, crypto_parser, market_parser


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
    
    def search_overseas_ticker(self, query: str) -> Dict[str, Any]:
        """해외 티커 검색"""
        parser = self.get_parser('ticker')
        return parser.search_overseas(query)
    
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


# 전역 서비스 매니저 인스턴스
service_manager = ServiceManager()