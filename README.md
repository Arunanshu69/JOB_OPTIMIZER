# Career Path Optimizer

> AI-powered Resume-to-Job Matcher & Skill Gap Analyzer

[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688.svg)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-14-black)](https://nextjs.org/)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 🎯 Overview

Career Path Optimizer transforms career guidance from keyword-driven guesswork into data-backed, AI-powered intelligence. It uses semantic understanding, LLMs, and machine learning to:

- **Semantic Resume-Job Matching**: Goes beyond keywords to understand true capabilities
- **Skill Gap Analysis**: Identifies missing skills aligned with real-world job demands
- **Personalized Learning Roadmap**: Generates a 6-month actionable plan
- **Interactive Skill Heatmap**: Visualizes strengths and gaps at a glance
- **AI Career Counsellor**: Provides continuous guidance and explanations

## 🏗️ Architecture

```
┌─────────────────┐         ┌──────────────────┐
│   Frontend      │◄────────┤   Backend API    │
│   (Next.js)     │  REST   │   (FastAPI)      │
└─────────────────┘         └──────────────────┘
                                     │
                    ┌────────────────┼────────────────┐
                    │                │                │
              ┌──────▼──────┐ ┌─────▼─────┐  ┌──────▼──────┐
              │  Resume      │ │  Semantic  │  │  Skill Gap  │
              │  Parser      │ │  Matching  │  │  Analyzer   │
              └──────────────┘ └───────────┘  └─────────────┘
                                     │
                              ┌──────▼──────┐
                              │  Vector DB  │
                              │   (FAISS)   │
                              └─────────────┘
```

## ✨ Features

### Core Functionality
- ✅ PDF/DOCX resume parsing with multiple extraction methods
- ✅ Semantic skill extraction and normalization
- ✅ Sentence-BERT embeddings for semantic similarity
- ✅ Cosine similarity-based matching
- ✅ Comprehensive skill gap analysis
- ✅ Interactive skill heatmap data generation
- ✅ 6-month learning roadmap generation
- ✅ Course recommendations (NPTEL, Coursera)

### Technical Highlights
- 🚀 High-performance FastAPI backend
- 🎨 Modern Next.js frontend (to be implemented)
- 🤖 Sentence-Transformers for embeddings
- 🔍 FAISS vector database for efficient similarity search
- 🔐 JWT-based authentication
- 📊 RESTful API with automatic OpenAPI documentation

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.9+
- **ML/NLP**: Sentence-Transformers, Gensim, Scikit-learn
- **Resume Parsing**: PyMuPDF, pdfplumber, python-docx
- **Vector DB**: FAISS
- **LLM Integration**: LangChain, OpenAI
- **Database**: PostgreSQL (with SQLAlchemy ORM)
- **Authentication**: JWT (python-jose)

### Frontend (In Progress)
- **Framework**: Next.js 14 with TypeScript
- **Styling**: Tailwind CSS
- **UI Components**: Shadcn/UI
- **Visualizations**: Recharts, D3.js
- **Animations**: Framer Motion

## 📦 Installation

### Prerequisites
- Python 3.9+
- Node.js 18+ (for frontend)
- PostgreSQL (optional, can use SQLite for dev)

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Run the server
python -m app.main
```

The API will be available at `http://localhost:8000`
- API Documentation: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Frontend Setup (Coming Soon)

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

## 🚀 Quick Start

### 1. Upload Resume
```bash
curl -X POST "http://localhost:8000/api/resume/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@resume.pdf"
```

### 2. Analyze Job Description
```bash
curl -X POST "http://localhost:8000/api/job/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Machine Learning Engineer",
    "description": "Looking for ML engineer with Python, TensorFlow, PyTorch..."
  }'
```

### 3. Calculate Match Score
```bash
curl -X POST "http://localhost:8000/api/match/calculate" \
  -H "Content-Type: application/json" \
  -d '{
    "resume_text": "...",
    "job_description": "...",
    "job_title": "ML Engineer"
  }'
```

### 4. Generate Learning Roadmap
```bash
curl -X POST "http://localhost:8000/api/roadmap/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "missing_skills": ["PyTorch", "Deep Learning", "Docker"],
    "target_role": "ML Engineer"
  }'
```

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Root endpoint |
| `/health` | GET | Health check |
| `/api/resume/upload` | POST | Upload and parse resume |
| `/api/job/analyze` | POST | Analyze job description |
| `/api/match/calculate` | POST | Calculate match score |
| `/api/roadmap/generate` | POST | Generate learning roadmap |

Full API documentation available at `/docs` when server is running.

## 🧪 Testing

```bash
# Run tests
cd backend
pytest

# With coverage
pytest --cov=app tests/
```

## 📁 Project Structure

```
webapp/
├── backend/
│   ├── app/
│   │   ├── api/          # API endpoints
│   │   ├── core/         # Configuration, database, security
│   │   ├── models/       # Database models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── services/     # Business logic
│   │   │   ├── resume_parser.py
│   │   │   ├── skill_extractor.py
│   │   │   ├── embedding_service.py
│   │   │   └── skill_gap_service.py
│   │   └── main.py       # FastAPI application
│   ├── tests/
│   ├── requirements.txt
│   └── .env.example
├── frontend/             # Next.js frontend (to be implemented)
├── PRD_Career_Path_Optimizer.md
├── DESIGN_Career_Path_Optimizer.md
├── TECH_STACK_Career_Path_Optimizer.md
├── todo.md
└── README.md
```

## 🎨 Design Philosophy

- **Clarity**: Make AI intelligence visible, not intimidating
- **Trust**: Explainability-first UI
- **Actionability**: Convert insights into execution
- **Progressive Disclosure**: Avoid overwhelming users

## 🔐 Security

- JWT-based authentication
- AES encryption for sensitive resume data
- GDPR-compliant data handling
- No third-party data sharing
- Secure file upload validation

## 📈 Performance

- Resume processing < 5 seconds
- Embedding generation with caching
- Efficient vector similarity search with FAISS
- Optimized database queries

## 🗺️ Roadmap

### Current Phase: MVP Development
- [x] Backend API structure
- [x] Resume parsing (PDF/DOCX)
- [x] Skill extraction and normalization
- [x] Semantic matching engine
- [x] Skill gap analysis
- [x] Basic roadmap generation
- [ ] Frontend implementation
- [ ] LLM integration for AI Career Counsellor
- [ ] Database persistence
- [ ] Authentication system

### Future Enhancements
- Knowledge Graph integration (Neo4j)
- Real-time labor market APIs
- ATS compatibility scoring
- Mock interview question generator
- Career trajectory simulation
- Recruiter-facing dashboard
- Multi-language support
- Mobile app

## 🤝 Contributing

Contributions are welcome! Please read our contributing guidelines before submitting PRs.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Team

Built with ❤️ by the Career Path Optimizer team

## 📞 Support

For questions or issues:
- Open an issue on GitHub
- Email: support@careerpathoptimizer.com

---

**Made with AI-powered intelligence for the future of career guidance**
