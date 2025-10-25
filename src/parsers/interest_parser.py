"""
금리 및 채권 정보 파싱을 위한 유틸리티 모듈
"""
import logging
import re
from typing import Dict, Any, List, Optional
from lxml import html
from core.base_parser import WebParserBase, ParserFactory
from core.interfaces import HttpClientInterface, ParserInterface


class InterestParserInterface(ParserInterface):
    """금리 파서 인터페이스"""
    
    def get_interest_rates(self) -> str:
        pass
    
    def get_bond_yields(self) -> str:
        pass


class InterestParser(WebParserBase, InterestParserInterface):
    """네이버 금융 금리 및 채권 정보 파싱 클래스"""
    
    BASE_URL = "https://finance.naver.com/marketindex/"
    LINK_PATTERN = r'\(/marketindex/interestDetail\.naver\?marketindexCd=[^)]+\)'
    
    def __init__(self, http_client: HttpClientInterface):
        super().__init__(http_client)
    
    def parse(self, *args, **kwargs) -> Dict[str, Any]:
        return {
            "interest_rates": self.get_interest_rates(),
            "bond_yields": self.get_bond_yields()
        }
    
    def _find_table_by_keyword(self, tree: html.HtmlElement, keyword: str) -> Optional[html.HtmlElement]:
        """키워드로 테이블 찾기"""
        tables = tree.xpath('//table')
        for table in tables:
            if keyword in table.text_content():
                return table
        return None
    
    def _extract_and_clean_table(self, table: html.HtmlElement) -> str:
        """테이블 추출 및 정리"""
        html_str = html.tostring(table, encoding='unicode')
        result = self.http_client.html_to_markdown(html_str)
        return re.sub(self.LINK_PATTERN, '', result)
    
    def _filter_lines(self, text: str, keywords: List[str]) -> str:
        """키워드로 라인 필터링"""
        lines = text.split('\n')
        filtered_lines = [line for line in lines if any(keyword in line for keyword in keywords)]
        return '\n'.join(filtered_lines) if filtered_lines else text
    
    def _parse_interest_data(self, keyword: str, filter_keywords: Optional[List[str]] = None) -> str:
        """공통 금리 데이터 파싱 로직"""
        try:
            tree = self.http_client.fetch_euc_kr(self.BASE_URL)
            if tree is None:
                return ""
            
            table = self._find_table_by_keyword(tree, keyword)
            if table is None:
                return ""
            
            result = self._extract_and_clean_table(table)
            
            if filter_keywords:
                result = self._filter_lines(result, filter_keywords)
            
            return result
        except Exception as e:
            logging.error(f"{keyword} 파싱 실패: {e}")
            return ""
    
    def get_interest_rates(self) -> str:
        """기준금리 및 주요 금리 정보 조회"""
        try:
            tree = self.http_client.fetch_euc_kr(self.BASE_URL)
            if tree is None:
                return ""
            
            table = self._find_table_by_keyword(tree, '금리')
            if table is not None and 'CD금리' in table.text_content():
                return self._extract_and_clean_table(table)
            return ""
        except Exception as e:
            logging.error(f"금리 정보 파싱 실패: {e}")
            return ""
    
    def get_bond_yields(self) -> str:
        """국고채 수익률 및 채권 정보 조회"""
        return self._parse_interest_data('국고채', ['국고채', '구분', '금리', '등락률'])
    
    def get_cd_rates(self) -> str:
        """CD금리 정보 조회"""
        return self._parse_interest_data('CD금리', ['CD금리', '구분', '금리', '등락률'])
    
    def get_corporate_bonds(self) -> str:
        """회사채 수익률 정보 조회"""
        return self._parse_interest_data('회사채', ['회사채', '구분', '금리', '등락률'])


# 팩토리에 파서 등록
ParserFactory.register_parser('interest', InterestParser)