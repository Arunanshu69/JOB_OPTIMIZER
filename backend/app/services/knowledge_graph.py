import json
import os
from typing import Dict, List, Optional

from app.services.skill_extractor import SkillExtractor

GRAPH_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "knowledge_graph.json")


def _canonicalize(value: str) -> str:
    lowered = value.strip().lower()
    cleaned = []
    for ch in lowered:
        if ch.isalnum():
            cleaned.append(ch)
        else:
            cleaned.append(" ")
    normalized = " ".join("".join(cleaned).split())
    return normalized.replace(" ", "_")


class KnowledgeGraph:
    def __init__(self, data: Dict[str, object]):
        self.skills = set(data.get("skills", []))
        self.roles = data.get("roles", {})
        self.courses = data.get("courses", [])
        self.prereqs = data.get("prereqs", {})

    @classmethod
    def load(cls) -> "KnowledgeGraph":
        with open(GRAPH_PATH, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        return cls(data)

    @staticmethod
    def normalize_skill_display(skills: List[str]) -> List[str]:
        return SkillExtractor.normalize_skills(skills)

    @staticmethod
    def canonicalize_skills(skills: List[str]) -> List[str]:
        return sorted({_canonicalize(skill) for skill in skills if skill})

    def find_role_key(self, role_text: str) -> Optional[str]:
        if not role_text:
            return None
        key = _canonicalize(role_text)
        if key in self.roles:
            return key
        for role_key in self.roles.keys():
            if role_key in key or key in role_key:
                return role_key
        return None

    def get_role_skills(self, role_text: str) -> List[str]:
        role_key = self.find_role_key(role_text)
        if not role_key:
            return []
        return self.roles.get(role_key, [])

    def order_skills_with_prereqs(self, skills: List[str]) -> List[str]:
        skills_set = set(skills)
        ordered = []
        visiting = set()
        visited = set()

        def visit(skill: str) -> None:
            if skill in visited:
                return
            if skill in visiting:
                return
            visiting.add(skill)
            for prereq in self.prereqs.get(skill, []):
                if prereq in skills_set:
                    visit(prereq)
            visiting.remove(skill)
            visited.add(skill)
            ordered.append(skill)

        for skill in skills:
            visit(skill)
        return ordered

    def recommend_courses(self, skills: List[str], limit: int = 5) -> List[Dict[str, object]]:
        skills_set = set(skills)
        scored = []
        for course in self.courses:
            course_skills = set(course.get("skills", []))
            overlap = skills_set.intersection(course_skills)
            if not overlap:
                continue
            score = len(overlap) / max(len(course_skills), 1)
            scored.append((score, course, overlap))
        scored.sort(key=lambda item: item[0], reverse=True)
        results = []
        for score, course, overlap in scored[:limit]:
            results.append({
                "skill": ", ".join(self.normalize_skill_display(sorted(overlap))),
                "platform": "Curated",
                "course_name": course.get("name", "Course"),
                "duration": "4-6 weeks",
                "roi_score": int(round(score * 100)),
                "relevance": "High" if score >= 0.6 else "Medium"
            })
        return results

    def suggest_alternative_roles(
        self,
        skills: List[str],
        current_role: Optional[str] = None,
        top_k: int = 5
    ) -> List[Dict[str, object]]:
        skill_set = set(skills)
        suggestions = []
        excluded = _canonicalize(current_role) if current_role else None
        for role_key, role_skills in self.roles.items():
            if excluded and excluded == role_key:
                continue
            role_skill_set = set(role_skills)
            if not role_skill_set:
                continue
            matched = sorted(list(role_skill_set.intersection(skill_set)))
            missing = sorted(list(role_skill_set.difference(skill_set)))
            match_pct = round((len(matched) / len(role_skill_set)) * 100, 2)
            suggestions.append({
                "role": role_key.replace("_", " ").title(),
                "match_percentage": match_pct,
                "matched_skills": self.normalize_skill_display(matched),
                "missing_skills": self.normalize_skill_display(missing),
                "reason": f"Matches {len(matched)} of {len(role_skill_set)} core skills."
            })
        suggestions.sort(key=lambda s: s["match_percentage"], reverse=True)
        return suggestions[:top_k]


def get_graph() -> KnowledgeGraph:
    return KnowledgeGraph.load()
