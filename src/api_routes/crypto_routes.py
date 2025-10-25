"""
암호화폐 관련 API 라우트
"""
from fastapi import APIRouter
from ..core.service_manager import service_manager

router = APIRouter(prefix="/crypto", tags=["crypto"])


@router.get("/data")
async def get_crypto_data():
    """암호화폐 시장 데이터 조회"""
    return {"data": service_manager.get_crypto_data()}