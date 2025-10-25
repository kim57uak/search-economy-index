"""
유가 및 귀금속 정보 파싱을 위한 유틸리티 모듈
"""
import logging
import re
from typing import Dict, Any
from lxml import html
import requests
from markdownify import markdownify as md


class GoldParser:
    """네이버 금융 유가 및 귀금속 정보 파싱 클래스"""
    
    BASE_URL = "https://finance.naver.com/marketindex/?tabSel=gold#tab_section"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Charset': 'UTF-8'
        })
    
    def _html_to_markdown(self, html_content: str) -> str:
        """HTML을 마크다운으로 변환합니다."""
        if not html_content:
            return ""
        markdown = md(html_content, heading_style="ATX")
        markdown = re.sub(r"\n\s*\n\s*\n", "\n\n", markdown)
        # 불필요한 URL 텍스트 제거
        markdown = re.sub(r'\(/marketindex/oilDetail\.naver\?marketindexCd=[^)]+\)', '', markdown)
        return markdown.strip()
    
    def _fetch_page(self) -> Dict[str, str]:
        """유가 및 귀금속 페이지를 가져와서 파싱합니다."""
        try:
            response = self.session.get(self.BASE_URL)
            response.raise_for_status()
            
            # EUC-KR 인코딩 처리
            content = response.content.decode('euc-kr', errors='ignore')
            tree = html.fromstring(content)
            
            results = {}
            
            # 유가
            oil_elem = tree.xpath('//*[@id="content"]/div[3]')
            if oil_elem:
                html_content = html.tostring(oil_elem[0], encoding='unicode')
                results['oil_prices'] = self._html_to_markdown(html_content)
            
            # 귀금속
            precious_metals_elem = tree.xpath('//*[@id="content"]/div[4]')
            if precious_metals_elem:
                html_content = html.tostring(precious_metals_elem[0], encoding='unicode')
                results['precious_metals'] = self._html_to_markdown(html_content)
            
            return results
            
        except Exception as e:
            logging.error(f"유가 및 귀금속 페이지 파싱 실패: {e}")
            return {}
    
    def get_oil_prices(self) -> str:
        """유가 정보 조회"""
        data = self._fetch_page()
        return data.get('oil_prices', '')
    
    def get_precious_metals(self) -> str:
        """귀금속 정보 조회"""
        data = self._fetch_page()
        return data.get('precious_metals', '')