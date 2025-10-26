"""
티커 정보 파싱을 위한 유틸리티 모듈
"""
import logging
import re
from typing import List, Dict, Any
from urllib.parse import quote
from core.base_parser import BaseTickerParser, ParserFactory
from core.interfaces import HttpClientInterface


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
        tree, content = self._fetch_search_page(query)
        if tree is None:
            return []
        
        # JavaScript 리다이렉트 확인 (검색 결과 1개일 때)
        redirect_ticker = self._check_js_redirect(content)
        if redirect_ticker:
            return [redirect_ticker]
        
        # 검색 결과가 1개면 종목 페이지로 리다이렉트됨
        single_ticker = self._parse_single_ticker_page(tree)
        if single_ticker:
            return [single_ticker]
        
        # 여러 개면 검색 결과 리스트 페이지
        return self._parse_domestic_tickers(tree)
    
    def search_overseas(self, query: str) -> List[Dict[str, str]]:
        """해외 티커 검색"""
        tree, _ = self._fetch_search_page(query)
        return self._parse_overseas_tickers(tree) if tree is not None else []
    
    def _fetch_search_page(self, query: str):
        """검색 페이지 가져오기"""
        try:
            encoded_query = quote(query)
            url = f"{self.BASE_URL}?query={encoded_query}&endUrl=&encoding=UTF-8&page=1"
            
            # 원본 콘텐츠도 함께 반환 (JavaScript 리다이렉트 확인용)
            import requests
            response = self.http_client.session.get(url)
            response.raise_for_status()
            content = response.content.decode('euc-kr', errors='ignore')
            
            from lxml import html
            tree = html.fromstring(content)
            return tree, content
        except Exception as e:
            logging.error(f"티커 검색 중 오류 발생: {e}")
            return None, None
    
    def _check_js_redirect(self, content: str) -> Dict[str, str]:
        """
        JavaScript 리다이렉트를 확인하고 종목 페이지에서 정보를 가져옵니다.
        
        Args:
            content: HTML 콘텐츠 문자열
            
        Returns:
            Dict[str, str]: 티커 정보 또는 None
        """
        try:
            # location.href = '/item/main.naver?code=080160' 패턴 찾기
            redirect_match = re.search(r'location\.href\s*=\s*["\']([^"\']+)["\']', content)
            if not redirect_match:
                return None
            
            redirect_url = redirect_match.group(1)
            code_match = re.search(r'code=([0-9A-Z]+)', redirect_url)
            if not code_match:
                return None
            
            ticker_code = code_match.group(1)
            
            # 종목 페이지에서 종목명 가져오기
            item_url = f"https://finance.naver.com{redirect_url}" if redirect_url.startswith('/') else redirect_url
            tree = self.http_client.fetch_utf8(item_url)
            if tree is None:
                return None
            
            # 종목명 추출
            name_elem = tree.xpath('//*[@id="middle"]//h2/a')
            if name_elem:
                company_name = self._clean_text(name_elem[0].text_content())
                return {
                    "ticker": ticker_code,
                    "name": company_name
                }
            
            return None
        except Exception as e:
            logging.debug(f"JavaScript 리다이렉트 처리 실패: {e}")
            return None
    
    def _parse_single_ticker_page(self, tree) -> Dict[str, str]:
        """
        단일 종목 페이지에서 티커 정보를 파싱합니다.
        검색 결과가 1개일 때 바로 종목 페이지로 리다이렉트됩니다.
        
        Args:
            tree: lxml HTML 트리 객체
            
        Returns:
            Dict[str, str]: 티커 정보 또는 None
        """
        try:
            # 종목명 추출: //*[@id="middle"]/div[1]/div[1]/h2/a
            name_elem = tree.xpath('//*[@id="middle"]//h2/a')
            if not name_elem:
                return None
            
            company_name = self._clean_text(name_elem[0].text_content())
            
            # 종목코드 추출: URL에서 code 파라미터
            code_elem = tree.xpath('//input[@id="code"]')
            if code_elem:
                ticker_code = code_elem[0].get('value')
                if ticker_code:
                    return {
                        "ticker": ticker_code,
                        "name": company_name
                    }
            
            return None
        except Exception as e:
            logging.debug(f"단일 종목 페이지 파싱 실패: {e}")
            return None
    
    def _parse_domestic_tickers(self, tree) -> List[Dict[str, str]]:
        """
        국내 주식 티커 정보를 파싱합니다.
        
        XPath: //*[@id="content"]/div[4]/table//tr
        
        Args:
            tree: lxml HTML 트리 객체
            
        Returns:
            List[Dict[str, str]]: 국내 티커 목록
        """
        try:
            rows = tree.xpath('//*[@id="content"]/div[4]/table//tr')
            tickers = []
            
            for row in rows:
                tds = row.xpath('./td')
                if not tds:  # 헤더 행 스킵
                    continue
                    
                # 첫 번째 td에서 링크 찾기
                link_elem = row.xpath('./td[1]//a[@href]')
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
            logging.debug(f"국내 티커 파싱 실패: {e}")
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


# 팩토리에 파서 등록
ParserFactory.register_parser('ticker', TickerParser)