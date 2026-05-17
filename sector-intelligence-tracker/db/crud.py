from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from db import models
from datetime import datetime
from typing import List, Optional

# --- Org CRUD ---
async def create_org(db: AsyncSession, name: str, api_key_hash: str, plan_tier: str = "free"):
    db_org = models.Org(name=name, api_key_hash=api_key_hash, plan_tier=plan_tier)
    db.add(db_org)
    await db.commit()
    await db.refresh(db_org)
    return db_org

async def get_org_by_api_key(db: AsyncSession, api_key_hash: str):
    result = await db.execute(select(models.Org).where(models.Org.api_key_hash == api_key_hash))
    return result.scalars().first()

# --- User CRUD ---
async def create_user(db: AsyncSession, email: str, hashed_password: str, org_id: int, role: str = "user"):
    db_user = models.User(email=email, hashed_password=hashed_password, org_id=org_id, role=role)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(models.User).where(models.User.email == email))
    return result.scalars().first()

# --- Sector CRUD ---
async def get_or_create_sector(db: AsyncSession, name: str, slug: str):
    result = await db.execute(select(models.Sector).where(models.Sector.slug == slug))
    db_sector = result.scalars().first()
    if not db_sector:
        db_sector = models.Sector(name=name, slug=slug)
        db.add(db_sector)
        await db.commit()
        await db.refresh(db_sector)
    return db_sector

# --- Report CRUD ---
async def create_report(db: AsyncSession, sector_id: int, pdf_path: str, gemini_summary: str, status: str = "done"):
    db_report = models.Report(
        sector_id=sector_id, 
        pdf_path=pdf_path, 
        gemini_summary=gemini_summary, 
        status=status
    )
    db.add(db_report)
    await db.commit()
    await db.refresh(db_report)
    return db_report

async def get_latest_report(db: AsyncSession, sector_id: int):
    result = await db.execute(
        select(models.Report)
        .where(models.Report.sector_id == sector_id)
        .order_by(models.Report.generated_at.desc())
    )
    return result.scalars().first()

# --- Snapshot CRUD ---
async def create_trend_snapshot(db: AsyncSession, sector_id: int, source: str, raw_json: str, signal_score: float):
    db_snapshot = models.TrendSnapshot(
        sector_id=sector_id,
        source=source,
        raw_json=raw_json,
        signal_score=signal_score
    )
    db.add(db_snapshot)
    await db.commit()
    await db.refresh(db_snapshot)
    return db_snapshot

async def get_snapshots_for_sector(db: AsyncSession, sector_id: int, limit: int = 10):
    result = await db.execute(
        select(models.TrendSnapshot)
        .where(models.TrendSnapshot.sector_id == sector_id)
        .order_by(models.TrendSnapshot.captured_at.desc())
        .limit(limit)
    )
    return result.scalars().all()

# --- RefreshToken CRUD ---
async def create_refresh_token(db: AsyncSession, user_id: int, token: str, expires_at: datetime):
    db_token = models.RefreshToken(user_id=user_id, token=token, expires_at=expires_at)
    db.add(db_token)
    await db.commit()
    await db.refresh(db_token)
    return db_token

async def get_refresh_token(db: AsyncSession, token: str):
    result = await db.execute(select(models.RefreshToken).where(models.RefreshToken.token == token))
    return result.scalars().first()

async def delete_refresh_token(db: AsyncSession, token: str):
    await db.execute(delete(models.RefreshToken).where(models.RefreshToken.token == token))
    await db.commit()

# --- UsageEvent CRUD ---
async def log_usage_event(db: AsyncSession, org_id: int, event_type: str, metadata: dict = None):
    db_event = models.UsageEvent(org_id=org_id, event_type=event_type, metadata_json=metadata or {})
    db.add(db_event)
    await db.commit()
    await db.refresh(db_event)
    return db_event

async def get_org_usage_for_month(db: AsyncSession, org_id: int, year: int, month: int):
    from sqlalchemy import extract, func
    result = await db.execute(
        select(func.count(models.UsageEvent.id))
        .where(models.UsageEvent.org_id == org_id)
        .where(models.UsageEvent.event_type == "report_generation")
        .where(extract('year', models.UsageEvent.timestamp) == year)
        .where(extract('month', models.UsageEvent.timestamp) == month)
    )
    return result.scalar() or 0
