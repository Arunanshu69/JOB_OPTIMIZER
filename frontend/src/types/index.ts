export interface ResumeData {
  filename: string;
  extracted_text: string;
  skills: string[];
  skill_count: number;
  file_path: string;
}

export interface JobDescriptionData {
  title: string;
  skills_required: string[];
  skill_count: number;
}

export interface SkillBreakdown {
  resume_skills: string[];
  required_skills: string[];
  matched_skills: string[];
  missing_skills: string[];
  additional_skills: string[];
}

export interface SkillBreakdownRaw {
  resume_skills: string[];
  required_skills: string[];
  matched_skills: string[];
  missing_skills: string[];
  additional_skills: string[];
}

export interface HeatmapSkill {
  skill: string;
  strength: 'high' | 'medium' | 'low' | 'missing';
  level: number;
  color: string;
  in_resume: boolean;
  in_job_requirement: boolean;
  domain: string;
}

export interface MatchData {
  success: boolean;
  match_score: number;
  semantic_similarity: number;
  skill_match_percentage: number;
  job_title?: string;
  skill_breakdown: SkillBreakdown;
  skill_breakdown_raw?: SkillBreakdownRaw;
  heatmap_data: HeatmapSkill[];
  explanation: string;
}

export interface RoadmapMilestone {
  month: number;
  title: string;
  skills: string[];
  focus_areas: string[];
  estimated_hours: number;
}

export interface CourseRecommendation {
  skill: string;
  platform: string;
  course_name: string;
  duration: string;
  roi_score: number;
  relevance: string;
}

export interface RoadmapData {
  target_role: string;
  duration_months: number;
  milestones: RoadmapMilestone[];
}

export interface AlternativeCareer {
  role: string;
  match_percentage: number;
  matched_skills: string[];
  missing_skills: string[];
  reason: string;
}

export interface CertificationRecommendation {
  name: string;
  provider: string;
  duration: string;
  cost: string;
  roi_score: number;
  skills: string[];
  reason: string;
}
