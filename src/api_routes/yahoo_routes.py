"""
Yahoo Finance API 라우트
"""
from fastapi import APIRouter, HTTPException
from core.service_manager import service_manager

router = APIRouter(prefix="/yahoo", tags=["yahoo"])


@router.get("/global-indices")
async def get_global_indices():
    """글로벌 주요 지수 조회"""
    try:
        result = service_manager.get_global_indices()
        return {"data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/us-treasury")
async def get_us_treasury_yields():
    """미국 국채 수익률 조회"""
    try:
        result = service_manager.get_us_treasury_yields()
        return {"data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/vix")
async def get_vix_data():
    """VIX 공포지수 조회"""
    try:
        result = service_manager.get_vix_data()
        return {"data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/commodities")
async def get_commodities():
    """글로벌 원자재 가격 조회"""
    try:
        result = service_manager.get_commodities()
        return {"data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/forex")
async def get_forex_majors():
    """주요 환율 조회"""
    try:
        result = service_manager.get_forex_majors()
        return {"data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/asian-indices")
async def get_asian_indices():
    """아시아 주요 지수 조회"""
    try:
        result = service_manager.get_asian_indices()
        return {"data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/european-indices")
async def get_european_indices():
    """유럽 주요 지수 조회"""
    try:
        result = service_manager.get_european_indices()
        return {"data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sectors")
async def get_yahoo_sector_performance():
    """섹터별 성과 조회"""
    try:
        result = service_manager.get_yahoo_sector_performance()
        return {"data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stock/{symbol}")
async def get_stock_quote(symbol: str):
    """개별 주식 정보 조회 (Yahoo Finance)"""
    try:
        result = service_manager.get_stock_quote(symbol)
        return {"data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/domestic-stock/{ticker}")
async def get_domestic_stock_quote(ticker: str):
    """국내 개별 주식 정보 조회"""
    try:
        result = service_manager.get_domestic_stock_quote(ticker)
        return {"data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/crypto/{symbol}")
async def get_crypto_quote(symbol: str):
    """개별 암호화폐 정보 조회"""
    try:
        result = service_manager.get_crypto_quote(symbol)
        return {"data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))