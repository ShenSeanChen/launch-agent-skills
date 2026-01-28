# Directory: launch-agent-skills/skills/rag-setup/skill.md
---
name: FastAPI Project Setup
description: Clone and set up launch-rag or launch-agentic-rag - production-ready FastAPI backends with RAG capabilities
triggers:
  - fastapi
  - api setup
  - project structure
  - python api
  - backend setup
  - launch-rag
  - rag backend
  - agentic rag
  - agent backend
---

# FastAPI Project Setup Skill

## Purpose

Clone and set up a production-ready FastAPI backend for RAG (Retrieval-Augmented Generation):

### Available Options:

**1. [launch-rag](https://github.com/ShenSeanChen/launch-rag)** - Basic RAG
- Vector similarity search with Supabase
- Question answering with citations
- Simple, focused implementation
- Perfect for learning RAG fundamentals

**2. [launch-agentic-rag](https://github.com/ShenSeanChen/launch-agentic-rag)** - Agentic RAG
- Everything in launch-rag PLUS:
- Agent reasoning (Retrieve → Reason → Decide → Act)
- Tool calling (schedule meetings, send emails)
- Multi-turn conversations
- Google Calendar/Gmail integration (optional)

Both include:
- Multiple AI provider support (OpenAI, Anthropic)
- Clean folder structure (core, services, models)
- Environment configuration with validation
- Health checks and API documentation
- Docker support
- Type hints and Pydantic validation

## Prerequisites

- Python 3.11+
- Supabase account
- OpenAI API key
- Anthropic API key (optional)
- Google Cloud credentials (optional, for agentic-rag tools)

## Instructions

### Step 0: Ask User Which Repository

**IMPORTANT**: Ask the user which version they want to set up:

**Prompt the user:**
```
Which FastAPI backend would you like to set up?

1. launch-rag (Basic RAG - recommended for learning)
   - Simple vector search + Q&A
   - Faster setup, fewer dependencies

2. launch-agentic-rag (Agentic RAG - advanced features)
   - Agent reasoning with tools
   - Calendar/email integration
   - Multi-turn conversations

Choose: [1/2]
```

**Decision Logic:**
- If user says "basic", "simple", "learning", or "1" → use launch-rag
- If user says "agentic", "agent", "tools", or "2" → use launch-agentic-rag
- If unclear, recommend launch-rag for first-time users

**Set variables:**
```bash
# Based on user choice
REPO_NAME="launch-rag"  # or "launch-agentic-rag"
REPO_URL="https://github.com/ShenSeanChen/$REPO_NAME.git"
```

### Step 1: Clone the Repository

**IMPORTANT**: Ask the user where they want to clone the repo (which directory), or use the current working directory.

```bash
# Clone the chosen repo
git clone $REPO_URL [project-name]
cd [project-name]
```

Replace `[project-name]` with the desired project folder name.

**Example:**
- `git clone https://github.com/ShenSeanChen/launch-rag.git my-rag-api`
- `git clone https://github.com/ShenSeanChen/launch-agentic-rag.git my-agent-api`

### Step 2: Create Virtual Environment

```bash
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables

Create a `.env` file from the template:

```bash
cp .env.example .env
```

**IMPORTANT**: The `.env.example` has placeholder values that MUST be replaced.

Then edit `.env` with your actual credentials:

```bash
# Required - Supabase (will be set by rag-database skill)
SUPABASE_URL=https://your-project-ref.supabase.co
SUPABASE_ANON_KEY=your_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key

# Required - OpenAI (needed for embeddings regardless of AI provider)
OPENAI_API_KEY=sk-your_openai_key
OPENAI_EMBED_MODEL=text-embedding-3-small
OPENAI_CHAT_MODEL=gpt-4o

# AI Provider Configuration
# IMPORTANT: Set to "openai" if you only have OpenAI key
# Set to "anthropic" only if you have BOTH OpenAI (for embeddings) AND Anthropic keys
AI_PROVIDER=openai

# Optional - Anthropic (only needed if AI_PROVIDER=anthropic)
ANTHROPIC_API_KEY=your_anthropic_key
ANTHROPIC_CHAT_MODEL=claude-3-5-sonnet-20241022
```

**Key Points**:
- ✅ **OpenAI key is ALWAYS required** (for embeddings via text-embedding-3-small)
- ✅ **Set AI_PROVIDER=openai** by default (uses GPT-4o for chat)
- ✅ **Only set AI_PROVIDER=anthropic** if you have a valid Anthropic key
- ⚠️ **Don't leave placeholder values** like `your_anthropic_api_key_here` - the app will fail at runtime

### Step 5: Set Up Supabase Database

Run the SQL initialization script in your Supabase SQL editor:

```bash
# The sql/init.sql file contains the database schema
# Copy and run it in Supabase SQL Editor at:
# https://supabase.com/dashboard/project/[your-project]/editor
```

### Step 6: Run the Server

```bash
uvicorn main:app --reload --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs
- **Health**: http://localhost:8000/healthz
- **Chat UI**: http://localhost:8000/chat (if available)

### Step 7: Test the Setup (Optional)

```bash
python test_setup.py
```

### Step 8: Next Steps Based on Repository

**If launch-rag:**
- ✅ Basic setup complete!
- Run `rag-database` skill next to configure database
- Start using the RAG endpoints

**If launch-agentic-rag:**
- ✅ Basic setup complete!
- Run `rag-database` skill next to configure database
- (Optional) Run `rag-tools` skill to configure Google Calendar/Gmail tools
- Explore agent reasoning and tool calling features

## Checklist

**Common steps (both repos):**
- [ ] Ask user: launch-rag or launch-agentic-rag?
- [ ] Clone the chosen repository to desired location
- [ ] Create Python 3.11+ virtual environment
- [ ] Install all dependencies from requirements.txt
- [ ] Copy .env.example to .env
- [ ] Add OpenAI API key to .env (REQUIRED)
- [ ] Set AI_PROVIDER=openai by default
- [ ] (Optional) Add Anthropic API key if using Claude

**For rag-database (next step):**
- [ ] Add Supabase credentials to .env
- [ ] Run SQL initialization script in Supabase
- [ ] Verify database connection

**For launch-agentic-rag only:**
- [ ] (Optional) Set up Google Cloud service account
- [ ] (Optional) Configure Calendar/Gmail tools

## What You Get

**launch-rag includes:**

```
launch-rag/
├── app/
│   ├── core/              # Configuration & database
│   ├── models/            # Pydantic schemas
│   ├── services/          # RAG logic, embeddings, AI
│   └── main.py            # FastAPI app
├── sql/
│   └── init_supabase.sql  # Database setup
├── static/                # Chat UI
├── test_setup.py
└── requirements.txt
```

**launch-agentic-rag includes (everything above PLUS):**

```
launch-agentic-rag/
├── app/
│   ├── core/              # Same as launch-rag
│   ├── models/            # Same as launch-rag
│   ├── services/
│   │   ├── rag.py         # Enhanced with agent reasoning
│   │   ├── agent.py       # Agent decision-making logic
│   │   └── tools/         # 🆕 Tool implementations
│   │       ├── calendar.py   # Google Calendar integration
│   │       └── email.py      # Gmail integration
│   └── main.py            # FastAPI app with agent endpoints
├── credentials/           # 🆕 Google Cloud credentials
└── requirements.txt       # Additional dependencies for tools
```

## Example Usage

**User**: "Set up a FastAPI backend for my new project"

**Claude should**:
1. **Ask which repo**: "Do you want basic RAG or agentic RAG?"
2. **Ask where to clone**: Current directory or specific path?
3. **Clone chosen repo** with user-specified project name
4. Create virtual environment
5. Install dependencies
6. Set up .env file (with AI_PROVIDER=openai by default)
7. Remind user about next steps:
   - Add OpenAI API key to .env
   - Run `rag-database` skill for database
   - (If agentic-rag) Optionally run `rag-tools` for Google integrations

## Important Notes

- **Always ask** where to clone the repo before running git clone
- The repo is production-ready with RAG capabilities built-in
- Requires Supabase for vector storage (pgvector extension)
- Supports both OpenAI and Anthropic AI providers
- Includes Docker support for easy deployment

## Related Skills

- `rag-database` - Configure Supabase database and pgvector
