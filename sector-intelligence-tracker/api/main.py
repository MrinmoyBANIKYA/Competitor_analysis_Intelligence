import sys
import os
import uuid
import datetime
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any, Optional

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from data.scrapers import DataFetcher, SectorData
from data.sectors import SECTORS
from reports.pdf_generator import generate_report, save_report

app = FastAPI(
    title="NixTio Sector Intelligence API",
    description="Backend API for real-time sector analysis and report generation.",
    version="1.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "https://nixtio-sector-analysis.streamlit.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Job Status Store (In-memory for demo, should be Redis/DB for production)
jobs = {}

# Pydantic Models
class AnalyzeRequest(BaseModel):
    sector: str
    companies: List[str]

class ReportGenerateRequest(BaseModel):
    sector: str
    companies: List[str]
    data: Optional[Dict[str, Any]] = None

def serialize_results(results: Dict[str, Any]) -> Dict[str, Any]:
    """Helper to convert DataFrames to dicts for JSON serialization."""
    serialized = {}
    for key, val in results.items():
        item = val.copy()
        data = item.get("data")
        if isinstance(data, pd.DataFrame):
            # Reset index to include date in trends
            df_to_ser = data.reset_index()
            # Convert to dict and handle NaN (JSON doesn't allow NaN)
            item["data"] = df_to_ser.replace({float('nan'): None}).to_dict(orient="records")
        
        # Handle datetime objects in the item itself (like last_updated)
        if isinstance(item.get("last_updated"), datetime.datetime):
            item["last_updated"] = item["last_updated"].isoformat()
            
        serialized[key] = item
    return serialized

# Endpoints
@app.get("/health")
async def health():
    return {
        "status": "ok",
        "version": "1.0.0",
        "uptime": "N/A"
    }

@app.post("/analyze")
async def analyze(request: AnalyzeRequest):
    fetcher = DataFetcher()
    sector_config = SECTORS.get(request.sector, {"name": request.sector, "companies": request.companies})
    news_api_key = os.getenv("NEWS_API_KEY", "")
    try:
        data = await fetcher.fetch_all(sector_config, request.companies, news_api_key)
        return serialize_results(data.results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/report/{sector}")
async def get_report_metadata(sector: str):
    return {
        "sector": sector,
        "last_generated": datetime.datetime.now().isoformat(),
        "status": "available"
    }

async def run_report_generation(job_id: str, sector: str, companies: list, data: dict = None):
    jobs[job_id]["status"] = "running"
    try:
        if not data:
            fetcher = DataFetcher()
            sector_config = SECTORS.get(sector, {"name": sector, "companies": companies})
            news_api_key = os.getenv("NEWS_API_KEY", "")
            sector_data = await fetcher.fetch_all(sector_config, companies, news_api_key)
            data = sector_data.results
        else:
            # Convert dicts back to DataFrames if needed for pdf_generator
            if "trends" in data and isinstance(data["trends"].get("data"), list):
                data["trends"]["data"] = pd.DataFrame(data["trends"]["data"])
                if "date" in data["trends"]["data"].columns:
                    data["trends"]["data"].set_index("date", inplace=True)

        # Build PDF
        pdf_bytes = generate_report(
            sector_name=sector,
            company_name=companies[0] if companies else "Unknown",
            df_ratings=data.get("ratings", {}).get("data", {}),
            df_hiring=data.get("jobs", {}).get("data", {}),
            df_news=data.get("news", {}).get("data", {}),
            df_glassdoor=data.get("employer", {}).get("data", {}),
            insight_text="Strategic analysis synthesized by NixTio AI Engine.",
            trends_df=data.get("trends", {}).get("data", pd.DataFrame())
        )
        
        filename = f"report_{sector}_{job_id[:8]}"
        filepath = save_report(pdf_bytes, filename)
        
        jobs[job_id]["status"] = "done"
        jobs[job_id]["finished_at"] = datetime.datetime.now().isoformat()
        jobs[job_id]["report_url"] = filepath
    except Exception as e:
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["error"] = str(e)

@app.post("/report/generate")
async def generate_report_endpoint(request: ReportGenerateRequest, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())
    jobs[job_id] = {
        "job_id": job_id,
        "status": "queued",
        "created_at": datetime.datetime.now().isoformat()
    }
    background_tasks.add_task(run_report_generation, job_id, request.sector, request.companies, request.data)
    return {"job_id": job_id}

@app.get("/report/status/{job_id}")
async def get_job_status(job_id: str):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    return jobs[job_id]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
