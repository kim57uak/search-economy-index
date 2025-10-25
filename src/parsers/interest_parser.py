"""
금리 및 채권 정보 파싱을 위한 유틸리티 모듈
"""
import logging
from typing import Dict, Any
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
    
    def __init__(self, http_client: HttpClientInterface):
        super().__init__(http_client)
    
    def parse(self, *args, **kwargs) -> Dict[str, Any]:
        return {
            "interest_rates": self.get_interest_rates(),
            "bond_yields": self.get_bond_yields()
        }
    
    def get_interest_rates(self) -> str:
        """기준금리 및 주요 금리 정보 조회"""
        try:
            url = "https://finance.naver.com/marketindex/?tabSel=interest#tab_section"
            tree = self.http_client.fetch_euc_kr(url)
            if tree is not None:
                return self._extract_element(tree, '//*[@id="content"]') or ""
            return ""
        except Exception as e:
            logging.error(f"금리 정보 파싱 실패: {e}")
            return ""
    
    def get_bond_yields(self) -> str:
        """국고채 수익률 및 채권 정보 조회"""
        try:
            url = "https://finance.naver.com/marketindex/bondDayList.naver?bondType=A"
            tree = self.http_client.fetch_euc_kr(url)
            if tree is not None:
                return self._extract_element(tree, '//*[@id="contentarea"]') or ""
            return ""
        except Exception as e:
            logging.error(f"채권 수익률 파싱 실패: {e}")
            return ""
    
    def get_cd_rates(self) -> str:
        """CD금리 정보 조회"""
        try:
            url = "https://finance.naver.com/marketindex/interestDayList.naver?marketindexCd=IRR_CD91&page=1"
            tree = self.http_client.fetch_euc_kr(url)
            if tree is not None:
                return self._extract_element(tree, '//*[@id="contentarea"]') or ""
            return ""
        except Exception as e:
            logging.error(f"CD금리 파싱 실패: {e}")
            return ""
    
    def get_corporate_bonds(self) -> str:
        """회사채 수익률 정보 조회"""
        try:
            url = "https://finance.naver.com/marketindex/bondDayList.naver?bondType=B"
            tree = self.http_client.fetch_euc_kr(url)
            if tree is not None:
                return self._extract_element(tree, '//*[@id="contentarea"]') or ""
            return ""
        except Exception as e:
            logging.error(f"회사채 수익률 파싱 실패: {e}")
            return ""


# 팩토리에 파서 등록
ParserFactory.register_parser('interest', InterestParser)