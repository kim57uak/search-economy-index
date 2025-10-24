"""
경제 지표 검색을 위한 MCP 서버
"""
import logging
from typing import Dict, Any
from mcp.server.fastmcp import FastMCP
from ticker_parser import TickerParser
from fnguide_parser import FnGuideParser


# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MCP 서버 생성
mcp = FastMCP("search-economy-index")

# 파서 인스턴스
ticker_parser = TickerParser()
fnguide_parser = FnGuideParser()


@mcp.tool(description="Search for Korean domestic stock ticker information from Naver Finance")
def search_domestic_ticker(query: str) -> Dict[str, Any]:
    """
    네이버 금융에서 국내 주식 티커 정보를 검색합니다.
    
    검색 결과에는 다음 정보가 포함됩니다:
    - 국내 티커 목록: 종목명, 종목코드 등
    - 실적속보: 최신 실적 발표 정보
    - 거래소공시: 공시 정보
    
    Args:
        query: 검색할 종목명 또는 티커 (예: "삼성전자", "005930")
        
    Returns:
        Dict[str, Any]: {
            "query": 검색어,
            "domestic_tickers": 국내 티커 목록,
            "earnings": 실적속보 정보,
            "disclosure": 거래소공시 정보
        }
    
    Example:
        search_domestic_ticker("삼성전자")
        # 삼성전자 관련 국내 티커 정보 반환
    """
    try:
        logger.info(f"국내 티커 검색: {query}")
        result = ticker_parser.search_ticker(query)
        return {
            "query": query,
            "domestic_tickers": result["domestic"],
            "earnings": result["earnings"],
            "disclosure": result["disclosure"]
        }
    except Exception as e:
        logger.error(f"국내 티커 검색 실패: {e}")
        return {"error": str(e)}


@mcp.tool(description="Search for international/overseas stock ticker information from Naver Finance")
def search_overseas_ticker(query: str) -> Dict[str, Any]:
    """
    네이버 금융에서 해외 주식 티커 정보를 검색합니다.
    
    검색 결과에는 다음 정보가 포함됩니다:
    - 해외 티커 목록: 종목명, 티커 심볼 등
    - 기타 정보: 관련 뉴스, 분석 정보 등
    
    Args:
        query: 검색할 종목명 또는 티커 (예: "Apple", "AAPL", "Tesla")
        
    Returns:
        Dict[str, Any]: {
            "query": 검색어,
            "overseas_tickers": 해외 티커 목록,
            "other": 기타 관련 정보
        }
    
    Example:
        search_overseas_ticker("AAPL")
        # Apple 관련 해외 티커 정보 반환
    """
    try:
        logger.info(f"해외 티커 검색: {query}")
        result = ticker_parser.search_ticker(query)
        return {
            "query": query,
            "overseas_tickers": result["overseas"],
            "other": result["other"]
        }
    except Exception as e:
        logger.error(f"해외 티커 검색 실패: {e}")
        return {"error": str(e)}


@mcp.tool(description="Get comprehensive Korean domestic stock snapshot with price, volume, and key metrics")
def get_stock_snapshot(ticker: str) -> Dict[str, Any]:
    """
    FnGuide에서 한국 국내 주식의 종합적인 스냅샷 정보를 조회합니다.
    
    주가, 거래량, 재무지표 및 한국 주식의 주요 성과 지표를 포함한
    상세한 주식 개요를 제공합니다.
    
    Args:
        ticker: 한국 주식 티커 심볼 (예: "005930" 삼성전자)
        
    Returns:
        종합적인 한국 주식 스냅샷 데이터를 포함한 딕셔너리
    """
    try:
        result = fnguide_parser.get_snapshot(ticker)
        return {"ticker": ticker, "snapshot": result}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool(description="Get detailed Korean company overview and business information")
def get_company_overview(ticker: str) -> Dict[str, Any]:
    """
    한국 기업의 상세한 기업 개요 및 사업 정보를 조회합니다.
    
    기업 프로필, 사업 설명, 주요 임원진 및
    기업 구조 정보를 제공합니다.
    
    Args:
        ticker: 한국 주식 티커 심볼 (예: "005930")
        
    Returns:
        한국 기업 개요 데이터를 포함한 딕셔너리
    """
    try:
        result = fnguide_parser.get_company_overview(ticker)
        return {"ticker": ticker, "company_overview": result}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool(description="Get Korean company financial statements including income statement, balance sheet, and cash flow")
def get_financial_statements(ticker: str) -> Dict[str, Any]:
    """
    한국 기업의 손익계산서, 대차대조표, 현금흐름표를 포함한 종합 재무제표를 조회합니다.
    
    매출, 이익, 자산, 부채, 현금흐름 정보를 포함한
    기본 분석을 위한 상세한 재무 데이터를 제공합니다.
    
    Args:
        ticker: 한국 주식 티커 심볼 (예: "005930")
        
    Returns:
        한국 기업 재무제표 데이터를 포함한 딕셔너리
    """
    try:
        result = fnguide_parser.get_financial_statement(ticker)
        return {"ticker": ticker, "financial_statements": result}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool(description="Get key financial ratios and metrics for Korean stock analysis")
