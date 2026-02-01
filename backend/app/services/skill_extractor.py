import re
from typing import List, Dict, Set
from loguru import logger

class SkillExtractor:
    """Service for extracting and normalizing skills from text."""
    
    # Comprehensive skill database
    SKILL_DATABASE = {
        # Programming Languages
        "python": ["python", "py", "python3"],
        "javascript": ["javascript", "js", "node.js", "nodejs", "node"],
        "java": ["java", "java8", "java11"],
        "cpp": ["c++", "cpp", "cplusplus"],
        "c": ["c programming", "c language"],
        "csharp": ["c#", "csharp", "c sharp"],
        "go": ["golang", "go lang", "go"],
        "rust": ["rust", "rust lang"],
        "typescript": ["typescript", "ts"],
        "r": ["r programming", "r language"],
        "sql": ["sql", "mysql", "postgresql", "postgres"],
        
        # Web Technologies
        "react": ["react", "reactjs", "react.js"],
        "angular": ["angular", "angularjs"],
        "vue": ["vue", "vuejs", "vue.js"],
        "html": ["html", "html5"],
        "css": ["css", "css3", "scss", "sass"],
        "django": ["django", "django framework"],
        "flask": ["flask", "flask framework"],
        "fastapi": ["fastapi", "fast api"],
        "express": ["express", "expressjs", "express.js"],
        "nextjs": ["next.js", "nextjs", "next"],
        
        # Machine Learning & AI
        "machine_learning": ["machine learning", "ml", "artificial intelligence", "ai"],
        "deep_learning": ["deep learning", "dl", "neural networks"],
        "tensorflow": ["tensorflow", "tf"],
        "pytorch": ["pytorch", "torch"],
        "keras": ["keras"],
        "scikit_learn": ["scikit-learn", "sklearn", "scikit learn"],
        "nlp": ["nlp", "natural language processing", "text processing"],
        "computer_vision": ["computer vision", "cv", "image processing"],
        "reinforcement_learning": ["reinforcement learning", "rl"],
        
        # Data Science
        "data_science": ["data science", "data scientist"],
        "data_analysis": ["data analysis", "data analyst"],
        "pandas": ["pandas"],
        "numpy": ["numpy"],
        "matplotlib": ["matplotlib"],
        "seaborn": ["seaborn"],
        "tableau": ["tableau"],
        "power_bi": ["power bi", "powerbi"],
        
        # Cloud & DevOps
        "aws": ["aws", "amazon web services"],
        "azure": ["azure", "microsoft azure"],
        "gcp": ["gcp", "google cloud", "google cloud platform"],
        "docker": ["docker", "containerization"],
        "kubernetes": ["kubernetes", "k8s"],
        "jenkins": ["jenkins", "ci/cd"],
        "terraform": ["terraform"],
        "ansible": ["ansible"],
        
        # Databases
        "mongodb": ["mongodb", "mongo"],
        "redis": ["redis"],
        "elasticsearch": ["elasticsearch", "elastic"],
        "cassandra": ["cassandra"],
        "dynamodb": ["dynamodb"],
        
        # Other Skills
        "git": ["git", "github", "gitlab", "version control"],
        "agile": ["agile", "scrum", "kanban"],
        "rest_api": ["rest", "restful", "rest api"],
        "graphql": ["graphql", "graph ql"],
        "microservices": ["microservices", "microservice architecture"],
    }
    
    # Skill to domain mapping
    SKILL_TO_DOMAIN = {
        "pytorch": "Deep Learning",
        "tensorflow": "Deep Learning",
        "keras": "Deep Learning",
        "numpy": "Numerical Computing",
        "pandas": "Data Analysis",
        "scikit_learn": "Machine Learning",
        "react": "Frontend Development",
        "angular": "Frontend Development",
        "vue": "Frontend Development",
        "django": "Backend Development",
        "flask": "Backend Development",
        "fastapi": "Backend Development",
        "aws": "Cloud Computing",
        "azure": "Cloud Computing",
        "gcp": "Cloud Computing",
        "docker": "DevOps",
        "kubernetes": "DevOps",
    }
    
    @staticmethod
    def extract_skills(text: str) -> List[str]:
        """
        Extract skills from text using pattern matching.
        
        Args:
            text: Input text (resume or job description)
            
        Returns:
            List of normalized skill names
        """
        text_lower = text.lower()
        found_skills = set()
        
        # Search for each skill pattern
        for normalized_skill, patterns in SkillExtractor.SKILL_DATABASE.items():
            for pattern in patterns:
                # Use word boundaries for accurate matching
                if re.search(r'\b' + re.escape(pattern) + r'\b', text_lower):
                    found_skills.add(normalized_skill)
                    break
        
        return sorted(list(found_skills))
    
    @staticmethod
    def normalize_skills(skills: List[str]) -> List[str]:
        """Normalize skill names to canonical form."""
        normalized = []
        for skill in skills:
            # Replace underscores with spaces and capitalize
            normalized_skill = skill.replace("_", " ").title()
            normalized.append(normalized_skill)
        return normalized
    
    @staticmethod
    def map_skill_to_domain(skill: str) -> str:
        """Map a skill to its domain."""
        return SkillExtractor.SKILL_TO_DOMAIN.get(skill, "General")
    
    @staticmethod
    def get_skill_hierarchy(skill: str) -> Dict[str, str]:
        """
        Get skill hierarchy (tool → domain).
        
        Returns:
            Dictionary with skill, domain, and category
        """
        domain = SkillExtractor.map_skill_to_domain(skill)
        normalized = skill.replace("_", " ").title()
        
        return {
            "skill": normalized,
            "domain": domain,
            "category": domain
        }
