# Entertainment Graph Frontend

Next.js frontend for comparing retrieval systems (Pure Vector, Graphiti, OpenMemory) side-by-side.

## Architecture

Built according to [specs/frontend.md](../specs/frontend.md)

- **Framework**: Next.js 15 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Backend API**: Railway (https://web-production-b84b0.up.railway.app)

## Local Development

1. Install dependencies:
```bash
npm install
```

2. Run development server:
```bash
npm run dev
```

3. Open [http://localhost:3000](http://localhost:3000)

## Deployment to Vercel

### Option 1: Via Vercel Dashboard (Recommended)

1. Go to [vercel.com](https://vercel.com)
2. Click "Add New Project"
3. Import your GitHub repository: `SripriyaSrini/entertainment-graph`
4. Configure project:
   - **Framework Preset**: Next.js
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`
5. Add environment variable:
   - `NEXT_PUBLIC_API_URL` = `https://web-production-b84b0.up.railway.app`
6. Click "Deploy"

### Option 2: Via Vercel CLI

```bash
npm install -g vercel
cd frontend
vercel
```

Follow the prompts and set the environment variable when asked.

## Environment Variables

- `NEXT_PUBLIC_API_URL`: Backend API URL (defaults to Railway deployment)

## Project Structure

```
frontend/
├── app/
│   ├── page.tsx          # Main comparison page
│   ├── layout.tsx        # Root layout
│   └── globals.css       # Global styles
├── components/
│   ├── SearchBar.tsx     # Query input + system selection
│   ├── MovieCard.tsx     # Individual movie result
│   └── SystemColumn.tsx  # Column for one system's results
├── lib/
│   ├── api.ts            # API client
│   └── types.ts          # TypeScript types
└── package.json
```

## Features

- ✅ Natural language query input
- ✅ Multi-system selection (Pure Vector, Graphiti, OpenMemory)
- ✅ Side-by-side results comparison
- ✅ System reasoning display
- ✅ Responsive design
- ✅ Dark theme

## Post-Deployment: Update Backend CORS

After deploying to Vercel, update the Railway backend to allow your Vercel domain:

1. Get your Vercel URL (e.g., `https://your-app.vercel.app`)
2. Update [python/src/entertainment_graph/main.py](../python/src/entertainment_graph/main.py):

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "https://your-app.vercel.app"  # Add this
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

3. Commit and push to trigger Railway redeploy

## Testing

Test queries:
- "Denis Villeneuve movies"
- "epic science fiction with desert landscapes"
- "intimate stories about technology and loneliness"
- "something like Severance but lighter"

## Tech Stack

| Component | Version |
|-----------|---------|
| Next.js | 15.1.0 |
| React | 19.0.0 |
| TypeScript | 5.7.2 |
| Tailwind CSS | 3.4.17 |

## Links

- **Backend API**: https://web-production-b84b0.up.railway.app
- **API Docs**: https://web-production-b84b0.up.railway.app/docs
- **Spec**: [specs/frontend.md](../specs/frontend.md)
