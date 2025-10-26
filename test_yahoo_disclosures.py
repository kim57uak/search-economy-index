#!/usr/bin/env python3
"""
Yahoo Finance 공시정보 테스트 스크립트
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from core.service_manager import service_manager

def test_yahoo_disclosures():
    """Yahoo Finance 공시정보 테스트"""
    print("=== Yahoo Finance 공시정보 테스트 ===\n")
    
    # 테스트할 주식 심볼들
    test_symbols = ["AAPL", "TSLA", "MSFT"]
    
    for symbol in test_symbols:
        print(f"--- {symbol} 공시정보 ---")
        try:
            result = service_manager.get_overseas_disclosures(symbol)
            print(result)
            print("\n" + "="*50 + "\n")
        except Exception as e:
            print(f"오류 발생: {e}")
            print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    test_yahoo_disclosures()