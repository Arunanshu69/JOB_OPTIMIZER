# 📄 Product Requirements Document (PRD)
## Resume-to-Job Matcher & Skill Gap Analyzer

**PS ID:** HY26-02  
**Type:** Software (SW)  
**Domain:** GenAI, LLMs, Career Intelligence  

---

## 1. Overview

### 1.1 Product Name
**Career Path Optimizer**  
(Resume-to-Job Matcher & Skill Gap Analyzer)

### 1.2 Problem Statement
Traditional recruitment and career guidance platforms rely heavily on **keyword-based matching (RegEx)**, which fails to capture the semantic meaning of skills and experiences. This results in:

- Underestimation of a candidate’s true capabilities  
- Poor job-fit recommendations  
- Generic upskilling advice with low career ROI  

For example, a student proficient in **PyTorch** may possess strong **Deep Learning** skills, yet be filtered out if the exact keyword is missing from their resume.

### 1.3 Solution Summary
The Career Path Optimizer leverages **Large Language Models (LLMs)**, **semantic embeddings**, and optionally **Knowledge Graphs** to:

- Perform **semantic resume-to-job matching**
- Identify **missing skill blocks** aligned with real-world job demands
- Generate a **personalized 6-month learning roadmap**
- Visualize strengths and gaps using an **interactive skill heatmap**
- Act as an **AI Career Counsellor** for continuous guidance

---

## 2. Goals & Objectives

### 2.1 Primary Goals
- Accurately assess candidate-job fit using **semantic understanding**
- Bridge skill gaps with **high-ROI learning recommendations**
- Provide actionable, time-bound career guidance

### 2.2 Success Metrics (KPIs)
- Resume–JD similarity score accuracy
- Reduction in false skill mismatches
- User engagement with learning roadmap
- Completion rate of recommended certifications
- User satisfaction score (career relevance)

---

## 3. Target Users

### 3.1 Primary Users
- College students
- Early-career professionals
- Career switchers

### 3.2 Secondary Users
- Career counsellors
- Training & placement cells
- EdTech platforms

---

## 4. User Personas

### Persona 1: Final-Year Student
- Has project-based skills but weak resume keywords
- Wants role-specific preparation (e.g., ML Engineer)

### Persona 2: Career Switcher
- Strong transferable skills
- Needs structured learning roadmap and validation

---

## 5. User Journey

1. Upload Resume (PDF/DOCX)
2. Select Target Job Role or Paste Job Description
3. System performs semantic analysis
4. Skill extraction & normalization
5. Skill gap detection vs market demand
6. Visualization via Skill Heatmap
7. AI Career Counsellor generates roadmap
8. Certification & course recommendations

---

## 6. Functional Requirements

### 6.1 Resume Ingestion
- Support PDF and DOCX formats
- Extract text reliably
- Handle unstructured layouts

### 6.2 Skill Extraction & Normalization
- Identify explicit and implicit skills
- Map tools → domains  
  Example:
  - PyTorch → Deep Learning  
  - NumPy → Numerical Computing  

### 6.3 Semantic Matching Engine
- Convert resumes and JDs into embeddings
- Compute cosine similarity
- Rank job-fit relevance score

### 6.4 Skill Gap Analysis
- Compare extracted skills with:
  - Job Description requirements
  - Live market demand dataset
- Identify:
  - Missing skills
  - Weak skill areas
  - Future-proof skills

### 6.5 Personalization Engine
- Recommend:
  - NPTEL courses
  - Coursera certifications
- Rank recommendations based on:
  - Job relevance
  - Time-to-skill
  - Career ROI

### 6.6 AI Career Counsellor
- Conversational interface
- Explains:
  - Why skills are missing
  - Why certain courses are suggested
- Generates a **6-month learning roadmap**

### 6.7 Skill Heatmap Visualization
- Interactive UI
- Color-coded skill strength levels
- Drill-down per skill

---

## 7. Non-Functional Requirements

### 7.1 Performance
- Resume processing < 5 seconds
- Embedding generation optimized with caching

### 7.2 Scalability
- Support concurrent users
- Modular architecture for model upgrades

### 7.3 Security & Privacy
- Resume data encrypted at rest
- No third-party data sharing
- GDPR-compliant data handling

### 7.4 Explainability
- Transparent reasoning for recommendations
- Human-readable explanations

---

## 8. Technical Architecture

### 8.1 Core Components

| Component | Description |
|---------|------------|
| Resume Parser | Extracts clean text |
| Embedding Engine | Word2Vec / BERT-based embeddings |
| Semantic Matcher | Similarity scoring |
| Knowledge Graph (Optional) | Skill relationships |
| Recommendation Engine | ROI-based suggestions |
| Visualization Layer | Skill Heatmap |
| LLM Layer | Career counsellor |

---

## 9. Technical Challenges & Approach

### 9.1 Contextual Embedding
- Use Word2Vec for baseline
- BERT or Sentence-BERT for deep semantic similarity
- High-dimensional vector mapping

### 9.2 Skill Ontology Mapping
- Tool → Skill → Domain hierarchy
- Expand via Knowledge Graphs

### 9.3 Live Market Demand Integration
- Periodic scraping or API-based role skill data
- Skill frequency normalization

---

## 10. Assumptions & Constraints

### Assumptions
- Resume text is extractable
- Job descriptions are available
- Course platforms expose metadata

### Constraints
- Limited compute for fine-tuning
- Cold-start problem for new roles

---

## 11. Risks & Mitigations

| Risk | Mitigation |
|----|------------|
| Hallucinated skill inference | Confidence scoring |
| Over-recommendation | ROI thresholding |
| Bias in data | Dataset diversification |

---

## 12. Expected Outcomes
- Accurate semantic resume–job matching
- Clear visualization of skill gaps
- Personalized, actionable 6-month roadmap
- Improved employability alignment with market needs

---

## 13. Future Enhancements
- ATS compatibility scoring
- Mock interview question generator
- Career trajectory simulation
- Recruiter-facing dashboard

---

## 14. Conclusion
The **Career Path Optimizer** transforms career guidance from **keyword-driven guesswork** into **data-backed, AI-powered intelligence**, enabling users to understand not just *where they stand*, but *exactly what to do next*.
