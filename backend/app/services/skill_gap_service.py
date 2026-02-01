from typing import List, Dict, Set
from loguru import logger
from app.services.skill_extractor import SkillExtractor

class SkillGapService:
    """Service for analyzing skill gaps between resume and job requirements."""
    
    @staticmethod
    def analyze_skill_gap(
        resume_skills: List[str],
        job_required_skills: List[str],
        market_demand: Dict[str, float] = None
    ) -> Dict[str, any]:
        """
        Analyze skill gap between resume and job requirements.
        
        Args:
            resume_skills: List of skills from resume
            job_required_skills: List of required skills from job description
            market_demand: Optional dictionary of skill: demand_score
            
        Returns:
            Dictionary containing gap analysis
        """
        resume_set = set(resume_skills)
        job_set = set(job_required_skills)
        
        # Missing skills: in job requirements but not in resume
        missing_skills = list(job_set - resume_set)
        
        # Strong skills: in both resume and job requirements
        strong_skills = list(resume_set & job_set)
        
        # Additional skills: in resume but not required (bonus skills)
        additional_skills = list(resume_set - job_set)
        
        # Calculate match percentage
        if len(job_required_skills) > 0:
            match_percentage = (len(strong_skills) / len(job_required_skills)) * 100
        else:
            match_percentage = 0.0
        
        # Prioritize missing skills by market demand if available
        missing_skills_prioritized = missing_skills
        if market_demand:
            missing_skills_prioritized = sorted(
                missing_skills,
                key=lambda s: market_demand.get(s, 0),
                reverse=True
            )
        
        # Weak skills (skills that appear in resume but might need strengthening)
        # For now, we'll consider skills mentioned but not strongly demonstrated
        # This would need more sophisticated analysis in production
        weak_skills = []
        
        return {
            "match_percentage": round(match_percentage, 2),
            "missing_skills": missing_skills_prioritized,
            "strong_skills": strong_skills,
            "weak_skills": weak_skills,
            "additional_skills": additional_skills,
            "total_resume_skills": len(resume_skills),
            "total_required_skills": len(job_required_skills),
            "skills_matched": len(strong_skills)
        }
    
    @staticmethod
    def generate_skill_heatmap_data(
        resume_skills: List[str],
        job_required_skills: List[str]
    ) -> List[Dict[str, any]]:
        """
        Generate data for skill heatmap visualization.
        
        Returns:
            List of skill objects with strength levels
        """
        resume_set = set(resume_skills)
        job_set = set(job_required_skills)
        
        heatmap_data = []
        
        # Process all unique skills
        all_skills = set(resume_skills + job_required_skills)
        
        for skill in all_skills:
            in_resume = skill in resume_set
            in_job = skill in job_set
            
            # Determine strength level and color
            if in_resume and in_job:
                strength = "high"
                color = "green"
                level = 3
            elif in_resume and not in_job:
                strength = "medium"
                color = "blue"
                level = 2
            elif not in_resume and in_job:
                strength = "missing"
                color = "red"
                level = 0
            else:
                strength = "low"
                color = "yellow"
                level = 1
            
            # Get skill hierarchy
            hierarchy = SkillExtractor.get_skill_hierarchy(skill)
            
            heatmap_data.append({
                "skill": SkillExtractor.normalize_skills([skill])[0],
                "strength": strength,
                "level": level,
                "color": color,
                "in_resume": in_resume,
                "in_job_requirement": in_job,
                "domain": hierarchy["domain"]
            })
        
        # Sort by level (missing first, then low, medium, high)
        heatmap_data.sort(key=lambda x: x["level"])
        
        return heatmap_data
    
    @staticmethod
    def calculate_match_score(
        semantic_similarity: float,
        skill_match_percentage: float,
        weights: Dict[str, float] = None
    ) -> float:
        """
        Calculate overall match score combining semantic similarity and skill match.
        
        Args:
            semantic_similarity: Cosine similarity score (0-1)
            skill_match_percentage: Percentage of skills matched (0-100)
            weights: Optional weights for combining scores
            
        Returns:
            Combined match score (0-100)
        """
        if weights is None:
            weights = {
                "semantic": 0.4,
                "skill": 0.6
            }
        
        # Normalize skill match to 0-1
        skill_match_normalized = skill_match_percentage / 100
        
        # Calculate weighted score
        match_score = (
            weights["semantic"] * semantic_similarity +
            weights["skill"] * skill_match_normalized
        ) * 100
        
        return round(match_score, 2)
