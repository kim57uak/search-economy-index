"""
MarketWatch 해외 주식 공시정보 및 어닝콜 파싱을 위한 유틸리티 모듈
"""
import logging
from typing import Dict, Any, List
from core.base_parser import WebParserBase, ParserFactory
from core.interfaces import HttpClientInterface, ParserInterface


class MarketWatchParserInterface(ParserInterface):
    """MarketWatch 파서 인터페이스"""
    
    def get_overseas_disclosures(self, symbol: str) -> str:
        pass


class MarketWatchParser(WebParserBase, MarketWatchParserInterface):
    """MarketWatch 해외 주식 공시정보 및 어닝콜 파싱 클래스"""
    
    BASE_URL = "https://www.marketwatch.com"
    
    def __init__(self, http_client: HttpClientInterface):
        super().__init__(http_client)
    
    def parse(self, *args, **kwargs) -> Dict[str, Any]:
        return {}
    
    def get_overseas_disclosures(self, symbol: str) -> str:
        """해외주식 공시정보 및 어닝콜 조회 (SEC EDGAR + MarketWatch)"""
        try:
            all_content = [f"=== {symbol} 공시정보 & Earnings Call ==="]
            
            # 1. SEC 공시 리스트 (직접 링크)
            all_content.append("\n=== SEC 공시 리스트 ===")
            
            sec_forms = [
                ("10-K Annual Report", "10-K"),
                ("10-Q Quarterly Report", "10-Q"),
                ("8-K Current Report", "8-K"),
                ("DEF 14A Proxy Statement", "DEF%2014A"),
                ("S-1 Registration Statement", "S-1"),
                ("4 Statement of Changes", "4")
            ]
            
            for form_name, form_code in sec_forms:
                edgar_url = f"https://www.sec.gov/edgar/search/?r=el#/q={symbol}&forms={form_code}"
                all_content.append(f"[{form_name}]({edgar_url})")
            
            # 2. MarketWatch에서 어닝콜 데이터 추출
            mw_url = f"https://www.marketwatch.com/investing/stock/{symbol.lower()}"
            try:
                mw_tree = self.http_client.fetch_utf8(mw_url)
                if mw_tree is not None:
                    all_content.append("\n=== Earnings Call 리스트 ===")
                    
                    # 어닝콜 관련 링크 찾기
                    all_links = mw_tree.xpath('//a[@href]')
                    earnings_count = 0
                    
                    for link in all_links:
                        if earnings_count >= 8:
                            break
                            
                        href = link.get('href', '')
                        title = link.text_content().strip()
                        
                        # Earnings 관련 링크 필터링
                        if (('/earnings' in href.lower() or 
                             ('earnings' in title.lower() and 'call' in title.lower()) or
                             'earnings-call' in href.lower()) and 
                            len(title) > 10 and len(title) < 100):
                            
                            full_url = f"https://www.marketwatch.com{href}" if href.startswith('/') else href
                            all_content.append(f"[{title[:80]}]({full_url})")
                            earnings_count += 1
            except Exception as e:
                logging.warning(f"MarketWatch 페이지 로드 실패: {e}")
            
            # 기본 링크
            all_content.extend([
                "\n=== 기본 링크 ===",
                f"[SEC EDGAR 공식 사이트](https://www.sec.gov/edgar/search/?r=el#/q={symbol})",
                f"[MarketWatch {symbol}](https://www.marketwatch.com/investing/stock/{symbol.lower()})",
                f"[MarketWatch Earnings](https://www.marketwatch.com/investing/stock/{symbol.lower()}/earnings)"
            ])
            
            return '\n'.join(all_content)
            
        except Exception as e:
            logging.error(f"공시정보 파싱 실패 ({symbol}): {e}")
            return f"{symbol} 공시정보 조회 중 오류가 발생했습니다."


# 팩토리에 파서 등록
ParserFactory.register_parser('marketwatch', MarketWatchParser)
