"""
시장 지표 정보 파싱을 위한 유틸리티 모듈
"""
import logging
import re
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
    
    LINK_PATTERN = r'\(/item/main\.naver\?code=\d+\)'
    
    def __init__(self, http_client: HttpClientInterface):
        super().__init__(http_client)
    
    def parse(self, *args, **kwargs) -> Dict[str, Any]:
        return {
            "market_indices": self.get_market_indices(),
            "sector_performance": self.get_sector_performance(),
            "top_gainers": self.get_top_gainers()
        }
    
    def _fetch_and_extract(self, url: str, xpath: str) -> str:
        """공통 데이터 추출 로직"""
        try:
            tree = self.http_client.fetch_euc_kr(url)
            if tree is not None:
                return self._extract_element(tree, xpath) or ""
            return ""
        except Exception as e:
            logging.error(f"데이터 추출 실패 ({url}): {e}")
            return ""
    
    def _clean_market_data(self, data: str, max_lines: int = 30) -> str:
        """시장 데이터 정리 및 최적화"""
        if not data:
            return ""
        
        # 불필요한 링크 패턴 제거
        data = re.sub(self.LINK_PATTERN, '', data)
        
        lines = data.split('\n')
        cleaned_lines = []
        
        for line in lines:
            if self._should_skip_line(line):
                continue
            if self._is_valid_market_line(line):
                cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines[:max_lines])
    
    def _should_skip_line(self, line: str) -> bool:
        """스킵할 라인 판단"""
        stripped = line.strip()
        return (stripped == '|  | | | | | | | | | | | |' or 
                stripped == '|  | | | | | | | | |' or 
                not stripped)
    
    def _is_valid_market_line(self, line: str) -> bool:
        """유효한 시장 데이터 라인 판단"""
        return ('|' in line and 
                any(keyword in line for keyword in ['상승', '하락', '종목명', 'N']))
    
    def get_market_indices(self) -> str:
        """주요 지수 정보 조회 (KOSPI, KOSDAQ, 코스피200)"""
        return self._fetch_and_extract(
            "https://finance.naver.com/sise/", 
            '//*[@id="content"]/div[2]'
        )
    
    def get_sector_performance(self) -> str:
        """업종별 등락률 정보 조회"""
        result = self._fetch_and_extract(
            "https://finance.naver.com/sise/sise_group.naver?type=upjong",
            '//*[@id="contentarea"]'
        )
        return self._clean_market_data(result, 50)
    
    def get_top_gainers(self) -> str:
        """상승률 상위 종목 조회"""
        result = self._fetch_and_extract(
            "https://finance.naver.com/sise/sise_rise.naver",
            '//*[@id="contentarea"]/div[3]/table'
        )
        return self._clean_market_data(result, 25)
    
    def get_top_losers(self) -> str:
        """하락률 상위 종목 조회"""
        result = self._fetch_and_extract(
            "https://finance.naver.com/sise/sise_fall.naver",
            '//*[@id="contentarea"]/div[3]/table'
        )
        return self._clean_market_data(result, 25)
    
    def get_volume_leaders(self) -> str:
        """거래량 상위 종목 조회"""
        result = self._fetch_and_extract(
            "https://finance.naver.com/sise/sise_quant.naver",
            '//*[@id="contentarea"]/div[3]/table'
        )
        return self._clean_market_data(result, 25)


# 팩토리에 파서 등록
ParserFactory.register_parser('market', MarketParser)