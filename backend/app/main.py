from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import shutil
from typing import Optional
from loguru import logger

from app.core.config import settings
from app.core.database import engine, Base
from app.services import (
    ResumeParser,
    SkillExtractor,
    embedding_service,
    SkillGapService
)
from app.schemas.schemas import (
    JobDescriptionCreate,
    SkillGapAnalysisRequest,
    MatchScoreResponse,
    MatchCalculateRequest,
    RoadmapGenerateRequest
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    debug=settings.DEBUG
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create upload directory
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Career Path Optimizer API",
        "version": settings.VERSION,
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

@app.post("/api/resume/upload")
async def upload_resume(file: UploadFile = File(...)):
    """
    Upload and parse a resume file.
    
    Supports PDF and DOCX formats.
    """
    try:
        # Validate file extension
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in settings.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file format. Allowed: {', '.join(settings.ALLOWED_EXTENSIONS)}"
            )
        
        # Save uploaded file
        file_path = os.path.join(settings.UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        logger.info(f"Resume uploaded: {file.filename}")
        
        # Parse resume
        extracted_text = ResumeParser.parse_resume(file_path, file.filename)
        if not extracted_text:
            raise HTTPException(
                status_code=400,
                detail="Failed to extract text from resume. Please ensure the file is readable."
            )
        
        # Clean text
        cleaned_text = ResumeParser.clean_text(extracted_text)
        
        # Extract skills
        skills = SkillExtractor.extract_skills(cleaned_text)
        normalized_skills = SkillExtractor.normalize_skills(skills)
        
        # Generate embedding
        embedding = embedding_service.generate_embedding(cleaned_text)
        
        logger.info(f"Extracted {len(skills)} skills from resume")
        
        return {
            "success": True,
            "filename": file.filename,
            # Return full text for downstream matching; include a short excerpt for UI if needed.
            "extracted_text": cleaned_text,
            "excerpt": cleaned_text[:500] + "..." if len(cleaned_text) > 500 else cleaned_text,
            "text_length": len(cleaned_text),
            "skills": normalized_skills,
            "skill_count": len(normalized_skills),
            "file_path": file_path,
            "embedding_generated": embedding is not None
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing resume: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/job/analyze")
async def analyze_job_description(job_data: JobDescriptionCreate):
    """
    Analyze a job description and extract required skills.
    """
    try:
        # Extract skills from job description
        skills = SkillExtractor.extract_skills(job_data.description)
        normalized_skills = SkillExtractor.normalize_skills(skills)
        
        # Generate embedding
        embedding = embedding_service.generate_embedding(job_data.description)
        
        logger.info(f"Analyzed job: {job_data.title}, found {len(skills)} skills")
        
        return {
            "success": True,
            "title": job_data.title,
            "skills_required": normalized_skills,
            "skill_count": len(normalized_skills),
            "embedding_generated": embedding is not None
        }
    
    except Exception as e:
        logger.error(f"Error analyzing job description: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/match/calculate")
async def calculate_match(payload: MatchCalculateRequest):
    """
    Calculate semantic match between resume and job description.
    
    Returns match score, skill breakdown, and gap analysis.
    """
    try:
        # Extract text and skills from resume
        resume_skills = SkillExtractor.extract_skills(payload.resume_text)
        resume_skills_normalized = SkillExtractor.normalize_skills(resume_skills)
        
        # Extract skills from job description
        job_skills = SkillExtractor.extract_skills(payload.job_description)
        if not job_skills:
            role_seed = f"{payload.job_title} {payload.job_description}"
            job_skills = SkillExtractor.infer_skills_from_role(role_seed)
        job_skills_normalized = SkillExtractor.normalize_skills(job_skills)
        
        # Generate embeddings
        resume_embedding = embedding_service.generate_embedding(payload.resume_text)
        job_embedding = embedding_service.generate_embedding(payload.job_description)
        
        if not resume_embedding or not job_embedding:
            raise HTTPException(
                status_code=500,
                detail="Failed to generate embeddings"
            )
        
        # Calculate semantic similarity
        semantic_similarity = embedding_service.compute_similarity(
            resume_embedding,
            job_embedding
        )
        
        # Perform skill gap analysis
        gap_analysis = SkillGapService.analyze_skill_gap(
            resume_skills,
            job_skills
        )
        
        # Calculate combined match score
        match_score = SkillGapService.calculate_match_score(
            semantic_similarity,
            gap_analysis["match_percentage"]
        )
        
        # Generate heatmap data
        heatmap_data = SkillGapService.generate_skill_heatmap_data(
            resume_skills,
            job_skills
        )
        
        # Generate explanation
        explanation = f"Based on semantic analysis and skill matching, your resume has a {match_score:.1f}% compatibility with the {payload.job_title} role. "
        explanation += f"You match {gap_analysis['skills_matched']} out of {gap_analysis['total_required_skills']} required skills. "
        
        if gap_analysis['missing_skills']:
            explanation += f"Key missing skills include: {', '.join(gap_analysis['missing_skills'][:3])}. "
        
        logger.info(f"Match calculated: {match_score}% for {payload.job_title}")
        
        return {
            "success": True,
            "match_score": match_score,
            "semantic_similarity": round(semantic_similarity * 100, 2),
            "skill_match_percentage": gap_analysis["match_percentage"],
            "skill_breakdown": {
                "resume_skills": resume_skills_normalized,
                "required_skills": job_skills_normalized,
                "matched_skills": [SkillExtractor.normalize_skills([s])[0] for s in gap_analysis["strong_skills"]],
                "missing_skills": [SkillExtractor.normalize_skills([s])[0] for s in gap_analysis["missing_skills"]],
                "additional_skills": [SkillExtractor.normalize_skills([s])[0] for s in gap_analysis["additional_skills"]]
            },
            "heatmap_data": heatmap_data,
            "explanation": explanation
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error calculating match: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/roadmap/generate")
async def generate_roadmap(payload: RoadmapGenerateRequest):
    """
    Generate a 6-month learning roadmap based on missing skills.
    """
    try:
        # Simple roadmap generation (can be enhanced with LLM)
        roadmap = {
            "target_role": payload.target_role,
            "duration_months": 6,
            "milestones": []
        }
        
        # Distribute skills across 6 months
        skills_per_month = max(1, len(payload.missing_skills) // 6)
        
        for month in range(1, 7):
            start_idx = (month - 1) * skills_per_month
            end_idx = start_idx + skills_per_month if month < 6 else len(payload.missing_skills)
            
            month_skills = payload.missing_skills[start_idx:end_idx]
            
            if month_skills:
                roadmap["milestones"].append({
                    "month": month,
                    "title": f"Month {month}: {', '.join(month_skills[:2])}",
                    "skills": month_skills,
                    "focus_areas": month_skills,
                    "estimated_hours": len(month_skills) * 20
                })
        
        # Course recommendations
        recommendations = []
        for skill in payload.missing_skills[:5]:  # Top 5 skills
            recommendations.append({
                "skill": skill,
                "platform": "Coursera / NPTEL",
                "course_name": f"{skill} Fundamentals",
                "duration": "4-6 weeks",
                "roi_score": 85,
                "relevance": "High"
            })
        
        logger.info(f"Generated roadmap for {payload.target_role}")
        
        return {
            "success": True,
            "roadmap": roadmap,
            "recommendations": recommendations
        }
    
    except Exception as e:
        logger.error(f"Error generating roadmap: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=settings.DEBUG)
