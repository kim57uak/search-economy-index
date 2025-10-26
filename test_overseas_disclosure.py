#!/usr/bin/env python3
"""
해외주식 공시정보 기능 테스트
"""
import sys
sys.path.append('src')

from core.service_manager import service_manager

def test_overseas_disclosure():
    """해외주식 공시정보 테스트"""
    symbols = ["AAPL", "TSLA", "MSFT"]  # 애플, 테슬라, 마이크로소프트
    
    for symbol in symbols:
        print(f"=== {symbol} 해외주식 공시정보 테스트 ===\n")
        
        try:
            result = service_manager.get_overseas_disclosures(symbol)
            print(f"결과 길이: {len(result)} 문자")
            print(f"결과 미리보기:\n{result[:500]}...")
            
            # 링크가 포함되어 있는지 확인
            if "[" in result and "](" in result:
                print("✅ 마크다운 링크 포함됨")
            else:
                print("❌ 마크다운 링크 없음")
                
            # SEC 관련 내용이 있는지 확인
            if "SEC" in result or "edgar" in result.lower():
                print("✅ SEC 관련 내용 포함됨")
            else:
                print("❌ SEC 관련 내용 없음")
                
        except Exception as e:
            print(f"❌ 오류: {e}")
        
        print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    test_overseas_disclosure()