# ⚡ Quick Start Guide - Career Path Optimizer

Get the Career Path Optimizer up and running in 5 minutes!

## Prerequisites

- Python 3.9 or higher
- Node.js 18 or higher
- npm or yarn

## 🚀 Quick Setup

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd career-path-optimizer
```

### 2. Start the Backend

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python -m app.main
```

✅ Backend is now running at `http://localhost:8000`
- API Docs: http://localhost:8000/docs

### 3. Start the Frontend (New Terminal)

```bash
# Navigate to frontend from project root
cd frontend

# Install dependencies
npm install

# Create environment file
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Run the dev server
npm run dev
```

✅ Frontend is now running at `http://localhost:3000`

## 🎯 Test the Application

1. Open http://localhost:3000 in your browser
2. Upload a resume (PDF or DOCX)
3. Paste a job description
4. Click "Analyze Match"
5. View your match score and skill gaps
6. Generate a learning roadmap

## 📝 Sample Job Description

Use this sample if you want to test quickly:

```
Machine Learning Engineer

We are looking for an ML Engineer with experience in:
- Python and PyTorch
- Deep Learning and Neural Networks
- Docker and Kubernetes
- FastAPI or Flask
- AWS or GCP
- Git version control

Responsibilities:
- Build and deploy ML models
- Work with large datasets
- Collaborate with data scientists
- Optimize model performance
```

## 🔧 Common Issues

### Backend won't start
- Make sure virtual environment is activated
- Check if port 8000 is available
- Install all dependencies: `pip install -r requirements.txt`

### Frontend won't start
- Delete node_modules and reinstall: `rm -rf node_modules && npm install`
- Check if port 3000 is available
- Ensure .env.local file exists with correct API URL

### Can't upload resume
- Check that backend is running
- Verify API URL in frontend/.env.local
- Check browser console for errors

## 📚 Next Steps

- Read the full [README.md](README.md) for detailed features
- Check [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment
- Review API documentation at http://localhost:8000/docs

## 🆘 Need Help?

- Check the logs in the terminal where the backend is running
- Open browser DevTools (F12) to see frontend errors
- Review the troubleshooting section in DEPLOYMENT.md

---

**Enjoy using Career Path Optimizer! 🚀**
