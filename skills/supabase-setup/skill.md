# Directory: launch-agent-skills/skills/supabase-setup/skill.md
---
name: Supabase Database Setup
description: Configure Supabase with pgvector, proper schemas, and RLS policies following launch-rag patterns
triggers:
  - supabase
  - database setup
  - vector database
  - pgvector
  - postgres
---

# Supabase Database Setup Skill

## Purpose

Set up a Supabase database with:
- pgvector extension for embeddings
- Proper table schemas with indexes
- Row Level Security (RLS) policies
- Vector search functions
- Python client integration

Based on patterns from [launch-rag](https://github.com/ShenSeanChen/launch-rag) and [launch-agentic-rag](https://github.com/ShenSeanChen/launch-agentic-rag).

## Instructions

### Step 1: Create SQL Initialization Script

**sql/init_supabase.sql**:

```sql
-- Directory: project-name/sql/init_supabase.sql
-- Supabase initialization script for RAG application
-- Run this in Supabase SQL Editor

-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create main table with vector column
CREATE TABLE IF NOT EXISTS documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    chunk_id TEXT UNIQUE NOT NULL,
    source TEXT,
    text TEXT NOT NULL,
    embedding VECTOR(1536),  -- OpenAI ada-002: 1536, text-embedding-3-large: 3072
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_documents_chunk_id ON documents(chunk_id);
CREATE INDEX IF NOT EXISTS idx_documents_source ON documents(source);
CREATE INDEX IF NOT EXISTS idx_documents_created_at ON documents(created_at DESC);

-- Create vector similarity search index (IVFFlat for large datasets)
CREATE INDEX IF NOT EXISTS idx_documents_embedding ON documents 
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- Vector search function
CREATE OR REPLACE FUNCTION match_documents(
    query_embedding VECTOR(1536),
    match_threshold FLOAT DEFAULT 0.7,
    match_count INT DEFAULT 10
)
RETURNS TABLE (
    id UUID,
    chunk_id TEXT,
    source TEXT,
    text TEXT,
    metadata JSONB,
    similarity FLOAT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        d.id,
        d.chunk_id,
        d.source,
        d.text,
        d.metadata,
        1 - (d.embedding <=> query_embedding) AS similarity
    FROM documents d
    WHERE 1 - (d.embedding <=> query_embedding) > match_threshold
    ORDER BY d.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;

-- Enable Row Level Security
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;

-- RLS Policies (adjust based on your auth needs)

-- Policy: Allow public read access (for public knowledge bases)
CREATE POLICY "Allow public read access"
ON documents FOR SELECT
TO public
USING (true);

-- Policy: Allow authenticated users to insert
CREATE POLICY "Allow authenticated insert"
ON documents FOR INSERT
TO authenticated
WITH CHECK (true);

-- Policy: Allow service role full access
CREATE POLICY "Allow service role full access"
ON documents FOR ALL
TO service_role
USING (true)
WITH CHECK (true);

-- Updated at trigger
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER documents_updated_at
    BEFORE UPDATE ON documents
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at();
```

### Step 2: Create Database Client

**app/core/database.py**:

```python
# Directory: project-name/app/core/database.py
"""
Supabase database client and operations.
"""

from supabase import create_client, Client
from typing import List, Dict, Any, Optional

from app.core.config import settings


class Database:
    """Supabase database client wrapper."""
    
    _client: Optional[Client] = None
    
    @classmethod
    def get_client(cls) -> Client:
        """Get or create Supabase client (singleton)."""
        if cls._client is None:
            cls._client = create_client(
                settings.SUPABASE_URL,
                settings.SUPABASE_SERVICE_ROLE_KEY
            )
        return cls._client
    
    @classmethod
    async def health_check(cls) -> bool:
        """Check database connectivity."""
        try:
            client = cls.get_client()
            # Simple query to verify connection
            client.table("documents").select("id").limit(1).execute()
            return True
        except Exception:
            return False
    
    @classmethod
    async def upsert_documents(
        cls, 
        documents: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Upsert documents with embeddings.
        
        Args:
            documents: List of dicts with chunk_id, text, embedding, etc.
        
        Returns:
            Upsert result from Supabase
        """
        client = cls.get_client()
        result = client.table("documents").upsert(
            documents,
            on_conflict="chunk_id"
        ).execute()
        return result
    
    @classmethod
    async def vector_search(
        cls,
        query_embedding: List[float],
        match_threshold: float = 0.7,
        match_count: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Perform vector similarity search.
        
        Args:
            query_embedding: Query vector (1536 dimensions for ada-002)
            match_threshold: Minimum similarity score (0-1)
            match_count: Maximum results to return
        
        Returns:
            List of matching documents with similarity scores
        """
        client = cls.get_client()
        result = client.rpc(
            "match_documents",
            {
                "query_embedding": query_embedding,
                "match_threshold": match_threshold,
                "match_count": match_count
            }
        ).execute()
        return result.data


# Convenience instance
db = Database()
```

### Step 3: Embedding Dimensions Guide

| Model | Dimensions | Use Case |
|-------|------------|----------|
| text-embedding-ada-002 | 1536 | General purpose, good balance |
| text-embedding-3-small | 1536 | Cost-effective, fast |
| text-embedding-3-large | 3072 | Highest quality |

**Important**: Match your `VECTOR(N)` column size to your embedding model!

### Step 4: Supabase Setup Checklist

When setting up Supabase:

- [ ] Create new project at supabase.com
- [ ] Wait for project to initialize (~2 min)
- [ ] Get API keys from Settings → API
  - [ ] Project URL
  - [ ] Anon Key
  - [ ] Service Role Key (keep secret!)
- [ ] Run SQL initialization script
- [ ] Verify pgvector extension is enabled
- [ ] Test connection with health check

### Step 5: Environment Variables

Add to `.env`:

```bash
# Supabase Configuration
SUPABASE_URL=https://your-project-ref.supabase.co
SUPABASE_ANON_KEY=eyJ...your_anon_key
SUPABASE_SERVICE_ROLE_KEY=eyJ...your_service_role_key
```

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| "pgvector not found" | Run `CREATE EXTENSION vector;` |
| Dimension mismatch | Match VECTOR(N) to embedding model |
| Slow queries | Add IVFFlat index, tune `lists` parameter |
| RLS blocking requests | Check policies, use service role for admin ops |

## Related Skills

- `fastapi-setup` - Create the API layer
