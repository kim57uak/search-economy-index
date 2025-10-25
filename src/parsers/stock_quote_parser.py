"""
개별 종목 정보 파싱을 위한 유틸리티 모듈 (국내 주식)
"""
import logging
import re
from typing import Dict, Any, List
from core.base_parser import WebParserBase, ParserFactory
from core.interfaces import HttpClientInterface, ParserInterface


class StockQuoteParserInterface(ParserInterface):
    """개별 종목 파서 인터페이스"""
    
    def get_domestic_stock_quote(self, ticker: str) -> str:
        pass


class StockQuoteParser(WebParserBase, StockQuoteParserInterface):
    """네이버 금융 개별 종목 정보 파싱 클래스"""
    
    BASE_URL = "https://finance.naver.com/item/main.naver"
    
    def __init__(self, http_client: HttpClientInterface):
        super().__init__(http_client)
    
    def parse(self, ticker: str) -> Dict[str, Any]:
        return {
            "domestic_quote": self.get_domestic_stock_quote(ticker)
        }
    
    def _clean_stock_data(self, data: str) -> str:
        """주식 데이터 정리"""
        if not data:
            return ""
        
        try:
            # 숫자와 기본 기호만 추출하여 간단한 정보 제공
            import re
            
            # 가격 정보 추출 (숫자, 콤마, 소수점)
            prices = re.findall(r'[\d,]+(?:\.\d+)?', data)
            
            # 백분율 정보 추출
            percentages = re.findall(r'[+-]?\d+\.\d+%', data)
            
            # 결과 정리
            result_parts = []
            
            if prices:
                # 주요 가격 정보 (첫 5개)
                main_prices = prices[:5]
                result_parts.append(f"가격: {', '.join(main_prices)}")
            
            if percentages:
                # 등락률 정보
                result_parts.append(f"등락률: {', '.join(percentages[:3])}")
            
            # 거래량 정보 추출 (큰 숫자)
            volumes = [p for p in prices if len(p.replace(',', '')) > 6]
            if volumes:
                result_parts.append(f"거래량: {volumes[0]}")
            
            return ' | '.join(result_parts) if result_parts else "데이터 없음"
            
        except Exception as e:
            return f"데이터 처리 오류: {str(e)}"
    
    def get_domestic_stock_quote(self, ticker: str) -> str:
        """국내 개별 주식 정보 조회"""
        try:
            url = f"{self.BASE_URL}?code={ticker}"
            tree = self.http_client.fetch_euc_kr(url)
            if tree is not None:
                # 주가 정보 직접 추출
                result_parts = []
                
                # 현재가 추출
                current_price = tree.xpath('//p[@class="no_today"]/em/span[@class="blind"]/text()')
                if current_price:
                    result_parts.append(f"현재가: {current_price[0]}")
                
                # 전일대비 추출
                change = tree.xpath('//p[@class="no_exday"]/em/span[@class="blind"]/text()')
                if change:
                    result_parts.append(f"전일대비: {change[0]}")
                
                # 등락률 추출
                change_rate = tree.xpath('//p[@class="no_exday"]/em[2]/span[@class="blind"]/text()')
                if change_rate:
                    result_parts.append(f"등락률: {change_rate[0]}")
                
                # 거래량 추출
                volume = tree.xpath('//td[contains(text(), "거래량")]/following-sibling::td/text()')
                if volume:
                    result_parts.append(f"거래량: {volume[0].strip()}")
                
                # 결과 반환
                if result_parts:
                    return ' | '.join(result_parts)
                else:
                    # 대체 방법: 전체 페이지에서 숫자 추출
                    page_text = tree.text_content()
                    return self._clean_stock_data(page_text)
            return ""
        except Exception as e:
            logging.error(f"국내 주식 정보 파싱 실패 ({ticker}): {e}")
            return ""
    
    def get_multiple_domestic_stock_quotes(self, tickers: List[str]) -> Dict[str, str]:
        """복수 국내 주식 정보 조회"""
        results = {}
        for ticker in tickers:
            results[ticker] = self.get_domestic_stock_quote(ticker)
        return results


# 팩토리에 파서 등록
ParserFactory.register_parser('stock_quote', StockQuoteParser)