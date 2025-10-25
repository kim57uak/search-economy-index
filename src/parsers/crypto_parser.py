"""
암호화폐 정보 파싱을 위한 유틸리티 모듈
"""
import logging
from typing import Dict, Any
from core.base_parser import WebParserBase, ParserFactory
from core.interfaces import HttpClientInterface, ParserInterface


class CryptoParserInterface(ParserInterface):
    """암호화폐 파서 인터페이스"""
    
    def get_crypto_data(self) -> str:
        pass


class CryptoParser(WebParserBase, CryptoParserInterface):
    """Investing.com 암호화폐 정보 파싱 클래스"""
    
    BASE_URL = "https://kr.investing.com/crypto"
    
    def __init__(self, http_client: HttpClientInterface):
        super().__init__(http_client)
    
    def parse(self, *args, **kwargs) -> Dict[str, Any]:
        return {"crypto_data": self.get_crypto_data()}
    
    def get_crypto_data(self) -> str:
        """암호화폐 데이터 조회"""
        try:
            tree = self.http_client.fetch_utf8(self.BASE_URL)
            if tree is not None:
                xpath = '//*[@id="__next"]/div[2]/div[2]/div[2]/div[1]/div[5]/div/div[2]/div[1]/table'
                return self._extract_element(tree, xpath) or ""
            return ""
        except Exception as e:
            logging.error(f"암호화폐 데이터 파싱 실패: {e}")
            return ""


# 팩토리에 파서 등록
ParserFactory.register_parser('crypto', CryptoParser)