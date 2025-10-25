"""
FnGuide 사이트 파싱을 위한 유틸리티 모듈
"""

import logging
from typing import Dict, Any
from core.base_parser import BaseFnGuideParser, ParserFactory
from core.interfaces import HttpClientInterface


class FnGuideParser(BaseFnGuideParser):
    """FnGuide 금융 정보 파싱 클래스"""

    def __init__(self, http_client: HttpClientInterface):
        super().__init__(http_client)

    def _fetch_page(self, endpoint: str, ticker: str) -> str:
        """페이지를 가져와서 파싱합니다."""
        try:
            url = self._build_url(endpoint, ticker)
            tree = self.http_client.fetch_utf8(url)
            if tree is not None:
                result = self._extract_element(tree, '//*[@id="compBody"]') or ""
                return self._clean_fnguide_content(result)
            return ""
        except Exception as e:
            logging.error(f"페이지 파싱 실패: {e}")
            return ""

    def _fetch_disclosure(self, ticker: str) -> str:
        """거래소공시 페이지를 파싱합니다."""
        try:
            url = self._build_url("SVD_Disclosure.asp", ticker)
            tree = self.http_client.fetch_utf8(url)
            if tree is not None:
                result = self._extract_element(tree, '//*[@id="compBody"]/div[2]') or ""
                return self._clean_fnguide_content(result)
            return ""
        except Exception as e:
            logging.error(f"거래소공시 파싱 실패: {e}")
            return ""

    def get_snapshot(self, ticker: str) -> str:
        """스냅샷 정보 조회"""
        return self._fetch_page("SVD_Main.asp", ticker)

    def get_company_overview(self, ticker: str) -> str:
        """기업개요 정보 조회"""
        return self._fetch_page("SVD_Corp.asp", ticker)

    def get_financial_statements(self, ticker: str) -> str:
        """재무제표 정보 조회"""
        return self._fetch_page("SVD_Finance.asp", ticker)

    def get_financial_ratios(self, ticker: str) -> str:
        """재무비율 정보 조회"""
        return self._fetch_page("SVD_FinanceRatio.asp", ticker)

    def get_investment_indicators(self, ticker: str) -> str:
        """투자지표 정보 조회"""
        return self._fetch_page("SVD_Invest.asp", ticker)

    def get_analyst_consensus(self, ticker: str) -> str:
        """컨센서스 정보 조회"""
        return self._fetch_page("SVD_Consensus.asp", ticker)

    def get_ownership_analysis(self, ticker: str) -> str:
        """지분분석 정보 조회"""
        return self._fetch_page("SVD_shareanalysis.asp", ticker)

    def get_industry_analysis(self, ticker: str) -> str:
        """업종분석 정보 조회"""
        return self._fetch_page("SVD_ujanal.asp", ticker)

    def get_competitor_comparison(self, ticker: str) -> str:
        """경쟁사비교 정보 조회"""
        return self._fetch_page("SVD_Comparison.asp", ticker)

    def get_exchange_disclosures(self, ticker: str) -> str:
        """거래소공시 정보 조회"""
        return self._fetch_disclosure(ticker)

    def get_earnings_reports(self, ticker: str) -> str:
        """실적속보 정보 조회"""
        return self._fetch_page("SVD_ProResultCorp.asp", ticker)
    
    def _clean_fnguide_content(self, content: str) -> str:
        """FnGuide 콘텐츠에서 불필요한 패턴 제거"""
        import re
        if not content:
            return ""
        
        # JavaScript 패턴 제거
        content = re.sub(r'\(javascript:[^)]*\)', '', content)
        # ASP 파일 URL 패턴 제거
        content = re.sub(r'\([^)]*\.asp\?[^)]*\)', '', content)
        # goHompage JavaScript 패턴 제거
        content = re.sub(r'\(javascript:goHompage\([^)]*\)\)', '', content)
        
        return content


# 팩토리에 파서 등록
ParserFactory.register_parser('fnguide', FnGuideParser)