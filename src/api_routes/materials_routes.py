"""
원자재 및 귀금속 관련 API 라우트
"""
from fastapi import APIRouter
from typing import Dict, Any
from parsers.materials_parser import MaterialsParser
from parsers.gold_parser import GoldParser

materials_router = APIRouter(prefix="/materials", tags=["materials"])
gold_router = APIRouter(prefix="/gold", tags=["gold"])

materials_parser = MaterialsParser()
gold_parser = GoldParser()

@materials_router.get("/energy")
def get_energy_futures() -> Dict[str, Any]:
    try:
        result = materials_parser.get_energy_futures()
        return {"energy_futures": result}
    except Exception as e:
        return {"error": str(e)}

@materials_router.get("/metals")
def get_non_ferrous_metals() -> Dict[str, Any]:
    try:
        result = materials_parser.get_non_ferrous_metals()
        return {"non_ferrous_metals": result}
    except Exception as e:
        return {"error": str(e)}

@materials_router.get("/agriculture")
def get_agriculture_futures() -> Dict[str, Any]:
    try:
        result = materials_parser.get_agriculture_futures()
        return {"agriculture_futures": result}
    except Exception as e:
        return {"error": str(e)}

@gold_router.get("/oil")
def get_oil_prices() -> Dict[str, Any]:
    try:
        result = gold_parser.get_oil_prices()
        return {"oil_prices": result}
    except Exception as e:
        return {"error": str(e)}

@gold_router.get("/precious")
def get_precious_metals() -> Dict[str, Any]:
    try:
        result = gold_parser.get_precious_metals()
        return {"precious_metals": result}
    except Exception as e:
        return {"error": str(e)}