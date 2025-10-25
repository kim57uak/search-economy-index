"""
FnGuide 사이트 파싱을 위한 유틸리티 모듈
"""

import logging
import re
from typing import Dict, Any
from lxml import html
import requests
from markdownify import markdownify as md

try:
    import chardet
except ImportError:
    chardet = None


class FnGuideParser:
    """FnGuide 금융 정보 파싱 클래스"""

    BASE_URL = "https://comp.fnguide.com/SVO2/ASP"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Charset": "UTF-8",
            }
        )



    def _fetch_page(self, endpoint: str, ticker: str) -> str:
        """페이지를 가져와서 파싱합니다."""
        try:
            url = self._build_url(endpoint, ticker)
            tree = self.http_client.fetch_utf8(url)
            if tree is not None:
                return self._extract_element(tree, '//*[@id="compBody"]') or ""
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
                return self._extract_element(tree, '//*[@id="compBody"]/div[2]') or ""
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


# 팩토리에 파서 등록
ParserFactory.register_parser('fnguide', FnGuideParser)
