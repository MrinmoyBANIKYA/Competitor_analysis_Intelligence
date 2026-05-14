import os
import asyncio
import json
from fastapi import FastAPI, BackgroundTasks, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import time
import uuid
from datetime import datetime
import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession

# Import scrapers and DataFetcher
from data.scrapers import DataFetcher, SectorData
from data.sectors import SECTORS
from db.database import get_db
from db import crud

app = FastAPI(
    title="Sector Intelligence API",
    description="Backend API for sector analysis and report generation with DB persistence",
    version="1.1.0"
)

# CORS Middleware
origins = [
    "http://localhost:8501",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Start time for uptime calculation
start_time = time.time()

# Job store for background tasks (consider moving to Redis/DB for production)
jobs = {}

# --- Pydantic Models ---

class AnalysisRequest(BaseModel):
    sector: str
    companies: List[str]
    news_api_key: Optional[str] = ""

class AnalysisResponse(BaseModel):
    sector: str
    results: Dict[str, Any]
    health_score: float
    timestamp: datetime = Field(default_factory=datetime.now)

class HealthResponse(BaseModel):
    status: str
    version: str
    uptime: float

class ReportMetadata(BaseModel):
    sector: str
    last_generated: datetime
    file_path: str
    status: str
    gemini_summary: Optional[str] = None

class ReportGenerateRequest(BaseModel):
    sector: str
    companies: List[str]
    data: Dict[str, Any]

class JobResponse(BaseModel):
    job_id: str
    status: str

# --- Endpoints ---

@app.get("/health", response_model=HealthResponse)
async def health():
    return {
        "status": "ok",
        "version": "1.1.0",
        "uptime": time.time() - start_time
    }

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze(request: AnalysisRequest, db: AsyncSession = Depends(get_db)):
    if request.sector not in SECTORS:
        raise HTTPException(status_code=404, detail="Sector not found")
    
    sector_config = SECTORS[request.sector]
    fetcher = DataFetcher()
    
    try:
        # Run the async fetcher
        sector_data = await fetcher.fetch_all(
            sector_config=sector_config,
            companies=request.companies,
            news_api_key=request.news_api_key
        )
        
        # Persistence: Save snapshot to DB
        db_sector = await crud.get_or_create_sector(db, name=request.sector, slug=request.sector.lower().replace(' ', '-'))
        
        # Prepare results for JSON serialization
        serializable_results = {}
        for key, val in sector_data.results.items():
            if isinstance(val.get("data"), pd.DataFrame):
                val["data"] = val["data"].to_dict(orient="records")
            serializable_results[key] = val
        
        # Save snapshot
        await crud.create_trend_snapshot(
            db, 
            sector_id=db_sector.id,
            source="multi-source",
            raw_json=json.dumps(serializable_results),
            signal_score=float(sector_data.health_score)
        )
            
        return {
            "sector": request.sector,
            "results": serializable_results,
            "health_score": sector_data.health_score
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/report/{sector}", response_model=ReportMetadata)
async def get_report_metadata(sector: str, db: AsyncSession = Depends(get_db)):
    db_sector = await crud.get_or_create_sector(db, name=sector, slug=sector.lower().replace(' ', '-'))
    db_report = await crud.get_latest_report(db, sector_id=db_sector.id)
    
    if db_report:
        return {
            "sector": sector,
            "last_generated": db_report.generated_at,
            "file_path": db_report.pdf_path,
            "status": db_report.status,
            "gemini_summary": db_report.gemini_summary
        }
    
    # Fallback to file check if not in DB
    report_path = f"reports/{sector.lower().replace(' ', '_')}_report.pdf"
    if os.path.exists(report_path):
        return {
            "sector": sector,
            "last_generated": datetime.fromtimestamp(os.path.getmtime(report_path)),
            "file_path": report_path,
            "status": "available"
        }
    else:
        raise HTTPException(status_code=404, detail="Report not found")

async def generate_pdf_task(job_id: str, sector: str, companies: List[str], data: Dict[str, Any], db_session_factory: Any):
    jobs[job_id] = "running"
    try:
        # Simulate PDF generation
        await asyncio.sleep(5)
        
        # Persistence: Save report metadata
        async with db_session_factory() as db:
            db_sector = await crud.get_or_create_sector(db, name=sector, slug=sector.lower().replace(' ', '-'))
            await crud.create_report(
                db, 
                sector_id=db_sector.id,
                pdf_path=f"reports/{sector.lower().replace(' ', '_')}_report.pdf",
                gemini_summary="Automated AI summary generated for this intelligence report.",
                status="done"
            )
            
        jobs[job_id] = "done"
    except Exception as e:
        print(f"Error generating report: {e}")
        jobs[job_id] = "failed"

@app.post("/report/generate", response_model=JobResponse)
async def generate_report_endpoint(request: ReportGenerateRequest, background_tasks: BackgroundTasks):
    from db.database import AsyncSessionLocal
    job_id = str(uuid.uuid4())
    jobs[job_id] = "queued"
    background_tasks.add_task(generate_pdf_task, job_id, request.sector, request.companies, request.data, AsyncSessionLocal)
    return {"job_id": job_id, "status": "queued"}

@app.get("/report/status/{job_id}", response_model=JobResponse)
async def get_job_status(job_id: str):
    status = jobs.get(job_id)
    if not status:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"job_id": job_id, "status": status}
