import pytest
import httpx
import asyncio
from api.main import app
from db.database import Base, get_db
from db import models, crud
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite+aiosqlite:///./test_auth.db"

def test_auth_and_billing_lifecycle():
    import os
    if os.path.exists("test_auth.db"):
        try:
            os.remove("test_auth.db")
        except Exception:
            pass
            
    async def run_async_test():
        # Setup temporary SQLite database file
        engine = create_async_engine(DATABASE_URL, connect_args={"check_same_thread": False})
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            
        AsyncSessionLocal = sessionmaker(
            engine, class_=AsyncSession, expire_on_commit=False
        )
        
        async with AsyncSessionLocal() as session:
            # Override get_db dependency to use this transaction session
            async def override_get_db():
                yield session
                
            app.dependency_overrides[get_db] = override_get_db
            
            async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
                # 1. Test registration
                register_payload = {
                    "email": "saas_operator@nixtio.com",
                    "password": "nixtio_secure_pass_2026",
                    "org_name": "NixTio Operators Corp"
                }
                resp = await ac.post("/auth/register", json=register_payload)
                assert resp.status_code == 200
                data = resp.json()
                assert "access_token" in data
                assert "refresh_token" in data
                assert data["token_type"] == "bearer"
                
                access_token = data["access_token"]
                refresh_token = data["refresh_token"]
                
                # 2. Test login
                login_payload = {
                    "email": "saas_operator@nixtio.com",
                    "password": "nixtio_secure_pass_2026"
                }
                login_resp = await ac.post("/auth/login", json=login_payload)
                assert login_resp.status_code == 200
                assert "access_token" in login_resp.json()
                
                # 3. Test get user context (/auth/me)
                headers = {"Authorization": f"Bearer {access_token}"}
                me_resp = await ac.get("/auth/me", headers=headers)
                assert me_resp.status_code == 200
                me_data = me_resp.json()
                assert me_data["email"] == "saas_operator@nixtio.com"
                assert me_data["org_name"] == "NixTio Operators Corp"
                assert me_data["plan_tier"] == "free"
                
                # 4. Test Token Refresh Flow
                refresh_resp = await ac.post("/auth/refresh", json={"refresh_token": refresh_token})
                assert refresh_resp.status_code == 200
                refresh_data = refresh_resp.json()
                assert "access_token" in refresh_data
                assert "refresh_token" in refresh_data
                
                new_access_token = refresh_data["access_token"]
                new_headers = {"Authorization": f"Bearer {new_access_token}"}
                
                # 5. Test billing usage initial (0 / 5)
                usage_resp = await ac.get("/billing/usage", headers=new_headers)
                assert usage_resp.status_code == 200
                usage_data = usage_resp.json()
                assert usage_data["plan_tier"] == "free"
                assert usage_data["usage"] == 0
                assert usage_data["limit"] == 5
                
                # 6. Test report generation limit enforcement
                # Mock background task report generate
                from unittest.mock import patch, AsyncMock
                mock_run = AsyncMock()
                mock_run.return_value = {"analysis": {"executive_summary": "Mocked test summary"}}
                
                with patch("api.main.get_intel_chain", return_value=mock_run):
                    # Trigger 5 successful generations to hit limit
                    for i in range(5):
                        gen_resp = await ac.post("/report/generate", json={
                            "sector": "Fintech Payments",
                            "companies": ["PhonePe"],
                            "data": {}
                        }, headers=new_headers)
                        assert gen_resp.status_code == 200
                        
                    # The 6th should exceed limit
                    over_resp = await ac.post("/report/generate", json={
                        "sector": "Fintech Payments",
                        "companies": ["PhonePe"],
                        "data": {}
                    }, headers=new_headers)
                    assert over_resp.status_code == 403
                    assert over_resp.json()["detail"] == "Usage limit exceeded for plan tier"
                    
                    # Check usage billing shows 5 / 5
                    usage_resp_after = await ac.get("/billing/usage", headers=new_headers)
                    assert usage_resp_after.json()["usage"] == 5

            # Cleanup dependency overrides
            app.dependency_overrides.pop(get_db, None)
            
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        await engine.dispose()
        
        import os
        if os.path.exists("test_auth.db"):
            try:
                os.remove("test_auth.db")
            except Exception:
                pass
            
    # Run the async execution block in a synchronous loop context
    asyncio.run(run_async_test())
