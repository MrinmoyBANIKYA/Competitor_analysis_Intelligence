import pytest
import httpx
import sys
import os
from pathlib import Path

# Add project root to sys.path
sys.path.append(os.path.join(os.getcwd(), "sector-intelligence-tracker"))

@pytest.mark.asyncio
async def test_health_endpoint():
    async with httpx.AsyncClient(base_url="http://localhost:8000") as ac:
        try:
            response = await ac.get("/health")
            assert response.status_code == 200
            assert response.json()["status"] == "ok"
        except httpx.ConnectError:
            pytest.skip("FastAPI server is not running")

@pytest.mark.asyncio
async def test_analyze_endpoint():
    payload = {
        "sector": "Fintech Payments",
        "companies": ["Paytm", "PhonePe"]
    }
    async with httpx.AsyncClient(base_url="http://localhost:8000") as ac:
        try:
            response = await ac.post("/analyze", json=payload)
            assert response.status_code == 200
            data = response.json()
            assert "trends" in data
            assert "ratings" in data
        except httpx.ConnectError:
            pytest.skip("FastAPI server is not running")

@pytest.mark.asyncio
async def test_report_workflow():
    payload = {
        "sector": "Fintech Payments",
        "companies": ["Paytm"]
    }
    async with httpx.AsyncClient(base_url="http://localhost:8000") as ac:
        try:
            # 1. Trigger generation
            resp_gen = await ac.post("/report/generate", json=payload)
            assert resp_gen.status_code == 200
            job_id = resp_gen.json()["job_id"]
            
            # 2. Check status
            resp_status = await ac.get(f"/report/status/{job_id}")
            assert resp_status.status_code == 200
            data = resp_status.json()
            assert data["status"] in ["queued", "running", "done"], f"Job failed with: {data.get('error')}"
        except httpx.ConnectError:
            pytest.skip("FastAPI server is not running")
