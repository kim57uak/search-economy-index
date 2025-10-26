#!/usr/bin/env python3
"""
Yahoo Finance 페이지 구조 디버깅 스크립트
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from parsers.http_client import HttpClient

def debug_yahoo_structure():
    """Yahoo Finance 페이지 구조 분석"""
    print("=== Yahoo Finance 페이지 구조 분석 ===\n")
    
    http_client = HttpClient()
    symbol = "AAPL"
    url = f"https://finance.yahoo.com/quote/{symbol}/"
    
    try:
        tree = http_client.fetch_utf8(url)
        if tree is not None:
            print(f"페이지 로드 성공: {url}")
            
            # 전체 페이지에서 tabpanel 관련 요소 찾기
            print("\n=== tabpanel 관련 요소 검색 ===")
            tabpanels = tree.xpath('//*[contains(@id, "tabpanel")]')
            print(f"tabpanel 요소 개수: {len(tabpanels)}")
            
            for i, panel in enumerate(tabpanels[:10]):
                panel_id = panel.get('id', 'no-id')
                print(f"{i+1}. ID: {panel_id}")
                
                # 각 tabpanel 내부의 링크 확인
                links = panel.xpath('.//a[@href]')
                print(f"   링크 개수: {len(links)}")
                for j, link in enumerate(links[:3]):
                    href = link.get('href', '')
                    text = link.text_content().strip()[:50]
                    print(f"   {j+1}. {text} -> {href}")
            
            # earnings와 sec-filing 관련 요소 직접 검색
            print("\n=== earnings 관련 요소 검색 ===")
            earnings_elements = tree.xpath('//*[contains(@id, "earnings") or contains(text(), "earnings")]')
            print(f"earnings 관련 요소 개수: {len(earnings_elements)}")
            
            print("\n=== sec-filing 관련 요소 검색 ===")
            sec_elements = tree.xpath('//*[contains(@id, "sec") or contains(text(), "SEC")]')
            print(f"SEC 관련 요소 개수: {len(sec_elements)}")
            
            # 모든 링크에서 earnings나 sec 관련 찾기
            print("\n=== 전체 페이지에서 earnings/sec 링크 검색 ===")
            all_links = tree.xpath('//a[@href]')
            earnings_links = []
            sec_links = []
            
            for link in all_links:
                href = link.get('href', '')
                text = link.text_content().strip()
                
                if 'earnings' in href.lower() or 'earnings' in text.lower():
                    earnings_links.append((text[:50], href))
                elif 'sec' in href.lower() or 'filing' in href.lower():
                    sec_links.append((text[:50], href))
            
            print(f"Earnings 관련 링크: {len(earnings_links)}")
            for text, href in earnings_links[:5]:
                print(f"  - {text} -> {href}")
                
            print(f"SEC 관련 링크: {len(sec_links)}")
            for text, href in sec_links[:5]:
                print(f"  - {text} -> {href}")
                
        else:
            print("페이지 로드 실패")
            
    except Exception as e:
        print(f"오류 발생: {e}")

if __name__ == "__main__":
    debug_yahoo_structure()