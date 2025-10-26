#!/usr/bin/env python3
"""
SEC 페이지 파싱 테스트
"""
import sys
sys.path.append('src')

from parsers.http_client import HttpClient

def test_sec_page_parsing():
    """SEC 페이지 구조 확인"""
    symbol = "AAPL"
    http_client = HttpClient()
    
    url = f"https://finance.yahoo.com/quote/{symbol}/sec-filings"
    print(f"테스트 URL: {url}")
    
    tree = http_client.fetch_utf8(url)
    if tree is not None:
        print("✅ 페이지 로드 성공")
        
        # 다양한 XPath로 링크 찾기
        xpaths = [
            '//a[contains(@href, "sec.gov")]',
            '//a[contains(@href, "edgar")]',
            '//a[contains(text(), "10-K")]',
            '//a[contains(text(), "10-Q")]',
            '//a[contains(text(), "8-K")]',
            '//a[@href]',  # 모든 링크
        ]
        
        for xpath in xpaths:
            links = tree.xpath(xpath)
            print(f"\nXPath: {xpath}")
            print(f"발견된 링크 수: {len(links)}")
            
            for i, link in enumerate(links[:5]):  # 처음 5개만
                href = link.get('href', '')
                text = link.text_content().strip()
                print(f"  {i+1}: {text[:50]} -> {href[:80]}")
    else:
        print("❌ 페이지 로드 실패")

if __name__ == "__main__":
    test_sec_page_parsing()