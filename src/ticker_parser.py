"""
티커 정보 파싱을 위한 유틸리티 모듈
"""
import logging
import re
from typing import List, Dict, Any
from lxml import html
import requests
from urllib.parse import quote


class TickerParser:
    """네이버 금융 티커 정보 파싱 클래스"""
    
    BASE_URL = "https://finance.naver.com/search/search.naver"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Charset': 'UTF-8'
        })
    
    def _clean_text(self, text: str) -> str:
        """HTML 태그와 불필요한 공백을 제거합니다."""
        if not text:
            return ""
        # HTML 태그 제거
        clean_text = re.sub(r'<[^>]+>', '', text)
        # 연속된 공백을 하나로 변환
        clean_text = re.sub(r'\s+', ' ', clean_text)
        return clean_text.strip()
    
    def search_ticker(self, query: str) -> Dict[str, Any]:
        """
        네이버 금융에서 티커 정보를 검색하고 파싱합니다.
        
        Args:
            query: 검색할 종목명 또는 티커
            
        Returns:
            Dict[str, Any]: 파싱된 전체 정보 (국내/해외 티커, 실적, 공시 등)
        """
        try:
            encoded_query = quote(query)
            url = f"{self.BASE_URL}?query={encoded_query}&endUrl=&encoding=UTF-8"
            
            response = self.session.get(url)
            response.raise_for_status()
            
            # 네이버 금융은 EUC-KR 인코딩 사용
            content = response.content.decode('euc-kr', errors='ignore')
            tree = html.fromstring(content)
            
            return {
                "domestic": self._parse_domestic_tickers(tree),
                "overseas": self._parse_overseas_tickers(tree),
                "earnings": self._parse_earnings_info(tree),
                "disclosure": self._parse_disclosure_info(tree),
                "other": self._parse_other_info(tree)
            }
            
        except Exception as e:
            logging.error(f"티커 검색 중 오류 발생: {e}")
            raise
    
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
    
    def _parse_earnings_info(self, tree) -> str:
        """
        실적속보 정보를 파싱합니다.
        
        XPath: //*[@id="compBody"]
        
        Args:
            tree: lxml HTML 트리 객체
            
        Returns:
            str: 실적속보 텍스트 내용
        """
        try:
            earnings_elem = tree.xpath('//*[@id="compBody"]')
            if earnings_elem:
                return self._clean_text(earnings_elem[0].text_content())
            return ""
        except Exception as e:
            logging.warning(f"실적속보 파싱 실패: {e}")
            return ""
    
    def _parse_disclosure_info(self, tree) -> str:
        """
        거래소공시 정보를 파싱합니다.
        
        XPath: //*[@id="compBody"]/div[2]
        
        Args:
            tree: lxml HTML 트리 객체
            
        Returns:
            str: 거래소공시 텍스트 내용
        """
        try:
            disclosure_elem = tree.xpath('//*[@id="compBody"]/div[2]')
            if disclosure_elem:
                return self._clean_text(disclosure_elem[0].text_content())
            return ""
        except Exception as e:
            logging.warning(f"거래소공시 파싱 실패: {e}")
            return ""
    
    def _parse_other_info(self, tree) -> str:
        """
        기타 관련 정보를 파싱합니다.
        
        XPath: //*[@id="compBody"]
        
        Args:
            tree: lxml HTML 트리 객체
            
        Returns:
            str: 기타 정보 텍스트 내용
        """
        try:
            other_elem = tree.xpath('//*[@id="compBody"]')
            if other_elem:
                return self._clean_text(other_elem[0].text_content())
            return ""
        except Exception as e:
            logging.warning(f"기타 정보 파싱 실패: {e}")
            return ""