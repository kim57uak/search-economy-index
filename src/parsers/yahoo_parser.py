"""
Yahoo Finance 글로벌 금융 데이터 파싱을 위한 유틸리티 모듈
"""
import logging
import re
from typing import Dict, Any, List
from core.base_parser import WebParserBase, ParserFactory
from core.interfaces import HttpClientInterface, ParserInterface


class YahooParserInterface(ParserInterface):
    """Yahoo Finance 파서 인터페이스"""
    
    def get_global_indices(self) -> str:
        pass
    
    def get_us_treasury_yields(self) -> str:
        pass


class YahooParser(WebParserBase, YahooParserInterface):
    """Yahoo Finance 글로벌 금융 데이터 파싱 클래스"""
    
    BASE_URL = "https://finance.yahoo.com"
    
    def __init__(self, http_client: HttpClientInterface):
        super().__init__(http_client)
    
    def parse(self, *args, **kwargs) -> Dict[str, Any]:
        return {
            "global_indices": self.get_global_indices(),
            "us_treasury_yields": self.get_us_treasury_yields()
        }
    
    def _clean_data(self, data: str) -> str:
        """데이터 정리"""
        if not data:
            return ""
        data = re.sub(r'\(/quote/[^)]+\)', '', data)
        lines = [line.strip() for line in data.split('\n') if line.strip() and '|' in line]
        return '\n'.join(lines[:20])
    
    def get_global_indices(self) -> str:
        """글로벌 주요 지수 정보 조회"""
        try:
            tree = self.http_client.fetch_utf8("https://finance.yahoo.com/world-indices/")
            if tree is not None:
                result = self._extract_element(tree, '//table') or ""
                return self._clean_data(result)
            return ""
        except Exception as e:
            logging.error(f"글로벌 지수 파싱 실패: {e}")
            return ""
    
    def get_us_treasury_yields(self) -> str:
        """미국 국채 수익률 정보 조회"""
        try:
            tree = self.http_client.fetch_utf8("https://finance.yahoo.com/bonds/")
            if tree is not None:
                result = self._extract_element(tree, '//table') or ""
                return self._clean_data(result)
            return ""
        except Exception as e:
            logging.error(f"미국 국채 수익률 파싱 실패: {e}")
            return ""
    
    def get_vix_data(self) -> str:
        """VIX 공포지수 정보 조회"""
        try:
            tree = self.http_client.fetch_utf8("https://finance.yahoo.com/quote/%5EVIX/")
            if tree is not None:
                result = self._extract_element(tree, '//div[contains(@class, "quote")]') or ""
                return self._clean_data(result)
            return ""
        except Exception as e:
            logging.error(f"VIX 데이터 파싱 실패: {e}")
            return ""
    
    def get_commodities(self) -> str:
        """글로벌 원자재 가격 정보 조회"""
        try:
            tree = self.http_client.fetch_utf8("https://finance.yahoo.com/commodities/")
            if tree is not None:
                result = self._extract_element(tree, '//table') or ""
                return self._clean_data(result)
            return ""
        except Exception as e:
            logging.error(f"원자재 데이터 파싱 실패: {e}")
            return ""
    
    def get_forex_majors(self) -> str:
        """주요 환율 정보 조회"""
        try:
            tree = self.http_client.fetch_utf8("https://finance.yahoo.com/currencies/")
            if tree is not None:
                result = self._extract_element(tree, '//table') or ""
                return self._clean_data(result)
            return ""
        except Exception as e:
            logging.error(f"환율 데이터 파싱 실패: {e}")
            return ""
    
    def get_asian_indices(self) -> str:
        """아시아 주요 지수 정보 조회"""
        try:
            tree = self.http_client.fetch_utf8("https://finance.yahoo.com/world-indices/")
            if tree is not None:
                result = self._extract_element(tree, '//table') or ""
                # 아시아 지수만 필터링
                lines = result.split('\n')
                asian_lines = [line for line in lines if any(keyword in line for keyword in ['Nikkei', 'Hang Seng', 'Shanghai', 'KOSPI', 'Taiwan', 'BSE'])]
                return '\n'.join(asian_lines[:15])
            return ""
        except Exception as e:
            logging.error(f"아시아 지수 파싱 실패: {e}")
            return ""
    
    def get_european_indices(self) -> str:
        """유럽 주요 지수 정보 조회"""
        try:
            tree = self.http_client.fetch_utf8("https://finance.yahoo.com/world-indices/")
            if tree is not None:
                result = self._extract_element(tree, '//table') or ""
                # 유럽 지수만 필터링
                lines = result.split('\n')
                european_lines = [line for line in lines if any(keyword in line for keyword in ['FTSE', 'DAX', 'CAC', 'IBEX', 'AEX', 'SMI'])]
                return '\n'.join(european_lines[:15])
            return ""
        except Exception as e:
            logging.error(f"유럽 지수 파싱 실패: {e}")
            return ""
    
    def get_sector_performance(self) -> str:
        """섹터별 성과 정보 조회"""
        try:
            tree = self.http_client.fetch_utf8("https://finance.yahoo.com/sectors/")
            if tree is not None:
                result = self._extract_element(tree, '//table') or ""
                return self._clean_data(result)
            return ""
        except Exception as e:
            logging.error(f"섹터 성과 파싱 실패: {e}")
            return ""
    
    def get_stock_quote(self, symbol: str) -> str:
        """개별 주식 정보 조회 (Yahoo Finance)"""
        try:
            url = f"https://finance.yahoo.com/quote/{symbol}/"
            tree = self.http_client.fetch_utf8(url)
            if tree is not None:
                # 가격 정보 추출
                price_elements = tree.xpath('//div[contains(@class, "price")]')
                if price_elements:
                    price_data = []
                    for elem in price_elements[:5]:  # 상위 5개만
                        text = elem.text_content().strip()
                        if text and len(text) < 50:  # 짧은 텍스트만
                            price_data.append(text)
                    
                    # 주식 이름 추출
                    title_elem = tree.xpath('//h1')
                    title = title_elem[0].text_content().strip() if title_elem else symbol
                    
                    result = f"**{title}**\n" + "\n".join(price_data[:10])
                    return result
            return ""
        except Exception as e:
            logging.error(f"주식 정보 파싱 실패 ({symbol}): {e}")
            return ""
    
    def get_crypto_quote(self, symbol: str) -> str:
        """개별 암호화폐 정보 조회 (Yahoo Finance)"""
        try:
            # 암호화폐 심볼 정규화 (BTC -> BTC-USD)
            if not symbol.endswith('-USD'):
                symbol = f"{symbol}-USD"
            
            url = f"https://finance.yahoo.com/quote/{symbol}/"
            tree = self.http_client.fetch_utf8(url)
            if tree is not None:
                # 가격 정보 추출
                price_elements = tree.xpath('//div[contains(@class, "price")]')
                if price_elements:
                    price_data = []
                    for elem in price_elements[:5]:
                        text = elem.text_content().strip()
                        if text and len(text) < 50:
                            price_data.append(text)
                    
                    # 암호화폐 이름 추출
                    title_elem = tree.xpath('//h1')
                    title = title_elem[0].text_content().strip() if title_elem else symbol
                    
                    result = f"**{title}**\n" + "\n".join(price_data[:10])
                    return result
            return ""
        except Exception as e:
            logging.error(f"암호화폐 정보 파싱 실패 ({symbol}): {e}")
            return ""
    
    def get_multiple_stock_quotes(self, symbols: List[str]) -> Dict[str, str]:
        """복수 해외 주식 정보 조회"""
        results = {}
        for symbol in symbols:
            results[symbol] = self.get_stock_quote(symbol)
        return results
    
    def get_multiple_crypto_quotes(self, symbols: List[str]) -> Dict[str, str]:
        """복수 암호화폐 정보 조회"""
        results = {}
        for symbol in symbols:
            results[symbol] = self.get_crypto_quote(symbol)
        return results
    
    def search_overseas_ticker(self, query: str) -> List[Dict[str, str]]:
        """해외 주식 티커 검색 (Yahoo Finance 웹 스크래핑)"""
        try:
            # Yahoo Finance 검색 페이지 사용
            from urllib.parse import quote
            encoded_query = quote(query)
            url = f"https://finance.yahoo.com/lookup?s={encoded_query}"
            
            tree = self.http_client.fetch_utf8(url)
            if tree is not None:
                # 검색 결과 테이블에서 티커 추출
                rows = tree.xpath('//table//tr')
                tickers = []
                
                for row in rows[1:11]:  # 헤더 제외, 상위 10개
                    cells = row.xpath('.//td')
                    if len(cells) >= 2:
                        # 첫 번째 셀에서 티커 추출
                        ticker_elem = cells[0].xpath('.//a')
                        if ticker_elem:
                            ticker_text = ticker_elem[0].text_content().strip()
                            name_text = cells[1].text_content().strip() if len(cells) > 1 else ''
                            
                            if ticker_text and len(ticker_text) < 10:  # 짧은 티커만
                                tickers.append({
                                    "ticker": ticker_text,
                                    "name": name_text,
                                    "exchange": "Yahoo Finance",
                                    "type": "EQUITY"
                                })
                
                return tickers
            
            return []
            
        except Exception as e:
            logging.error(f"해외 티커 검색 실패: {e}")
            return []


# 팩토리에 파서 등록
ParserFactory.register_parser('yahoo', YahooParser)