def get_financial_ratios(ticker: str) -> Dict[str, Any]:
    """
    한국 주식 분석을 위한 주요 재무비율 및 지표를 조회합니다.
    
    재무 분석 및 주식 평가에 필수적인 수익성, 유동성,
    효율성, 레버리지 비율을 제공합니다.
    
    Args:
        ticker: 한국 주식 티커 심볼 (예: "005930")
        
    Returns:
        한국 주식 재무비율 데이터를 포함한 딕셔너리
    """
    try:
        result = fnguide_parser.get_financial_ratio(ticker)
        return {"ticker": ticker, "financial_ratios": result}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool(description="Get Korean stock investment indicators and valuation metrics like P/E, P/B ratios")
def get_investment_indicators(ticker: str) -> Dict[str, Any]:
    """
    한국 주식의 투자지표 및 밸류에이션 지표를 조회합니다.
    
    주식 평가를 위한 PER, PBR, 배당수익률 및
    기타 주요 투자 지표를 제공합니다.
    
    Args:
        ticker: 한국 주식 티커 심볼 (예: "005930")
        
    Returns:
        한국 주식 투자지표 데이터를 포함한 딕셔너리
    """
    try:
        result = fnguide_parser.get_investment_indicator(ticker)
        return {"ticker": ticker, "investment_indicators": result}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool(description="Get Korean stock analyst consensus, ratings, and price targets")
def get_analyst_consensus(ticker: str) -> Dict[str, Any]:
    """
    한국 주식의 애널리스트 컨센서스 및 추천 의견을 조회합니다.
    
    금융기관 및 리서치 회사의 애널리스트 등급,
    목표주가, 컨센서스 전망을 제공합니다.
    
    Args:
        ticker: 한국 주식 티커 심볼 (예: "005930")
        
    Returns:
        한국 주식 애널리스트 컨센서스 데이터를 포함한 딕셔너리
    """
    try:
        result = fnguide_parser.get_consensus(ticker)
        return {"ticker": ticker, "analyst_consensus": result}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool(description="Get Korean company shareholding structure and ownership analysis")
def get_ownership_analysis(ticker: str) -> Dict[str, Any]:
    """
    한국 기업의 주주구조 및 지분 분석 정보를 조회합니다.
    
    주요 주주, 기관 투자자 지분율 및
    주주구조 변화 패턴에 대한 정보를 제공합니다.
    
    Args:
        ticker: 한국 주식 티커 심볼 (예: "005930")
        
    Returns:
        한국 기업 지분 분석 데이터를 포함한 딕셔너리
    """
    try:
        result = fnguide_parser.get_share_analysis(ticker)
        return {"ticker": ticker, "ownership_analysis": result}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool(description="Get Korean industry sector analysis and trends comparison")
def get_industry_analysis(ticker: str) -> Dict[str, Any]:
    """
    한국 업종 섹터 분석 및 비교 정보를 조회합니다.
    
    업종 트렌드, 섹터 성과 및 동일 업종 그룹 내
    비교 분석을 제공합니다.
    
    Args:
        ticker: 한국 주식 티커 심볼 (예: "005930")
        
    Returns:
        한국 업종 분석 데이터를 포함한 딕셔너리
    """
    try:
        result = fnguide_parser.get_industry_analysis(ticker)
        return {"ticker": ticker, "industry_analysis": result}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool(description="Get Korean company competitor comparison and peer analysis")
def get_competitor_comparison(ticker: str) -> Dict[str, Any]:
    """
    한국 기업의 경쟁사 비교 및 동종업계 분석을 조회합니다.
    
    재무지표, 성과, 시장 지위 비교를 포함한
    업계 동종기업과의 비교 분석을 제공합니다.
    
    Args:
        ticker: 한국 주식 티커 심볼 (예: "005930")
        
    Returns:
        한국 기업 경쟁사 비교 데이터를 포함한 딕셔너리
    """
    try:
        result = fnguide_parser.get_competitor_comparison(ticker)
        return {"ticker": ticker, "competitor_comparison": result}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool(description="Get Korean stock exchange disclosures and regulatory filings")
def get_exchange_disclosures(ticker: str) -> Dict[str, Any]:
    """
    한국 거래소의 공식 공시 및 규제 신고서를 조회합니다.
    
    거래소의 공식 발표, 규제 신고서 및
    중요한 기업 공시 정보를 제공합니다.
    
    Args:
        ticker: 한국 주식 티커 심볼 (예: "005930")
        
    Returns:
        한국 거래소 공시 데이터를 포함한 딕셔너리
    """
    try:
        result = fnguide_parser.get_disclosure(ticker)
        return {"ticker": ticker, "exchange_disclosures": result}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool(description="Get latest Korean company earnings reports and financial results")
def get_earnings_reports(ticker: str) -> Dict[str, Any]:
    """
    한국 기업의 최신 실적 보고서 및 재무 결과를 조회합니다.
    
    기업의 분기별 및 연간 실적 보고서, 재무 결과 및
    성과 업데이트를 제공합니다.
    
    Args:
        ticker: 한국 주식 티커 심볼 (예: "005930")
        
    Returns:
        한국 기업 실적 보고서 데이터를 포함한 딕셔너리
    """
    try:
        result = fnguide_parser.get_earnings_report(ticker)
        return {"ticker": ticker, "earnings_reports": result}
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    mcp.run()