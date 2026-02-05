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
        "sql": ["sql", "mysql", "postgresql", "postgres", "sqlite"],
        "bash": ["bash", "shell scripting", "shell script"],
        "linux": ["linux", "unix"],
        
        # Web Technologies
        "react": ["react", "reactjs", "react.js"],
        "angular": ["angular", "angularjs"],
        "vue": ["vue", "vuejs", "vue.js"],
        "html": ["html", "html5"],
        "css": ["css", "css3", "scss", "sass"],
        "tailwind": ["tailwind", "tailwindcss", "tailwind css"],
        "bootstrap": ["bootstrap"],
        "material_ui": ["material ui", "mui"],
        "django": ["django", "django framework"],
        "flask": ["flask", "flask framework"],
        "fastapi": ["fastapi", "fast api"],
        "express": ["express", "expressjs", "express.js"],
        "nestjs": ["nestjs", "nest.js", "nest js"],
        "nextjs": ["next.js", "nextjs", "next"],
        "nodejs": ["node.js", "nodejs", "node"],
        "rest_api": ["rest", "restful", "rest api"],
        "graphql": ["graphql", "graph ql"],
        
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
        "excel": ["excel", "ms excel", "microsoft excel"],
        
        # Cloud & DevOps
        "aws": ["aws", "amazon web services"],
        "azure": ["azure", "microsoft azure"],
        "gcp": ["gcp", "google cloud", "google cloud platform"],
        "docker": ["docker", "containerization"],
        "kubernetes": ["kubernetes", "k8s"],
        "jenkins": ["jenkins"],
        "ci_cd": ["ci/cd", "cicd", "continuous integration", "continuous delivery"],
        "terraform": ["terraform"],
        "ansible": ["ansible"],
        
        # Databases
        "mongodb": ["mongodb", "mongo"],
        "redis": ["redis"],
        "elasticsearch": ["elasticsearch", "elastic"],
        "cassandra": ["cassandra"],
        "dynamodb": ["dynamodb"],
        "firebase": ["firebase", "firestore"],
        
        # Other Skills
        "git": ["git", "github", "gitlab", "version control"],
        "agile": ["agile", "scrum", "kanban"],
        "microservices": ["microservices", "microservice architecture"],
        "testing": ["unit testing", "integration testing", "testing", "tdd"],
        "pytest": ["pytest"],
        "jest": ["jest"],
        "redux": ["redux", "redux toolkit", "rtk"],
        "vite": ["vite"],
        "webpack": ["webpack"],
        "oauth": ["oauth", "oauth2"],
        "jwt": ["jwt", "json web token"],
        "oop": ["object oriented", "oop"],
        "data_structures": ["data structures"],
        "algorithms": ["algorithms", "algorithmic"],
    }

    ROLE_SKILL_MAP = {
        "software engineer": [
            "python", "javascript", "typescript", "java", "sql",
            "git", "rest_api", "testing", "data_structures", "algorithms"
        ],
        "full stack": [
            "javascript", "typescript", "react", "nodejs", "express",
            "sql", "mongodb", "rest_api", "git", "docker"
        ],
        "frontend": [
            "javascript", "typescript", "react", "html", "css",
            "tailwind", "redux", "vite", "git"
        ],
        "backend": [
            "python", "java", "nodejs", "fastapi", "django",
            "sql", "redis", "rest_api", "docker", "git"
        ],
        "data scientist": [
            "python", "pandas", "numpy", "scikit_learn",
            "machine_learning", "sql", "matplotlib"
        ],
        "data analyst": [
            "sql", "python", "pandas", "excel", "tableau", "power_bi"
        ],
        "machine learning engineer": [
            "python", "pytorch", "tensorflow", "machine_learning",
            "deep_learning", "docker", "aws"
        ],
        "devops": [
            "docker", "kubernetes", "aws", "linux", "ci_cd", "terraform"
        ],
        "cloud engineer": [
            "aws", "azure", "gcp", "docker", "linux", "terraform"
        ],
        "mobile": [
            "javascript", "typescript", "react", "git"
        ],
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
                if SkillExtractor._pattern_in_text(pattern, text_lower):
                    found_skills.add(normalized_skill)
                    break
        
        return sorted(list(found_skills))

    @staticmethod
    def infer_skills_from_role(text: str) -> List[str]:
        """Infer likely skills based on role keywords in text."""
        text_lower = text.lower()
        inferred = set()
        for role_key, skills in SkillExtractor.ROLE_SKILL_MAP.items():
            if role_key in text_lower:
                inferred.update(skills)
        return sorted(list(inferred))

    @staticmethod
    def _pattern_in_text(pattern: str, text_lower: str) -> bool:
        """
        Match patterns with safer boundaries than \\b so tokens like c++ work.
        """
        escaped = re.escape(pattern)
        regex = r'(?<![a-z0-9])' + escaped + r'(?![a-z0-9])'
        return re.search(regex, text_lower) is not None
    
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
