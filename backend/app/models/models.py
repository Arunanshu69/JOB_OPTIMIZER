from sqlalchemy import Column, Integer, String, Text, DateTime, Float, JSON
from sqlalchemy.sql import func
from app.core.database import Base

class User(Base):
    """User model."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Resume(Base):
    """Resume model."""
    __tablename__ = "resumes"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    extracted_text = Column(Text)
    skills = Column(JSON)  # List of extracted skills
    embedding = Column(JSON)  # Vector embedding
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class JobDescription(Base):
    """Job Description model."""
    __tablename__ = "job_descriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    skills_required = Column(JSON)  # List of required skills
    embedding = Column(JSON)  # Vector embedding
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class SkillGapAnalysis(Base):
    """Skill Gap Analysis model."""
    __tablename__ = "skill_gap_analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, index=True)
    job_description_id = Column(Integer, index=True)
    match_score = Column(Float)
    missing_skills = Column(JSON)  # List of missing skills
    weak_skills = Column(JSON)  # List of weak skills
    strong_skills = Column(JSON)  # List of strong skills
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class LearningRoadmap(Base):
    """Learning Roadmap model."""
    __tablename__ = "learning_roadmaps"
    
    id = Column(Integer, primary_key=True, index=True)
    skill_gap_analysis_id = Column(Integer, index=True)
    roadmap_data = Column(JSON)  # Complete roadmap structure
    recommendations = Column(JSON)  # Course recommendations
    created_at = Column(DateTime(timezone=True), server_default=func.now())
