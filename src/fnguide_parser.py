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

    def _html_to_markdown(self, html_content: str) -> str:
        """HTML을 마크다운으로 변환합니다."""
        if not html_content:
            return ""
        # HTML을 마크다운으로 변환
        markdown = md(html_content, heading_style="ATX")
        # 불필요한 공백 정리
        markdown = re.sub(r"\n\s*\n\s*\n", "\n\n", markdown)
        return markdown.strip()

    def _fetch_page(self, url: str) -> str:
        """페이지를 가져와서 파싱합니다."""
        try:
            response = self.session.get(url)
            response.raise_for_status()

            # 한글 인코딩 처리
            if chardet and (
                response.encoding is None
                or response.encoding.lower() in ["iso-8859-1", "ascii"]
            ):
                detected = chardet.detect(response.content)
                if detected["encoding"]:
                    response.encoding = detected["encoding"]
                else:
                    response.encoding = "utf-8"
            elif response.encoding is None:
                response.encoding = "utf-8"

            tree = html.fromstring(
                response.content, parser=html.HTMLParser(encoding=response.encoding)
            )

            comp_body = tree.xpath('//*[@id="compBody"]')
            if comp_body:
                # HTML 요소를 문자열로 변환 후 마크다운으로 변환
                html_content = html.tostring(comp_body[0], encoding='unicode')
                return self._html_to_markdown(html_content)
            return ""
        except Exception as e:
            logging.error(f"페이지 파싱 실패 {url}: {e}")
            return ""

    def _fetch_disclosure(self, url: str) -> str:
        """거래소공시 페이지를 파싱합니다."""
        try:
            response = self.session.get(url)
            response.raise_for_status()

            # 한글 인코딩 처리
            if chardet and (
                response.encoding is None
                or response.encoding.lower() in ["iso-8859-1", "ascii"]
            ):
                detected = chardet.detect(response.content)
                if detected["encoding"]:
                    response.encoding = detected["encoding"]
                else:
                    response.encoding = "utf-8"
            elif response.encoding is None:
                response.encoding = "utf-8"

            tree = html.fromstring(
                response.content, parser=html.HTMLParser(encoding=response.encoding)
            )

            disclosure_elem = tree.xpath('//*[@id="compBody"]/div[2]')
            if disclosure_elem:
                # HTML 요소를 문자열로 변환 후 마크다운으로 변환
                html_content = html.tostring(disclosure_elem[0], encoding='unicode')
                return self._html_to_markdown(html_content)
            return ""
        except Exception as e:
            logging.error(f"거래소공시 파싱 실패 {url}: {e}")
            return ""

    def get_snapshot(self, ticker: str) -> str:
        """스냅샷 정보 조회"""
        url = f"{self.BASE_URL}/SVD_Main.asp?pGB=1&gicode=A{ticker}&cID=&MenuYn=Y&ReportGB=&NewMenuID=101&stkGb=701"
        return self._fetch_page(url)

    def get_company_overview(self, ticker: str) -> str:
        """기업개요 정보 조회"""
        url = f"{self.BASE_URL}/SVD_Corp.asp?pGB=1&gicode=A{ticker}&cID=&MenuYn=Y&ReportGB=&NewMenuID=102&stkGb=701"
        return self._fetch_page(url)

    def get_financial_statement(self, ticker: str) -> str:
        """재무제표 정보 조회"""
        url = f"{self.BASE_URL}/SVD_Finance.asp?pGB=1&gicode=A{ticker}&cID=&MenuYn=Y&ReportGB=&NewMenuID=103&stkGb=701"
        return self._fetch_page(url)

    def get_financial_ratio(self, ticker: str) -> str:
        """재무비율 정보 조회"""
        url = f"{self.BASE_URL}/SVD_FinanceRatio.asp?pGB=1&gicode=A{ticker}&cID=&MenuYn=Y&ReportGB=&NewMenuID=104&stkGb=701"
        return self._fetch_page(url)

    def get_investment_indicator(self, ticker: str) -> str:
        """투자지표 정보 조회"""
        url = f"{self.BASE_URL}/SVD_Invest.asp?pGB=1&gicode=A{ticker}&cID=&MenuYn=Y&ReportGB=&NewMenuID=105&stkGb=701"
        return self._fetch_page(url)

    def get_consensus(self, ticker: str) -> str:
        """컨센서스 정보 조회"""
        url = f"{self.BASE_URL}/SVD_Consensus.asp?pGB=1&gicode=A{ticker}&cID=&MenuYn=Y&ReportGB=&NewMenuID=108&stkGb=701"
        return self._fetch_page(url)

    def get_share_analysis(self, ticker: str) -> str:
        """지분분석 정보 조회"""
        url = f"{self.BASE_URL}/SVD_shareanalysis.asp?pGB=1&gicode=A{ticker}&cID=&MenuYn=Y&ReportGB=&NewMenuID=109&stkGb=701"
        return self._fetch_page(url)

    def get_industry_analysis(self, ticker: str) -> str:
        """업종분석 정보 조회"""
        url = f"{self.BASE_URL}/SVD_ujanal.asp?pGB=1&gicode=A{ticker}&cID=&MenuYn=Y&ReportGB=&NewMenuID=110&stkGb=701"
        return self._fetch_page(url)

    def get_competitor_comparison(self, ticker: str) -> str:
        """경쟁사비교 정보 조회"""
        url = f"{self.BASE_URL}/SVD_Comparison.asp?pGB=1&gicode=A{ticker}&cID=&MenuYn=Y&ReportGB=&NewMenuID=106&stkGb=701&cpGb=undefined"
        return self._fetch_page(url)

    def get_disclosure(self, ticker: str) -> str:
        """거래소공시 정보 조회"""
        url = f"{self.BASE_URL}/SVD_Disclosure.asp?pGB=1&gicode=A{ticker}&cID=&MenuYn=Y&ReportGB=&NewMenuID=107&stkGb=701"
        return self._fetch_disclosure(url)

    def get_earnings_report(self, ticker: str) -> str:
        """실적속보 정보 조회"""
        url = f"{self.BASE_URL}/SVD_ProResultCorp.asp?pGB=1&gicode=A{ticker}&cID=&MenuYn=Y&ReportGB=&NewMenuID=503&stkGb=701"
        return self._fetch_page(url)
