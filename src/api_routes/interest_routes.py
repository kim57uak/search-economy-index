"""
금리 및 채권 관련 API 라우트
"""
from fastapi import APIRouter
from core.service_manager import service_manager

router = APIRouter(prefix="/interest", tags=["interest"])


@router.get("/rates")
async def get_interest_rates():
    """기준금리 및 주요 금리 조회"""
    return {"data": service_manager.get_interest_rates()}


@router.get("/bonds")
async def get_bond_yields():
    """국고채 수익률 조회"""
    return {"data": service_manager.get_bond_yields()}


@router.get("/cd")
async def get_cd_rates():
    """CD금리 조회"""
    return {"data": service_manager.get_cd_rates()}


@router.get("/corporate")
async def get_corporate_bonds():
    """회사채 수익률 조회"""
    return {"data": service_manager.get_corporate_bonds()}