"""
시장 지표 관련 API 라우트
"""
from fastapi import APIRouter
from core.service_manager import service_manager

router = APIRouter(prefix="/market", tags=["market"])


@router.get("/indices")
async def get_market_indices():
    """주요 지수 정보 조회"""
    return {"data": service_manager.get_market_indices()}


@router.get("/sectors")
async def get_sector_performance():
    """업종별 등락률 조회"""
    return {"data": service_manager.get_sector_performance()}


@router.get("/gainers")
async def get_top_gainers():
    """상승률 상위 종목 조회"""
    return {"data": service_manager.get_top_gainers()}


@router.get("/losers")
async def get_top_losers():
    """하락률 상위 종목 조회"""
    return {"data": service_manager.get_top_losers()}


@router.get("/volume")
async def get_volume_leaders():
    """거래량 상위 종목 조회"""
    return {"data": service_manager.get_volume_leaders()}