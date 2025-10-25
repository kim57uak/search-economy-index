"""
공통 HTTP 클라이언트 모듈
"""
import requests
from typing import Optional
from lxml import html
import re
from markdownify import markdownify as md
from core.interfaces import HttpClientInterface

try:
    import chardet
except ImportError:
    chardet = None


class HttpClient(HttpClientInterface):
    """공통 HTTP 클라이언트 클래스"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Charset': 'UTF-8'
        })
    
    def fetch_euc_kr(self, url: str) -> Optional[html.HtmlElement]:
        """EUC-KR 인코딩 페이지를 가져와서 HTML 트리로 반환"""
        try:
            response = self.session.get(url)
            response.raise_for_status()
            content = response.content.decode('euc-kr', errors='ignore')
            return html.fromstring(content)
        except Exception:
            return None
    
    def fetch_utf8(self, url: str) -> Optional[html.HtmlElement]:
        """UTF-8 인코딩 페이지를 가져와서 HTML 트리로 반환"""
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
            
            return html.fromstring(
                response.content, parser=html.HTMLParser(encoding=response.encoding)
            )
        except Exception:
            return None
    
    @staticmethod
    def html_to_markdown(html_content: str) -> str:
        """HTML을 마크다운으로 변환"""
        if not html_content:
            return ""
        markdown = md(html_content, heading_style="ATX")
        markdown = re.sub(r"\n\s*\n\s*\n", "\n\n", markdown)
        return markdown.strip()


# 싱글톤 인스턴스
http_client = HttpClient()