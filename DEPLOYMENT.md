# Deployment Guide: Railway + Vercel

**Backend:** Railway (FastAPI)
**Frontend:** Vercel (Next.js/React - to be added)

---

## Phase 1: Deploy Backend to Railway

### Prerequisites
1. **Railway Account:** Sign up at [railway.app](https://railway.app)
2. **Git Repository:** Push code to GitHub (Railway connects to GitHub)
3. **Environment Variables:** OpenAI API key, Neo4j credentials

---

### Step 1: Create Railway Project

1. Go to [railway.app](https://railway.app) and log in
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Select your `entertainment-graph` repository
5. Railway will auto-detect Python and use the config files we created

---

### Step 2: Configure Environment Variables

In Railway project settings, add these environment variables:

```
OPENAI_API_KEY=your_openai_key
NEO4J_URI=neo4j+s://your_neo4j_instance.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_neo4j_password
LLM_MODEL=gpt-4
ENVIRONMENT=production
```

**Important:** Railway provides these automatically:
- `PORT` - Auto-assigned port (Railway handles this)
- `RAILWAY_ENVIRONMENT` - production/staging

---

### Step 3: Deploy

1. Railway will automatically build and deploy when you push to GitHub
2. Check deployment logs in Railway dashboard
3. Once deployed, Railway provides a public URL: `https://your-app.railway.app`

---

### Step 4: Test the API

```bash
# Health check
curl https://your-app.railway.app/health

# Query Pure Vector system
curl -X POST https://your-app.railway.app/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Denis Villeneuve movies",
    "system": "pure_vector",
    "limit": 5
  }'
```

---

## Phase 2: Deploy Frontend to Vercel (Future)

### When you create a frontend (Next.js/React):

1. Create `/frontend` directory with Next.js app
2. Go to [vercel.com](https://vercel.com) and log in
3. Click "New Project"
4. Import your GitHub repo
5. Vercel auto-detects Next.js
6. Set environment variable:
   ```
   NEXT_PUBLIC_API_URL=https://your-app.railway.app
   ```
7. Deploy

---

## Architecture

```
┌─────────────────┐
│   Vercel        │  Frontend (Next.js)
│   Frontend      │  https://your-app.vercel.app
└────────┬────────┘
         │
         │ HTTP Requests
         ▼
┌─────────────────┐
│   Railway       │  Backend (FastAPI)
│   Backend       │  https://your-app.railway.app
└────────┬────────┘
         │
         ├─── OpenAI API (embeddings, LLM)
         ├─── Neo4j Aura (Graphiti)
         └─── Local storage (ChromaDB, OpenMemory SQLite)
```

---

## Configuration Files Created

### railway.toml
Tells Railway how to build and run your FastAPI app:
- Build: Install Python dependencies from `requirements.txt`
- Deploy: Run uvicorn server on Railway's assigned port

### Procfile
Alternative config format (Railway supports both):
- Specifies the web process command

### requirements.txt
Root-level dependency file that Railway uses for installation

---

## Deployment Checklist

### Backend (Railway) ✅
- [x] Create [railway.toml](railway.toml)
- [x] Create [Procfile](Procfile)
- [x] Create [requirements.txt](requirements.txt)
- [ ] Push code to GitHub
- [ ] Connect Railway to GitHub repo
- [ ] Set environment variables in Railway
- [ ] Deploy and test

### Frontend (Vercel) ⏳
- [ ] Create Next.js/React frontend
- [ ] Connect Vercel to GitHub repo
- [ ] Set `NEXT_PUBLIC_API_URL` env var
- [ ] Deploy

---

## Cost Estimates

### Railway Backend
- **Free tier:** $5/month credit
- **Usage:** ~$5-10/month for hobby project
  - 512MB RAM
  - Shared CPU
  - No cold starts

### Vercel Frontend
- **Free tier:** Very generous
  - 100GB bandwidth
  - Unlimited deployments
  - Serverless functions (100 hours)

### External Services
- **Neo4j Aura:** Free tier (1 database)
- **OpenAI API:** Pay-per-use (~$0.02-0.10 per request depending on system)

**Total estimated cost:** $5-10/month (mostly Railway)

---

## Scaling Considerations

### When to upgrade Railway:
- If you exceed 512MB RAM (large ChromaDB/OpenMemory databases)
- If you need faster response times (upgrade CPU)
- If you need persistent storage (add Railway volumes)

### Performance optimization:
- Use Railway's built-in Redis for caching
- Add Railway PostgreSQL for structured data
- Enable CORS for frontend access

---

## Next Steps

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "feat: add Railway deployment config"
   git push origin main
   ```

2. **Deploy to Railway:**
   - Visit railway.app
   - Create new project from GitHub
   - Add environment variables
   - Deploy

3. **Test endpoints:**
   - Health check: `/health`
   - Ingest: `POST /ingest`
   - Query: `POST /query`

4. **Build frontend** (Phase 2):
   - Create Next.js app in `/frontend`
   - Connect to Railway backend API
   - Deploy to Vercel

---

## Troubleshooting

### Railway build fails
- Check build logs in Railway dashboard
- Verify `requirements.txt` has all dependencies
- Ensure Python version compatibility (Railway uses Python 3.11+)

### API returns 500 errors
- Check environment variables are set correctly
- Verify Neo4j Aura connection
- Check Railway logs for Python errors

### CORS errors from frontend
- Add CORS middleware in FastAPI ([main.py](python/src/entertainment_graph/main.py))
- Allow your Vercel domain in CORS origins

---

## Support

- **Railway Docs:** https://docs.railway.app
- **Vercel Docs:** https://vercel.com/docs
- **FastAPI Deployment:** https://fastapi.tiangolo.com/deployment/

For project-specific questions, see:
- [README.md](README.md)
- [PROGRESS.md](PROGRESS.md)
- [PHASE1_TASKS.md](PHASE1_TASKS.md)
