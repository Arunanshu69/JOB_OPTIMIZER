# 🚀 Deployment Guide - Career Path Optimizer

This guide covers deploying both the backend (FastAPI) and frontend (Next.js) components of the Career Path Optimizer.

## Table of Contents
1. [Local Development Setup](#local-development-setup)
2. [Backend Deployment](#backend-deployment)
3. [Frontend Deployment](#frontend-deployment)
4. [Environment Variables](#environment-variables)
5. [Testing the Deployment](#testing-the-deployment)

---

## Local Development Setup

### Backend

1. **Navigate to backend directory**:
```bash
cd backend
```

2. **Create and activate virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Create .env file**:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Run the backend server**:
```bash
python -m app.main
```

The API will be available at `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/health`

### Frontend

1. **Navigate to frontend directory**:
```bash
cd frontend
```

2. **Install dependencies**:
```bash
npm install
```

3. **Create .env.local file**:
```bash
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
```

4. **Run the development server**:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

---

## Backend Deployment

### Option 1: Render (Recommended)

1. **Create a new Web Service on Render**
2. **Connect your GitHub repository**
3. **Configure the service**:
   - **Name**: career-path-optimizer-api
   - **Environment**: Python 3
   - **Build Command**: `cd backend && pip install -r requirements.txt`
   - **Start Command**: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Region**: Choose closest to your users

4. **Add Environment Variables** (in Render dashboard):
   ```
   DATABASE_URL=your-postgresql-connection-string
   SECRET_KEY=your-secret-key-here
   OPENAI_API_KEY=your-openai-api-key
   ALLOWED_ORIGINS=https://your-frontend-domain.com
   ```

5. **Deploy**: Click "Create Web Service"

### Option 2: AWS EC2

1. **Launch EC2 Instance**:
   - AMI: Ubuntu 22.04 LTS
   - Instance Type: t3.medium (minimum)
   - Security Group: Allow ports 22 (SSH) and 8000

2. **SSH into the instance**:
```bash
ssh -i your-key.pem ubuntu@your-ec2-ip
```

3. **Install dependencies**:
```bash
sudo apt update
sudo apt install python3-pip python3-venv nginx -y
```

4. **Clone repository**:
```bash
git clone your-repo-url
cd career-path-optimizer/backend
```

5. **Set up virtual environment and install**:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

6. **Create .env file**:
```bash
cp .env.example .env
nano .env  # Edit with your settings
```

7. **Set up systemd service**:
```bash
sudo nano /etc/systemd/system/career-optimizer.service
```

Add:
```ini
[Unit]
Description=Career Path Optimizer API
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/career-path-optimizer/backend
Environment="PATH=/home/ubuntu/career-path-optimizer/backend/venv/bin"
ExecStart=/home/ubuntu/career-path-optimizer/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000

[Install]
WantedBy=multi-user.target
```

8. **Start the service**:
```bash
sudo systemctl daemon-reload
sudo systemctl start career-optimizer
sudo systemctl enable career-optimizer
sudo systemctl status career-optimizer
```

9. **Configure Nginx as reverse proxy**:
```bash
sudo nano /etc/nginx/sites-available/career-optimizer
```

Add:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Enable and restart:
```bash
sudo ln -s /etc/nginx/sites-available/career-optimizer /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## Frontend Deployment

### Option 1: Vercel (Recommended)

1. **Install Vercel CLI**:
```bash
npm install -g vercel
```

2. **Navigate to frontend directory**:
```bash
cd frontend
```

3. **Deploy**:
```bash
vercel
```

4. **Set environment variables** in Vercel dashboard:
   ```
   NEXT_PUBLIC_API_URL=https://your-backend-url.com
   ```

5. **For production deployment**:
```bash
vercel --prod
```

### Option 2: Netlify

1. **Install Netlify CLI**:
```bash
npm install -g netlify-cli
```

2. **Navigate to frontend directory and build**:
```bash
cd frontend
npm run build
```

3. **Deploy**:
```bash
netlify deploy --prod
```

4. **Set environment variables** in Netlify dashboard:
   - Go to Site settings → Build & deploy → Environment
   - Add: `NEXT_PUBLIC_API_URL=https://your-backend-url.com`

---

## Environment Variables

### Backend (.env)

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/career_optimizer

# Security
SECRET_KEY=your-very-secure-secret-key-change-this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
ALLOWED_ORIGINS=https://your-frontend-domain.com,http://localhost:3000

# OpenAI (for future LLM features)
OPENAI_API_KEY=sk-your-openai-api-key

# Application
DEBUG=False
MAX_UPLOAD_SIZE=10485760

# Models
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

### Frontend (.env.local)

```bash
NEXT_PUBLIC_API_URL=https://your-backend-api-url.com
```

---

## Testing the Deployment

### 1. Test Backend API

```bash
# Health check
curl https://your-backend-url.com/health

# Expected response:
# {"status": "healthy"}
```

### 2. Test Resume Upload

```bash
curl -X POST "https://your-backend-url.com/api/resume/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@test-resume.pdf"
```

### 3. Test Frontend

1. Open `https://your-frontend-url.com` in browser
2. Upload a test resume
3. Paste a job description
4. Click "Analyze Match"
5. Verify match results appear
6. Click "Generate Learning Roadmap"
7. Verify roadmap appears

---

## Docker Deployment (Advanced)

### Backend Dockerfile

Create `backend/Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Frontend Dockerfile

Create `frontend/Dockerfile`:

```dockerfile
FROM node:18-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM node:18-alpine AS runner

WORKDIR /app

COPY --from=builder /app/next.config.js ./
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json

EXPOSE 3000

CMD ["npm", "start"]
```

### Docker Compose

Create `docker-compose.yml` in project root:

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/career_optimizer
      - SECRET_KEY=${SECRET_KEY}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    depends_on:
      - db

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000
    depends_on:
      - backend

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=career_optimizer
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

**Run with Docker Compose**:
```bash
docker-compose up -d
```

---

## Monitoring & Maintenance

### Health Checks

Set up automated health checks:

```bash
# Backend health check
*/5 * * * * curl -f https://your-backend-url.com/health || echo "Backend down"

# Frontend health check
*/5 * * * * curl -f https://your-frontend-url.com || echo "Frontend down"
```

### Logs

**Backend logs (systemd)**:
```bash
sudo journalctl -u career-optimizer -f
```

**Render logs**: Available in Render dashboard

**Vercel logs**: Available in Vercel dashboard

### Updates

To update the deployment:

1. **Pull latest changes**:
```bash
git pull origin main
```

2. **Backend** (if using systemd):
```bash
sudo systemctl restart career-optimizer
```

3. **Frontend** (Vercel):
```bash
vercel --prod
```

---

## Troubleshooting

### Backend Issues

**Import errors**:
```bash
# Ensure virtual environment is activated
source venv/bin/activate
pip install -r requirements.txt
```

**Port already in use**:
```bash
# Find and kill process
lsof -i :8000
kill -9 <PID>
```

### Frontend Issues

**Build failures**:
```bash
# Clear cache and rebuild
rm -rf .next node_modules
npm install
npm run build
```

**API connection issues**:
- Check `NEXT_PUBLIC_API_URL` in environment variables
- Ensure CORS is configured on backend

---

## Security Checklist

- [ ] Change default SECRET_KEY
- [ ] Use strong database passwords
- [ ] Enable HTTPS (use Certbot for Let's Encrypt)
- [ ] Set up firewall rules
- [ ] Regular security updates
- [ ] Implement rate limiting
- [ ] Set up backup systems
- [ ] Monitor logs for suspicious activity

---

## Support

For deployment issues:
1. Check logs first
2. Review environment variables
3. Test API endpoints individually
4. Check CORS configuration
5. Open an issue on GitHub

---

**Last Updated**: 2026-02-01
