"""
환율 관련 API 라우트
"""
from fastapi import APIRouter
from typing import Dict, Any
from parsers.exchange_parser import ExchangeParser

router = APIRouter(prefix="/exchange", tags=["exchange"])
exchange_parser = ExchangeParser()

@router.get("/domestic")
def get_domestic_exchange() -> Dict[str, Any]:
    try:
        result = exchange_parser.get_domestic_exchange()
        return {"domestic_exchange": result}
    except Exception as e:
        return {"error": str(e)}

@router.get("/world")
def get_world_exchange() -> Dict[str, Any]:
    try:
        result = exchange_parser.get_world_exchange()
        return {"world_exchange": result}
    except Exception as e:
        return {"error": str(e)}