"""
파서 기본 클래스 및 팩토리 패턴 구현
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from lxml import html
from core.interfaces import HttpClientInterface, ParserInterface, WebParserBase


class TickerParserInterface(ParserInterface):
    """티커 파서 인터페이스"""
    
    @abstractmethod
    def search_domestic(self, query: str) -> List[Dict[str, str]]:
        pass
    
    @abstractmethod
    def search_overseas(self, query: str) -> List[Dict[str, str]]:
        pass


class FnGuideParserInterface(ParserInterface):
    """FnGuide 파서 인터페이스"""
    
    @abstractmethod
    def get_snapshot(self, ticker: str) -> str:
        pass
    
    @abstractmethod
    def get_company_overview(self, ticker: str) -> str:
        pass
    
    @abstractmethod
    def get_financial_statements(self, ticker: str) -> str:
        pass


class ParserFactory:
    """파서 팩토리 클래스"""
    
    _parsers = {}
    
    @classmethod
    def register_parser(cls, parser_type: str, parser_class):
        cls._parsers[parser_type] = parser_class
    
    @classmethod
    def create_parser(cls, parser_type: str, http_client: HttpClientInterface):
        if parser_type not in cls._parsers:
            raise ValueError(f"Unknown parser type: {parser_type}")
        return cls._parsers[parser_type](http_client)


class BaseTickerParser(WebParserBase, TickerParserInterface):
    """티커 파서 기본 클래스"""
    
    def __init__(self, http_client: HttpClientInterface):
        super().__init__(http_client)
    
    def parse(self, query: str) -> Dict[str, Any]:
        return {
            "domestic": self.search_domestic(query),
            "overseas": self.search_overseas(query)
        }


class BaseFnGuideParser(WebParserBase, FnGuideParserInterface):
    """FnGuide 파서 기본 클래스"""
    
    BASE_URL = "https://comp.fnguide.com/SVO2/ASP"
    
    def __init__(self, http_client: HttpClientInterface):
        super().__init__(http_client)
    
    def parse(self, ticker: str, method: str) -> str:
        method_map = {
            'snapshot': self.get_snapshot,
            'overview': self.get_company_overview,
            'financials': self.get_financial_statements
        }
        return method_map.get(method, self.get_snapshot)(ticker)
    
    def _build_url(self, endpoint: str, ticker: str) -> str:
        return f"{self.BASE_URL}/{endpoint}?pGB=1&gicode=A{ticker}&cID=&MenuYn=Y&ReportGB=&NewMenuID=101&stkGb=701"