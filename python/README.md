# Entertainment Graph - Backend

FastAPI backend for comparing retrieval systems.

## Setup

### 1. Install dependencies

```bash
cd python
pip install -e .
```

### 2. Configure environment

```bash
cp .env.example .env
```

Edit `.env` and add:
- `OPENAI_API_KEY` (required for embeddings and LLM)
- `NEO4J_URI`, `NEO4J_USERNAME`, `NEO4J_PASSWORD` (optional, for Mem0 with graph)

### 3. Test systems

```bash
python test_basic.py
```

This will:
- Test Pure Vector system (ChromaDB + OpenAI)
- Test Mem0 system
- Ingest sample movies
- Run test queries

### 4. Start server

```bash
uvicorn entertainment_graph.main:app --reload
```

Visit: http://localhost:8000/docs

## API Endpoints

### Health
- `GET /health` - Check system status

### Movies
- `GET /movies` - List all movies
- `GET /movies/{movie_id}` - Get movie details

### Ingest
- `POST /ingest` - Ingest all movies into all systems
- `POST /ingest/{system_name}` - Ingest into specific system

### Query
- `POST /query/{system_name}` - Query a specific system
- `POST /query/compare` - Query all systems and compare
- `GET /query/systems` - List available systems

## Example Query

```bash
curl -X POST http://localhost:8000/query/compare \
  -H "Content-Type: application/json" \
  -d '{"query": "something like Severance but lighter", "limit": 5}'
```

## Systems

- **pure_vector**: ChromaDB + OpenAI embeddings + LLM (baseline)
- **mem0**: Mem0 hybrid memory (vector + optional graph)
- **mem0_graph**: Mem0 with Neo4j graph (if Neo4j configured)

## Project Structure

```
src/entertainment_graph/
├── main.py              # FastAPI app
├── config.py            # Settings
├── models/              # Data schemas
│   ├── movie.py
│   └── query.py
├── systems/             # Retrieval systems
│   ├── base.py
│   ├── pure_vector.py
│   └── mem0_system.py
├── routers/             # API endpoints
│   ├── query.py
│   ├── movies.py
│   ├── ingest.py
│   └── health.py
└── services/            # Business logic
    └── data_loader.py
```
