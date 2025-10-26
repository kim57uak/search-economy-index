"""
암호화폐 티커 검색을 위한 유틸리티 모듈
"""
import logging
import requests
from typing import List, Dict, Any
from core.base_parser import WebParserBase, ParserFactory
from core.interfaces import HttpClientInterface, ParserInterface


class CryptoTickerParserInterface(ParserInterface):
    """암호화폐 티커 파서 인터페이스"""
    
    def search_crypto_ticker(self, query: str) -> List[Dict[str, str]]:
        pass


class CryptoTickerParser(WebParserBase, CryptoTickerParserInterface):
    """CoinGecko API를 사용한 암호화폐 티커 검색 클래스"""
    
    BASE_URL = "https://api.coingecko.com/api/v3"
    
    def __init__(self, http_client: HttpClientInterface):
        super().__init__(http_client)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; CryptoSearch/1.0)'
        })
    
    def parse(self, query: str) -> Dict[str, Any]:
        return {
            "crypto_tickers": self.search_crypto_ticker(query)
        }
    
    def search_crypto_ticker(self, query: str) -> List[Dict[str, str]]:
        """암호화폐 티커 검색 (Data source: CoinGecko API)"""
        try:
            url = f"{self.BASE_URL}/search?query={query}"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            tickers = []
            
            if 'coins' in data:
                for coin in data['coins'][:10]:  # 상위 10개만
                    tickers.append({
                        "symbol": coin.get('symbol', '').upper(),
                        "name": coin.get('name', ''),
                        "id": coin.get('id', ''),
                        "market_cap_rank": coin.get('market_cap_rank', 0),
                        "source": "CoinGecko API"
                    })
            
            return tickers
            
        except Exception as e:
            logging.error(f"암호화폐 티커 검색 실패: {e}")
            return []
    
    def get_top_cryptos(self, limit: int = 20, currency: str = 'krw') -> List[Dict[str, str]]:
        """상위 암호화폐 목록 조회 (Data source: CoinGecko API)"""
        try:
            url = f"{self.BASE_URL}/coins/markets"
            params = {
                'vs_currency': currency.lower(),
                'order': 'market_cap_desc',
                'per_page': limit,
                'page': 1
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            cryptos = []
            
            for coin in data:
                cryptos.append({
                    "symbol": coin.get('symbol', '').upper(),
                    "name": coin.get('name', ''),
                    "id": coin.get('id', ''),
                    "current_price": coin.get('current_price', 0),
                    "market_cap_rank": coin.get('market_cap_rank', 0),
                    "source": "CoinGecko API"
                })
            
            return cryptos
            
        except Exception as e:
            logging.error(f"상위 암호화폐 조회 실패: {e}")
            return []


# 팩토리에 파서 등록
ParserFactory.register_parser('crypto_ticker', CryptoTickerParser)