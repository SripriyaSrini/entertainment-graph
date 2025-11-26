# Frontend Specification: Entertainment Graph Comparison UI

## Goal

Build a React frontend that allows users to:
1. Query the Entertainment Graph API across multiple retrieval systems
2. View results side-by-side for comparison
3. Evaluate and understand differences between systems

This supports Phase 1's goal: empirical comparison of Pure Vector, Graphiti, and OpenMemory systems.

---

## Architecture

### Stack

| Component | Choice | Rationale |
|-----------|--------|-----------|
| Framework | Next.js 14 (App Router) | React with SSR, great Vercel deployment |
| Language | TypeScript | Type safety for API contracts |
| Styling | Tailwind CSS | Rapid UI development, consistent design |
| HTTP Client | fetch (native) | Simple, no extra dependencies needed |
| Deployment | Vercel | Free tier, optimized for Next.js |

### Backend Connection

- **API Base URL**: `https://web-production-b84b0.up.railway.app` (Railway deployment)
- **Endpoints**:
  - `GET /health` - System status
  - `POST /query/{system_name}` - Query a specific system
  - `POST /ingest/{system_name}/bulk` - Ingest movies

---

## User Interface

### Pages

#### 1. Home/Search Page (`/`)

**Purpose**: Main query interface

**Components**:
- Query input (text area for natural language)
- System selector (checkboxes: Pure Vector, Graphiti, OpenMemory)
- Limit selector (3, 5, 10 results)
- Search button
- Results display area

**Layout**:
```
┌─────────────────────────────────────────────┐
│  Entertainment Graph Comparison             │
│  ─────────────────────────────────────      │
│  [Search Box                          ]     │
│  Systems: ☑ Pure Vector  ☑ Graphiti  ☐ Open│
│  Limit: ○ 3  ● 5  ○ 10                      │
│  [Search Button]                            │
│                                             │
│  ┌─────────────┬─────────────┬──────────┐  │
│  │ Pure Vector │  Graphiti   │OpenMemory│  │
│  │ ─────────── │ ─────────── │──────────│  │
│  │ Results...  │ Results...  │Results...│  │
│  └─────────────┴─────────────┴──────────┘  │
└─────────────────────────────────────────────┘
```

#### 2. System Status Page (`/status`)

**Purpose**: View system health

**Components**:
- Health check for each system
- Connection status to Railway API
- Recent ingestion stats (if available)

---

## Components

### 1. `SearchBar`

**Props**:
- `onSearch: (query: string, systems: string[], limit: number) => void`
- `isLoading: boolean`

**Features**:
- Text input for query
- Multi-select for systems
- Limit selector
- Loading state

### 2. `ResultsComparison`

**Props**:
- `results: Record<string, QueryResult>`
- `query: string`

**Features**:
- Side-by-side column layout
- Each column shows one system's results
- Synchronized scrolling (optional)

### 3. `MovieCard`

**Props**:
- `movie: Movie`
- `score: number`
- `explanation: string`

**Features**:
- Title, year, director
- Score/relevance indicator
- Explanation text
- Visual styling (poster placeholder or gradient)

### 4. `SystemColumn`

**Props**:
- `systemName: string`
- `results: Movie[]`
- `reasoning: string`

**Features**:
- System name header
- Agent reasoning section
- List of MovieCards
- Empty state if no results

---

## Data Types

### TypeScript Interfaces

```typescript
interface Movie {
  id: string;
  title: string;
  year: number;
  director: string[];
  genres: string[];
  plot_summary?: string;
  score?: number;
  explanation?: string;
}

interface QueryResult {
  results: Movie[];
  reasoning: string;
  system_name: string;
}

interface HealthStatus {
  status: string;
  pure_vector: boolean;
  graphiti: boolean;
  openmemory: boolean;
}
```

---

## API Integration

### Environment Variables

```bash
# .env.local
NEXT_PUBLIC_API_URL=https://web-production-b84b0.up.railway.app
```

### API Service (`lib/api.ts`)

```typescript
export class EntertainmentGraphAPI {
  private baseURL: string;

  async query(system: string, query: string, limit: number): Promise<QueryResult>
  async health(): Promise<HealthStatus>
}
```

---

## Styling Guidelines

### Design Principles

1. **Clean & Minimal**: Focus on content comparison, not decoration
2. **Responsive**: Mobile-friendly (stack columns vertically)
3. **Accessible**: Proper contrast, keyboard navigation
4. **Fast**: Optimistic UI updates, loading states

### Color Palette

```
Background: #0f172a (dark slate)
Cards: #1e293b (lighter slate)
Text: #e2e8f0 (light gray)
Accent: #3b82f6 (blue)
Success: #10b981 (green)
Error: #ef4444 (red)
```

### Typography

- Headers: `font-bold text-2xl`
- Body: `text-base`
- Explanations: `text-sm text-gray-400`

---

## Implementation Plan

### Phase 1: Basic Query Interface (MVP)
1. ✅ Create Next.js project
2. ✅ Set up Tailwind CSS
3. ✅ Create SearchBar component
4. ✅ Create ResultsComparison component
5. ✅ Create MovieCard component
6. ✅ Implement API client
7. ✅ Connect to Railway backend
8. ✅ Deploy to Vercel

### Phase 2: Enhanced Features (Future)
- [ ] Save queries/results
- [ ] Export comparison to PDF
- [ ] Evaluation scoring UI (1-5 stars)
- [ ] Query history
- [ ] Advanced filters (by genre, year, director)

---

## Success Criteria

Frontend is complete when:
- [ ] Users can enter a query and select systems
- [ ] Results display side-by-side for comparison
- [ ] Each system shows reasoning + results
- [ ] UI is responsive and accessible
- [ ] Deployed to Vercel at a public URL
- [ ] Connected to Railway backend API

---

## File Structure

```
frontend/
├── app/
│   ├── page.tsx              # Home/Search page
│   ├── status/
│   │   └── page.tsx          # System status
│   └── layout.tsx            # Root layout
├── components/
│   ├── SearchBar.tsx
│   ├── ResultsComparison.tsx
│   ├── SystemColumn.tsx
│   └── MovieCard.tsx
├── lib/
│   ├── api.ts                # API client
│   └── types.ts              # TypeScript types
├── public/
│   └── (static assets)
└── package.json
```

---

## Deployment

### Vercel Setup

1. Connect GitHub repo to Vercel
2. Set environment variable: `NEXT_PUBLIC_API_URL`
3. Deploy from `main` branch
4. Auto-deploy on push

### CORS Configuration

Backend already configured for frontend:
```python
allow_origins=["http://localhost:3000", "http://localhost:5173"]
```

Will need to add Vercel domain after deployment.

---

## Open Questions

- [ ] Should we add authentication? (Not for Phase 1 MVP)
- [ ] Should results persist in local storage? (Nice-to-have)
- [ ] Should we show query latency? (Yes - useful for comparison)

---

## Status

**Phase**: Ready to implement
**Next Steps**: Create Next.js project and implement SearchBar component
