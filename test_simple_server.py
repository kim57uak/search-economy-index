#!/usr/bin/env python3
"""
Simple API 서버 테스트 코드
"""
import requests
import time
import subprocess
import sys
import os
from threading import Thread

def start_server():
    """백그라운드에서 서버 시작"""
    try:
        subprocess.run([sys.executable, "run_api_server.py"], 
                      cwd=os.path.dirname(__file__))
    except Exception as e:
        print(f"서버 시작 실패: {e}")

def test_server_health():
    """서버 상태 확인"""
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        return response.status_code == 200
    except:
        return False

def test_api_endpoints():
    """API 엔드포인트 테스트"""
    base_url = "http://localhost:8000"
    
    print("=== Simple API 서버 테스트 ===")
    
    # 서버 상태 확인
    if not test_server_health():
        print("✗ 서버에 연결할 수 없습니다.")
        print("서버를 먼저 시작하세요: python run_api_server.py")
        return False
    
    print("✓ 서버 연결 성공")
    
    # 테스트할 엔드포인트 목록
    test_cases = [
        # 네이버 금융 검색
        ("GET", "/search/domestic/삼성전자", "국내 티커 검색"),
        ("GET", "/search/overseas/AAPL", "해외 티커 검색"),
        
        # FnGuide 분석 (005930 = 삼성전자)
        ("GET", "/fnguide/snapshot/005930", "스냅샷 조회"),
        ("GET", "/fnguide/overview/005930", "기업개요 조회"),
        ("GET", "/fnguide/financials/005930", "재무제표 조회"),
        ("GET", "/fnguide/ratios/005930", "재무비율 조회"),
        ("GET", "/fnguide/indicators/005930", "투자지표 조회"),
        ("GET", "/fnguide/consensus/005930", "컨센서스 조회"),
        ("GET", "/fnguide/ownership/005930", "지분분석 조회"),
        ("GET", "/fnguide/industry/005930", "업종분석 조회"),
        ("GET", "/fnguide/competitors/005930", "경쟁사비교 조회"),
        ("GET", "/fnguide/disclosures/005930", "거래소공시 조회"),
        ("GET", "/fnguide/earnings/005930", "실적보고서 조회"),
    ]
    
    success_count = 0
    total_count = len(test_cases)
    
    for method, endpoint, description in test_cases:
        try:
            url = f"{base_url}{endpoint}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if "error" not in data:
                    print(f"✓ {description} 성공")
                    success_count += 1
                else:
                    print(f"✗ {description} 실패: {data['error']}")
            else:
                print(f"✗ {description} 실패: HTTP {response.status_code}")
                
        except requests.exceptions.Timeout:
            print(f"✗ {description} 실패: 타임아웃")
        except Exception as e:
            print(f"✗ {description} 실패: {e}")
    
    print(f"\n=== 테스트 결과 ===")
    print(f"성공: {success_count}/{total_count}")
    print(f"성공률: {success_count/total_count*100:.1f}%")
    
    return success_count == total_count

def test_with_curl():
    """curl 명령어 예시 출력"""
    print("\n=== curl 테스트 명령어 예시 ===")
    
    curl_commands = [
        'curl "http://localhost:8000/"',
        'curl "http://localhost:8000/search/domestic/삼성전자"',
        'curl "http://localhost:8000/search/overseas/AAPL"',
        'curl "http://localhost:8000/fnguide/snapshot/005930"',
        'curl "http://localhost:8000/fnguide/overview/005930"',
    ]
    
    for cmd in curl_commands:
        print(f"  {cmd}")

def main():
    """메인 함수"""
    print("Simple API 서버 테스트를 시작합니다...")
    
    # 서버 상태 확인
    if test_server_health():
        print("서버가 이미 실행 중입니다.")
        test_api_endpoints()
    else:
        print("서버가 실행되지 않았습니다.")
        print("\n서버를 시작하려면 다음 명령어를 실행하세요:")
        print("python run_api_server.py")
        print("\n그 후 다시 이 테스트를 실행하세요:")
        print("python test_simple_server.py")
    
    # curl 예시 출력
    test_with_curl()

if __name__ == "__main__":
    main()