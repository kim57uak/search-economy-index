"""
파서 인터페이스 정의
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from lxml import html


class HttpClientInterface(ABC):
    """HTTP 클라이언트 인터페이스"""
    
    @abstractmethod
    def fetch_euc_kr(self, url: str) -> Optional[html.HtmlElement]:
        pass
    
    @abstractmethod
    def fetch_utf8(self, url: str) -> Optional[html.HtmlElement]:
        pass
    
    @staticmethod
    @abstractmethod
    def html_to_markdown(html_content: str) -> str:
        pass


class ParserInterface(ABC):
    """파서 기본 인터페이스"""
    
    @abstractmethod
    def parse(self, *args, **kwargs) -> Dict[str, Any]:
        pass


class WebParserBase:
    """웹 파싱 기본 클래스"""
    
    def __init__(self, http_client: HttpClientInterface):
        self.http_client = http_client
    
    def _extract_element(self, tree: html.HtmlElement, xpath: str) -> Optional[str]:
        """XPath로 요소 추출 후 마크다운 변환"""
        try:
            elements = tree.xpath(xpath)
            if elements:
                html_content = html.tostring(elements[0], encoding='unicode')
                return self.http_client.html_to_markdown(html_content)
            return None
        except Exception:
            return None