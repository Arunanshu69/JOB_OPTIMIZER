import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Resume API
export const uploadResume = async (file: File) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await api.post('/api/resume/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  
  return response.data;
};

// Job Description API
export const analyzeJobDescription = async (title: string, description: string) => {
  const response = await api.post('/api/job/analyze', {
    title,
    description,
  });
  
  return response.data;
};

// Match Calculation API
export const calculateMatch = async (
  resumeText: string,
  jobDescription: string,
  jobTitle: string = 'Target Role'
) => {
  const response = await api.post('/api/match/calculate', {
    resume_text: resumeText,
    job_description: jobDescription,
    job_title: jobTitle,
  });
  
  return response.data;
};

// Roadmap Generation API
export const generateRoadmap = async (
  missingSkills: string[],
  targetRole: string = 'Your Target Role',
  currentSkills: string[] = []
) => {
  const response = await api.post('/api/roadmap/generate', {
    missing_skills: missingSkills,
    target_role: targetRole,
    current_skills: currentSkills,
  });
  
  return response.data;
};

export const getAlternativeCareers = async (
  skills: string[],
  currentRole: string = '',
  topK: number = 5
) => {
  const response = await api.post('/api/career/alternatives', {
    skills,
    current_role: currentRole || undefined,
    top_k: topK,
  });

  return response.data;
};
