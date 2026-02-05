from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Resume schemas
class ResumeUpload(BaseModel):
    user_id: Optional[int] = None

class ResumeResponse(BaseModel):
    id: int
    filename: str
    extracted_text: Optional[str]
    skills: Optional[List[str]]
    created_at: datetime
    
    class Config:
        from_attributes = True

# Job Description schemas
class JobDescriptionCreate(BaseModel):
    title: str
    description: str

class JobDescriptionResponse(BaseModel):
    id: int
    title: str
    description: str
    skills_required: Optional[List[str]]
    created_at: datetime
    
    class Config:
        from_attributes = True

# Skill Gap Analysis schemas
class SkillGapAnalysisRequest(BaseModel):
    resume_id: int
    job_description_id: Optional[int] = None
    job_description_text: Optional[str] = None

class SkillGapAnalysisResponse(BaseModel):
    id: int
    resume_id: int
    job_description_id: Optional[int]
    match_score: float
    missing_skills: List[str]
    weak_skills: List[str]
    strong_skills: List[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

# Learning Roadmap schemas
class LearningRoadmapResponse(BaseModel):
    id: int
    skill_gap_analysis_id: int
    roadmap_data: Dict[str, Any]
    recommendations: List[Dict[str, Any]]
    created_at: datetime
    
    class Config:
        from_attributes = True

# Match Score Response
class MatchScoreResponse(BaseModel):
    match_score: float
    skill_breakdown: Dict[str, Any]
    explanation: str

class MatchCalculateRequest(BaseModel):
    resume_text: str
    job_description: str
    job_title: Optional[str] = "Target Role"

class RoadmapGenerateRequest(BaseModel):
    missing_skills: List[str]
    target_role: Optional[str] = "Your Target Role"
