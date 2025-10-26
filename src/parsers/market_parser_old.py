"""
시장 지표 정보 파싱을 위한 유틸리티 모듈
"""
import logging
from typing import Dict, Any
from core.base_parser import WebParserBase, ParserFactory
from core.interfaces import HttpClientInterface, ParserInterface


class MarketParserInterface(ParserInterface):
    """시장 파서 인터페이스"""
    
    def get_market_indices(self) -> str:
        pass
    
    def get_sector_performance(self) -> str:
        pass
    
    def get_top_gainers(self) -> str:
        pass


class MarketParser(WebParserBase, MarketParserInterface):
    """네이버 금융 시장 지표 파싱 클래스"""
    
    def __init__(self, http_client: HttpClientInterface):
        super().__init__(http_client)
    
    def parse(self, *args, **kwargs) -> Dict[str, Any]:
        return {
            "market_indices": self.get_market_indices(),
            "sector_performance": self.get_sector_performance(),
            "top_gainers": self.get_top_gainers()
        }
    
    def get_market_indices(self) -> str:
        """주요 지수 정보 조회 (KOSPI, KOSDAQ, 코스피200)"""
        try:
            url = "https://finance.naver.com/sise/"
            tree = self.http_client.fetch_euc_kr(url)
            if tree is not None:
                return self._extract_element(tree, '//*[@id="content"]/div[2]') or ""
            return ""
        except Exception as e:
            logging.error(f"시장 지수 파싱 실패: {e}")
            return ""
    
    def get_sector_performance(self) -> str:
        """업종별 등락률 정보 조회"""
        try:
            url = "https://finance.naver.com/sise/sise_group.naver?type=upjong"
            tree = self.http_client.fetch_euc_kr(url)
            if tree is not None:
                return self._extract_element(tree, '//*[@id="contentarea"]') or ""
            return ""
        except Exception as e:
            logging.error(f"업종별 등락률 파싱 실패: {e}")
            return ""
    
    def get_top_gainers(self) -> str:
        """상승률 상위 종목 조회"""
        try:
            url = "https://finance.naver.com/sise/sise_rise.naver"
            tree = self.http_client.fetch_euc_kr(url)
            if tree is not None:
                return self._extract_element(tree, '//*[@id="contentarea"]/div[3]/table/tbody/tr[position()<=50]') or ""
            return ""
        except Exception as e:
            logging.error(f"상승률 상위 종목 파싱 실패: {e}")
            return ""
    
    def get_top_losers(self) -> str:
        """하락률 상위 종목 조회"""
        try:
            url = "https://finance.naver.com/sise/sise_fall.naver"
            tree = self.http_client.fetch_euc_kr(url)
            if tree is not None:
                return self._extract_element(tree, '//*[@id="contentarea"]/div[3]/table/tbody/tr[position()<=50]') or ""
            return ""
        except Exception as e:
            logging.error(f"하락률 상위 종목 파싱 실패: {e}")
            return ""
    
    def get_volume_leaders(self) -> str:
        """거래량 상위 종목 조회"""
        try:
            url = "https://finance.naver.com/sise/sise_volume.naver"
            tree = self.http_client.fetch_euc_kr(url)
            if tree is not None:
                return self._extract_element(tree, '//*[@id="contentarea"]/div[3]/table/tbody/tr[position()<=50]') or ""
            return ""
        except Exception as e:
            logging.error(f"거래량 상위 종목 파싱 실패: {e}")
            return ""


# 팩토리에 파서 등록
ParserFactory.register_parser('market', MarketParser)