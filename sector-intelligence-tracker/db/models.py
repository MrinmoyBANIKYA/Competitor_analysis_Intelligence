from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from db.database import Base

class Org(Base):
    __tablename__ = "orgs"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    plan_tier = Column(String, default="free")
    api_key_hash = Column(String, unique=True, index=True)
    users = relationship("User", back_populates="org")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    org_id = Column(Integer, ForeignKey("orgs.id"))
    role = Column(String, default="user")
    created_at = Column(DateTime, default=datetime.utcnow)
    org = relationship("Org", back_populates="users")

class Sector(Base):
    __tablename__ = "sectors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    slug = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    reports = relationship("Report", back_populates="sector")
    snapshots = relationship("TrendSnapshot", back_populates="sector")

class Report(Base):
    __tablename__ = "reports"
    id = Column(Integer, primary_key=True, index=True)
    sector_id = Column(Integer, ForeignKey("sectors.id"))
    generated_at = Column(DateTime, default=datetime.utcnow)
    pdf_path = Column(String)
    gemini_summary = Column(Text)
    status = Column(String, default="pending")
    sector = relationship("Sector", back_populates="reports")

class TrendSnapshot(Base):
    __tablename__ = "trend_snapshots"
    id = Column(Integer, primary_key=True, index=True)
    sector_id = Column(Integer, ForeignKey("sectors.id"))
    source = Column(String)
    captured_at = Column(DateTime, default=datetime.utcnow)
    raw_json = Column(Text) # or use JSON type for Postgres
    signal_score = Column(Float)
    sector = relationship("Sector", back_populates="snapshots")
