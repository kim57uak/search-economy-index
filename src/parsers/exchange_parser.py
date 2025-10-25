"""
환율 정보 파싱을 위한 유틸리티 모듈
"""
import logging
import re
from typing import Dict, Any
from lxml import html
import requests
from markdownify import markdownify as md


class ExchangeParser:
    """네이버 금융 환율 정보 파싱 클래스"""
    
    DOMESTIC_URL = "https://finance.naver.com/marketindex/?tabSel=exchange#tab_section"
    WORLD_BASE_URL = "https://finance.naver.com/marketindex/worldExchangeList.naver"
    
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
        return markdown.strip()
    
    def get_domestic_exchange(self) -> str:
        """국내환율 정보 조회"""
        try:
            response = self.session.get(self.DOMESTIC_URL)
            response.raise_for_status()
            
            # EUC-KR 인코딩 처리
            content = response.content.decode('euc-kr', errors='ignore')
            tree = html.fromstring(content)
            
            # 국내환율 전체 페이지
            body_elem = tree.xpath('/html/body/div')
            if body_elem:
                html_content = html.tostring(body_elem[0], encoding='unicode')
                return self._html_to_markdown(html_content)
            
            return ""
            
        except Exception as e:
            logging.error(f"국내환율 페이지 파싱 실패: {e}")
            return ""
    
    def get_world_exchange(self) -> str:
        """국제시장환율 정보 조회 (1-4페이지 통합)"""
        try:
            all_content = []
            
            # 1-4페이지 모두 수집
            for page in range(1, 5):
                url = f"{self.WORLD_BASE_URL}?page={page}"
                response = self.session.get(url)
                response.raise_for_status()
                
                # EUC-KR 인코딩 처리
                content = response.content.decode('euc-kr', errors='ignore')
                tree = html.fromstring(content)
                
                # 전체 body 내용
                body_elem = tree.xpath('/html/body')
                if body_elem:
                    html_content = html.tostring(body_elem[0], encoding='unicode')
                    markdown_content = self._html_to_markdown(html_content)
                    # 불필요한 URL 텍스트 제거
                    markdown_content = re.sub(r'/marketindex/worldExchangeDetail\.naver\?marketindexCd=', '', markdown_content)
                    markdown_content = re.sub(r'/marketindex/worldExchangeList\.naver\?page=[1-4]', '', markdown_content)
                    markdown_content = re.sub(r'\(FX_[^)]+\)', '', markdown_content)
                    all_content.append(f"## 페이지 {page}\n\n{markdown_content}")
            
            return "\n\n---\n\n".join(all_content)
            
        except Exception as e:
            logging.error(f"국제시장환율 페이지 파싱 실패: {e}")
            return ""