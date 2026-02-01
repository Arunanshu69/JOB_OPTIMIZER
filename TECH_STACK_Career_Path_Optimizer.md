# 🧱 Technical Stack Documentation  
## Career Path Optimizer  
**Resume-to-Job Matcher & Skill Gap Analyzer**

---

## 1. Frontend Stack (User Interface)

### 1.1 Core Technologies
- **Framework:** Next.js (React)
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **UI Components:** Shadcn/UI or Radix UI

**Rationale**
- Rapid development and iteration
- Clean, scalable component architecture
- Industry-standard choice for modern AI dashboards

---

### 1.2 Data Visualization
- **Charts & Graphs:** Recharts
- **Advanced Visuals:** D3.js
- **Skill Heatmaps:** Custom D3.js grid or radial heatmap

**Rationale**
- Skill gaps are best understood visually
- Enables interactive, explainable analytics

---

### 1.3 Motion & UX Enhancements
- **Animations:** Framer Motion
- **Icons:** Lucide Icons

**Guideline**
Animations must enhance understanding, not distract.

---

## 2. Backend Stack (Application Core)

### 2.1 API Layer
- **Framework:** FastAPI
- **Language:** Python

**Rationale**
- High performance with async support
- Seamless integration with ML and LLM pipelines
- Automatic OpenAPI documentation

---

### 2.2 Resume Processing
- **PDF Parsing:** PyMuPDF / pdfplumber
- **DOCX Parsing:** python-docx

**Purpose**
- Accurate extraction of unstructured resume content
- Robust handling of real-world resume formats

---

## 3. AI / ML Stack (Semantic Intelligence)

### 3.1 Embeddings & Semantic Matching
- **Baseline Model:** Word2Vec (Gensim)
- **Primary Model:** Sentence-BERT
- **Similarity Metric:** Cosine Similarity

**Purpose**
- Map resumes and job descriptions into a shared semantic vector space
- Capture contextual meaning beyond keyword overlap

---

### 3.2 Skill Ontology & Mapping
- **Approach:** Hybrid rule-based + embedding similarity
- **Optional Enhancement:** Knowledge Graph using Neo4j

**Example Mapping**
```
PyTorch → Deep Learning → Machine Learning → Artificial Intelligence
```

---

### 3.3 LLM Layer (AI Career Counsellor)
- **Model Class:** GPT-class LLM or open-source equivalent
- **Framework:** LangChain

**Responsibilities**
- Explain skill gaps in natural language
- Justify course and roadmap recommendations
- Generate personalized 6-month learning plans

---

## 4. Recommendation Engine (ROI Optimization)

### 4.1 Recommendation Logic
- **Type:** Hybrid (Rule-based + Score-weighted)

### 4.2 Input Signals
- Job role relevance
- Skill gap severity
- Time-to-skill acquisition
- Market demand weight

### 4.3 Output
- Ranked NPTEL and Coursera certifications
- Transparent reasoning for each recommendation

---

## 5. Database & Storage Layer

### 5.1 Primary Database
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy

**Stores**
- User profiles
- Skill vectors
- Job descriptions
- Learning roadmaps

---

### 5.2 Vector Database
- **Option 1:** FAISS (local, hackathon-friendly)
- **Option 2:** Pinecone / Weaviate (cloud-scale)

**Purpose**
- High-speed similarity search
- Efficient resume-to-job matching

---

## 6. Market Demand Intelligence

### 6.1 Data Sources
- Periodic scraping of job portals
- Curated skill-demand datasets

### 6.2 Processing Stack
- Pandas
- NumPy

**Outputs**
- Skill frequency scores
- Role-skill demand matrices

---

## 7. Authentication & Security

- **Authentication:** JWT-based auth
- **Encryption:** AES for sensitive resume data

**Principle**
User data privacy is non-negotiable.

---

## 8. DevOps & Deployment

### 8.1 Containerization
- Docker (frontend and backend services)

### 8.2 Deployment Targets
- **Frontend:** Vercel
- **Backend:** AWS EC2 / Render

### 8.3 CI/CD
- GitHub Actions (optional)

---

## 9. Observability & Quality Assurance

- **Logging:** Loguru
- **Error Tracking:** Sentry
- **API Testing:** Postman

Ensures system robustness and production readiness.

---

## 10. End-to-End System Flow

```
Resume Upload
   ↓
Text Extraction
   ↓
Skill Extraction + Embedding Generation
   ↓
Semantic Matching (Resume ↔ Job Description)
   ↓
Skill Gap Analysis (Market-weighted)
   ↓
Skill Heatmap & Match Score Visualization
   ↓
AI Career Counsellor
   ↓
6-Month Learning Roadmap + Course ROI Recommendations
```

---

## 11. Why This Tech Stack Works

- Balances modern tools with stability
- Explainable and interpretable AI pipeline
- Scales from hackathon prototype to real-world deployment
- Every component serves a clear functional purpose

---

## 12. Future Stack Enhancements

- Full knowledge graph integration
- Real-time labor market APIs
- Model fine-tuning for domain-specific roles
- Recruiter-facing analytics dashboards
