#!/usr/bin/env python3
"""
경제 지표 검색 HTTP API 서버
"""
import sys
import os
from fastapi import FastAPI

# 현재 디렉토리를 Python 경로에 추가
sys.path.insert(0, os.path.dirname(__file__))

# 도메인별 라우터들 import
from api_routes.ticker_routes import router as ticker_router
from api_routes.fnguide_routes import router as fnguide_router
from api_routes.materials_routes import materials_router, gold_router
from api_routes.exchange_routes import router as exchange_router

app = FastAPI(title="Search Economy Index API")

@app.get("/")
def root():
    return {"message": "Search Economy Index API"}

# 도메인별 라우터 등록
app.include_router(ticker_router)      # /search/*
app.include_router(fnguide_router)     # /fnguide/*
app.include_router(materials_router)   # /materials/*
app.include_router(gold_router)        # /gold/*
app.include_router(exchange_router)    # /exchange/*

def main():
    """HTTP API 서버 메인 함수"""
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()