"""
티커 정보 파싱을 위한 유틸리티 모듈
"""
import logging
import re
from typing import List, Dict, Any
from urllib.parse import quote
from ..core.base_parser import BaseTickerParser, ParserFactory
from ..core.interfaces import HttpClientInterface


class TickerParser(BaseTickerParser):
    """네이버 금융 티커 정보 파싱 클래스"""
    
    BASE_URL = "https://finance.naver.com/search/search.naver"
    
    def __init__(self, http_client: HttpClientInterface):
        super().__init__(http_client)
    
    def _clean_text(self, text: str) -> str:
        """HTML 태그와 불필요한 공백을 제거합니다."""
        if not text:
            return ""
        # HTML 태그 제거
        clean_text = re.sub(r'<[^>]+>', '', text)
        # 연속된 공백을 하나로 변환
        clean_text = re.sub(r'\s+', ' ', clean_text)
        return clean_text.strip()
    
    def search_domestic(self, query: str) -> List[Dict[str, str]]:
        """국내 티커 검색"""
        tree = self._fetch_search_page(query)
        return self._parse_domestic_tickers(tree) if tree is not None else []
    
    def search_overseas(self, query: str) -> List[Dict[str, str]]:
        """해외 티커 검색"""
        tree = self._fetch_search_page(query)
        return self._parse_overseas_tickers(tree) if tree is not None else []
    
    def _fetch_search_page(self, query: str):
        """검색 페이지 가져오기"""
        try:
            encoded_query = quote(query)
            url = f"{self.BASE_URL}?query={encoded_query}&endUrl=&encoding=UTF-8"
            return self.http_client.fetch_euc_kr(url)
        except Exception as e:
            logging.error(f"티커 검색 중 오류 발생: {e}")
            return None
    
    def _parse_domestic_tickers(self, tree) -> List[Dict[str, str]]:
        """
        국내 주식 티커 정보를 파싱합니다.
        
        XPath: //*[@id="content"]/div[4]/table/tbody/tr/td[1]
        
        Args:
            tree: lxml HTML 트리 객체
            
        Returns:
            List[Dict[str, str]]: 국내 티커 목록
        """
        try:
            rows = tree.xpath('//*[@id="content"]/div[4]/table/tbody/tr')
            tickers = []
            
            for row in rows:
                ticker_elem = row.xpath('./td[1]')
                if ticker_elem:
                    # 링크에서 티커 코드 추출
                    link_elem = ticker_elem[0].xpath('.//a[@href]')
                    if link_elem:
                        href = link_elem[0].get('href')
                        # /item/main.naver?code=005930에서 005930 추출
                        code_match = re.search(r'code=([0-9A-Z]+)', href)
                        if code_match:
                            ticker_code = code_match.group(1)
                            company_name = self._clean_text(link_elem[0].text_content())
                            tickers.append({
                                "ticker": ticker_code,
                                "name": company_name
                            })
            
            return tickers
        except Exception as e:
            logging.warning(f"국내 티커 파싱 실패: {e}")
            return []
    
    def _parse_overseas_tickers(self, tree) -> List[Dict[str, str]]:
        """
        해외 주식 티커 정보를 파싱합니다.
        
        XPath: //*[@id="content"]/div[8]/table/tbody/tr/td[1]
        
        Args:
            tree: lxml HTML 트리 객체
            
        Returns:
            List[Dict[str, str]]: 해외 티커 목록
        """
        try:
            rows = tree.xpath('//*[@id="content"]/div[8]/table/tbody/tr')
            tickers = []
            
            for row in rows:
                ticker_elem = row.xpath('./td[1]')
                if ticker_elem:
                    # 링크에서 티커 코드 추출
                    link_elem = ticker_elem[0].xpath('.//a[@href]')
                    if link_elem:
                        href = link_elem[0].get('href')
                        # https://m.stock.naver.com/worldstock/stock/TSLA.O/total에서 TSLA 추출
                        ticker_match = re.search(r'/stock/([A-Z]+)', href)
                        if ticker_match:
                            ticker_code = ticker_match.group(1)
                            company_name = self._clean_text(link_elem[0].text_content())
                            tickers.append({
                                "ticker": ticker_code,
                                "name": company_name
                            })
            
            return tickers
        except Exception as e:
            logging.warning(f"해외 티커 파싱 실패: {e}")
            return []
    
