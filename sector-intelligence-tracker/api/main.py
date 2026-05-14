import os
import asyncio
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import time
import uuid
from datetime import datetime
import pandas as pd

# Import scrapers and DataFetcher
from data.scrapers import DataFetcher, SectorData
from data.sectors import SECTORS

app = FastAPI(
    title="Sector Intelligence API",
    description="Backend API for sector analysis and report generation",
    version="1.0.0"
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

# Job store for background tasks
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

class ReportGenerateRequest(BaseModel):
    sector: str
    companies: List[str]
    data: Dict[str, Any] # Pass the analyzed data to generate report

class JobResponse(BaseModel):
    job_id: str
    status: str

# --- Endpoints ---

@app.get("/health", response_model=HealthResponse)
async def health():
    return {
        "status": "ok",
        "version": "1.0.0",
        "uptime": time.time() - start_time
    }

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze(request: AnalysisRequest):
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
        
        # Prepare results for JSON serialization
        # Convert DataFrames to dicts
        serializable_results = {}
        for key, val in sector_data.results.items():
            if isinstance(val.get("data"), pd.DataFrame):
                val["data"] = val["data"].to_dict(orient="records")
            serializable_results[key] = val
            
        return {
            "sector": request.sector,
            "results": serializable_results,
            "health_score": sector_data.health_score
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/report/{sector}", response_model=ReportMetadata)
async def get_report_metadata(sector: str):
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

async def generate_pdf_task(job_id: str, sector: str, companies: List[str], data: Dict[str, Any]):
    jobs[job_id] = "running"
    try:
        # Here you would call your actual PDF generation logic
        # For now, we simulate with a sleep
        from reports.pdf_generator import generate_report
        # We need to reconstruct DataFrames for the report generator if it expects them
        # ... (implementation details omitted for brevity, assuming mock generation)
        await asyncio.sleep(5)
        jobs[job_id] = "done"
    except Exception as e:
        print(f"Error generating report: {e}")
        jobs[job_id] = "failed"

@app.post("/report/generate", response_model=JobResponse)
async def generate_report_endpoint(request: ReportGenerateRequest, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())
    jobs[job_id] = "queued"
    background_tasks.add_task(generate_pdf_task, job_id, request.sector, request.companies, request.data)
    return {"job_id": job_id, "status": "queued"}

@app.get("/report/status/{job_id}", response_model=JobResponse)
async def get_job_status(job_id: str):
    status = jobs.get(job_id)
    if not status:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"job_id": job_id, "status": status}
