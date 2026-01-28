# Directory: launch-agent-skills/skills/rag-database/skill.md
---
name: Supabase Database Setup
description: Set up Supabase database for launch-rag or launch-agentic-rag using CLI automation or manual setup
triggers:
  - supabase
  - database setup
  - vector database
  - pgvector
  - postgres
  - supabase setup
---

# Supabase Database Setup Skill

## Purpose

Set up a Supabase database for RAG applications using either:
1. **CLI Automation** (recommended) - Fully automated via `supabase` CLI
2. **Manual Setup** - Web dashboard guided walkthrough

**Works with both:**
- [launch-rag](https://github.com/ShenSeanChen/launch-rag) - Basic RAG
- [launch-agentic-rag](https://github.com/ShenSeanChen/launch-agentic-rag) - Agentic RAG

Both repos use the **identical SQL schema** (`rag_chunks` table with pgvector, 1536 dimensions).

**IMPORTANT**: This skill should be used AFTER cloning/setting up your FastAPI project (use `rag-setup` skill first).

## Instructions

### Step 0: Choose Setup Method

**Ask the user which method they prefer:**

**Option A: CLI Automation** (faster, fully automated)
- Requires: Supabase CLI installed
- Check with: `which supabase`
- Install if needed: `brew install supabase/tap/supabase` (macOS)

**Option B: Manual Setup** (web dashboard)
- No CLI required
- Step-by-step web interface

---

## 🚀 OPTION A: CLI Automation (Recommended)

### Security Note for Demos/Tutorials

**IMPORTANT**: When setting up Supabase for live demos, YouTube tutorials, or presentations:

- ✅ **Use JSON output mode** to parse values programmatically
- ✅ **Generate strong passwords** without displaying them
- ✅ **Mask all sensitive outputs** (API keys, passwords, tokens)
- ✅ **Show process, not secrets** - display steps and confirmations, not actual values
- ✅ **Auto-update .env** - write credentials directly to file without showing them
- ✅ **Confirm success** with "✅ Credentials saved to .env" messages

### Step 1: Check Requirements

```bash
# Check if Supabase CLI is installed
which supabase

# Check if SQL file exists
ls -la sql/init_supabase.sql
```

If CLI is not installed:
```bash
# macOS
brew install supabase/tap/supabase

# Other platforms: https://supabase.com/docs/guides/cli/getting-started
```

### Step 2: Login to Supabase

```bash
# Login to Supabase (opens browser for auth)
supabase login
```

This will:
- Open your browser for authentication
- Save access token locally
- Allow CLI to manage your projects

**For demos**: The login only needs to happen once and won't expose credentials.

### Step 3: Ask User for Project Details

**Always ask the user for:**

1. **Project name**
   - Suggest: `demo-agent-rag`, `youtube-rag-demo`, `agent-skills-demo`, or `rag-agent-test`
   - For demos: Use names that clearly indicate it's for testing/demo purposes

2. **Database password handling**
   - For production: Ask user to provide their own strong password
   - For demos/tutorials: Generate a strong random password automatically
   - **NEVER display the password** - store it directly in `.env`

3. **Region**
   - List options: `us-east-1`, `us-west-1`, `eu-west-1`, `ap-southeast-1`, etc.
   - Default to user's closest region

4. **Organization**
   - Get via: `supabase orgs list --output json`
   - Use the first org or ask user to select

### Step 4: Generate Secure Password (for demos)

```bash
# Generate a strong 32-character password
DB_PASSWORD=$(openssl rand -base64 32 | tr -d "=+/" | cut -c1-32)

# Tell user (but don't show password)
echo "✅ Generated strong database password (saved to .env)"
```

### Step 5: Get or Create YouTube Organization

```bash
# Get org list in JSON format
ORGS_JSON=$(supabase orgs list --output json)

# Check if "YouTube" org exists
YOUTUBE_ORG=$(echo "$ORGS_JSON" | jq -r '.[] | select(.name == "YouTube") | .id')

if [ -z "$YOUTUBE_ORG" ]; then
  # YouTube org doesn't exist, check for alternatives or create one
  echo "ℹ️  No 'YouTube' organization found"
  echo "   Creating a new 'YouTube' organization for demo projects..."

  # Create YouTube org (requires web UI or API - CLI may not support org creation)
  # Guide user to create it manually if needed
  echo "   Please create a 'YouTube' organization in Supabase dashboard"
  echo "   Or using the first available organization..."

  ORG_ID=$(echo "$ORGS_JSON" | jq -r '.[0].id')
  ORG_NAME=$(echo "$ORGS_JSON" | jq -r '.[0].name')
  echo "✅ Using organization: $ORG_NAME"
else
  ORG_ID="$YOUTUBE_ORG"
  echo "✅ Using organization: YouTube (perfect for demos!)"
fi
```

**IMPORTANT**:
- For demo/tutorial projects, always prefer the "YouTube" organization if it exists
- This keeps demo projects organized separately from production
- If "YouTube" org doesn't exist, use the first available or ask user to create one

### Step 6: Create Project via CLI

```bash
# Create project with JSON output to capture details
supabase projects create <project-name> \
  --org-id "$ORG_ID" \
  --region us-east-1 \
  --db-password "$DB_PASSWORD" \
  --output json > project_output.json

# Parse project details
PROJECT_REF=$(cat project_output.json | jq -r '.id')
PROJECT_URL="https://${PROJECT_REF}.supabase.co"

echo "✅ Project created: <project-name>"
echo "✅ Project URL: $PROJECT_URL (saved to .env)"

# Clean up temp file (don't leave it around)
rm project_output.json
```

**Important**:
- Use `--output json` to get machine-readable output
- Parse with `jq` or Python for safety
- Never echo sensitive values directly
- Wait for project to be ready (~2 minutes)

### Step 7: Wait for Project Initialization

```bash
# Wait for project to be fully ready (usually ~2 minutes)
echo "⏳ Waiting for project initialization..."
sleep 120

echo "✅ Project should be ready now"
```

### Step 8: Get API Keys (Securely)

```bash
# Get API keys (default table output is more reliable than JSON)
supabase projects api-keys --project-ref "$PROJECT_REF" > /tmp/api_keys_output.txt

# Parse the table output (more reliable than JSON for this command)
ANON_KEY=$(grep "anon" /tmp/api_keys_output.txt | awk '{print $3}')
SERVICE_KEY=$(grep "service_role" /tmp/api_keys_output.txt | awk '{print $3}')

# Confirm without showing values
echo "✅ Retrieved API keys (saved to .env)"
echo "   - Anon key: ${ANON_KEY:0:20}... (hidden)"
echo "   - Service key: ${SERVICE_KEY:0:20}... (hidden)"

# Clean up temp file
rm /tmp/api_keys_output.txt
```

**IMPORTANT**: The `--output json` flag for api-keys command may not work correctly in all Supabase CLI versions. Use the default table output and parse with awk/grep for reliability.

### Step 9: Link Local Project

```bash
# Link the local directory to the Supabase project
cd fastapi-project  # or current project directory
supabase link --project-ref "$PROJECT_REF"

echo "✅ Linked local project to Supabase"
```

### Step 10: Run SQL Initialization

```bash
# Execute the SQL file directly via psql connection
echo "🔧 Running database initialization..."

# Use Supabase CLI to execute SQL
supabase db reset --linked

# Or manually run the SQL
PGPASSWORD="$DB_PASSWORD" psql \
  "postgresql://postgres:$DB_PASSWORD@db.$PROJECT_REF.supabase.co:5432/postgres" \
  -f sql/init_supabase.sql

echo "✅ Database initialized with pgvector and RAG schema"
```

**Alternative migration approach:**
```bash
# Initialize Supabase in project
supabase init

# Copy SQL file to migrations
mkdir -p supabase/migrations
cp sql/init_supabase.sql supabase/migrations/$(date +%Y%m%d%H%M%S)_init.sql

# Push migrations
supabase db push

echo "✅ Migrations applied successfully"
```

### Step 11: Auto-Update .env File (Secure)

**Use Edit tool to update .env WITHOUT displaying sensitive values:**

```bash
# Update .env file securely
# Use the Edit tool to modify the .env file programmatically

# Values to update:
# SUPABASE_URL="$PROJECT_URL"
# SUPABASE_ANON_KEY="$ANON_KEY"
# SUPABASE_SERVICE_ROLE_KEY="$SERVICE_KEY"

echo "✅ Updated .env file with Supabase credentials"
echo "   Location: fastapi-project/.env"
```

**IMPORTANT for Claude Code**:
- Use the `Edit` tool to modify `.env` file
- Replace placeholder values with actual credentials
- Do NOT echo or display the actual keys in output
- Confirm with generic success message

### Step 11b: Configure AI Provider (Critical!)

**After updating Supabase credentials, check and fix AI provider settings:**

```bash
# Check if user has valid API keys
if grep -q "your_anthropic_api_key_here" .env; then
  echo "⚠️  Anthropic key is placeholder - switching to OpenAI"

  # Use Edit tool to change AI_PROVIDER to openai
  # sed -i '' 's/AI_PROVIDER=anthropic/AI_PROVIDER=openai/' .env

  echo "✅ Set AI_PROVIDER=openai (change to 'anthropic' if you add Anthropic key later)"
fi

# Verify OpenAI key exists
if grep -q "your_openai_api_key_here" .env; then
  echo "❌ ERROR: OpenAI API key is required!"
  echo "   Please update OPENAI_API_KEY in .env with your actual key"
  echo "   Get your key from: https://platform.openai.com/api-keys"
fi
```

**Key Points**:
- ✅ **OpenAI key is REQUIRED** - used for embeddings (text-embedding-3-small)
- ✅ **Default to AI_PROVIDER=openai** unless user explicitly has Anthropic key
- ⚠️ **Check for placeholder values** and warn user to replace them
- ⚠️ **Don't leave placeholder API keys** - they cause runtime 401 errors

### Step 12: Verify Setup

```bash
# Test database connection (in project directory)
cd fastapi-project
source venv/bin/activate
python test_setup.py

echo "✅ Setup verification complete"
```

### Step 13: Display Summary (Safe for Demos)

```bash
echo ""
echo "=================================================="
echo "🎉 Supabase Setup Complete!"
echo "=================================================="
echo ""
echo "Project Details:"
echo "  Name: <project-name>"
echo "  URL: $PROJECT_URL"
echo "  Region: us-east-1"
echo ""
echo "Database:"
echo "  ✅ pgvector extension enabled"
echo "  ✅ rag_chunks table created"
echo "  ✅ Vector search functions ready"
echo "  ✅ Row-level security configured"
echo ""
echo "Credentials:"
echo "  ✅ Supabase credentials saved to .env"
echo "  ✅ AI_PROVIDER set to: openai"
echo ""
echo "⚠️  IMPORTANT: Verify Your API Keys"
echo "  • OpenAI key is REQUIRED (for embeddings)"
echo "  • If you see 401 errors, check .env for placeholder values"
echo "  • Don't use placeholder keys like 'your_api_key_here'"
echo ""
echo "Next Steps:"
echo "  1. Verify your OpenAI API key is set in .env"
echo "  2. cd fastapi-project"
echo "  3. source venv/bin/activate"
echo "  4. uvicorn main:app --reload --port 8000"
echo "  5. Visit http://localhost:8000/docs"
echo "  6. Try /seed endpoint to populate database"
echo "  7. Ask questions at http://localhost:8000/chat"
echo ""
echo "=================================================="
```

---

## 📋 OPTION B: Manual Setup

### Step 1: Check for SQL Initialization File

```bash
# Check if SQL init file exists
ls -la sql/
```

Expected: `sql/init_supabase.sql`

### Step 2: Create Supabase Project (Manual)

**Tell the user:**

1. Go to [https://supabase.com](https://supabase.com)
2. Sign in or create an account
3. Click "New Project"
4. Fill in project details:
   - **Name**: Choose a project name (e.g., "my-rag-agent")
   - **Database Password**: Create a strong password (save it!)
   - **Region**: Choose closest to you
   - **Pricing Plan**: Free tier is sufficient for development
5. Click "Create new project"
6. **Wait ~2 minutes** for project to initialize

### Step 3: Retrieve API Keys

Once the project is ready, guide the user to get their API keys:

**Tell the user:**

1. In your Supabase dashboard, go to **Settings** (gear icon in sidebar)
2. Click **API** in the settings menu
3. Copy these three values (you'll need them for `.env`):
   - **Project URL**: `https://xxxxx.supabase.co`
   - **anon public key**: Starts with `eyJ...` (long string)
   - **service_role secret key**: Starts with `eyJ...` (different long string)

**Important**: Keep the service_role key SECRET - it has full database access!

### Step 4: Run SQL Initialization Script

**Tell the user:**

1. In Supabase dashboard, go to **SQL Editor** (left sidebar)
2. Click **New query** button
3. Open the local file `sql/init_supabase.sql` and copy its ENTIRE contents
4. Paste into the SQL Editor
5. Click **Run** (or press Cmd/Ctrl + Enter)
6. You should see success messages and verification results at the bottom

**What this script creates:**
- ✅ pgvector extension for vector operations
- ✅ `rag_chunks` table with VECTOR(1536) for embeddings
- ✅ IVFFlat index for fast vector similarity search
- ✅ `match_chunks()` function for semantic search
- ✅ `get_chunk_stats()` function for database statistics
- ✅ Row Level Security policies
- ✅ Performance indexes

### Step 5: Update Environment Variables

Help the user update their `.env` file:

```bash
# Open .env file
# Edit these values with your Supabase credentials:

SUPABASE_URL=https://your-project-ref.supabase.co
SUPABASE_ANON_KEY=eyJ...your_anon_key_from_step_3
SUPABASE_SERVICE_ROLE_KEY=eyJ...your_service_role_key_from_step_3
```

**Also ensure these are set:**
```bash
# OpenAI (required for embeddings)
OPENAI_API_KEY=sk-your_openai_key
OPENAI_EMBED_MODEL=text-embedding-3-small
OPENAI_CHAT_MODEL=gpt-4o

# AI Provider
AI_PROVIDER=openai

# Optional: Anthropic
ANTHROPIC_API_KEY=your_anthropic_key
ANTHROPIC_CHAT_MODEL=claude-3-5-sonnet-20241022
```

### Step 6: Verify Setup

After configuration, test the database connection:

```bash
# Run the test script
python test_setup.py
```

This script will verify:
- ✅ Environment variables are set
- ✅ Supabase connection works
- ✅ Database tables exist
- ✅ Vector functions are available

### Step 7: Seed Initial Data (Optional)

If the project has sample data, seed it:

```bash
# Start the server
uvicorn main:app --reload --port 8000

# In another terminal, seed the database
curl -X POST http://localhost:8000/seed
```

## What Gets Created

The `sql/init_supabase.sql` script from launch-rag creates:

| Component | Description |
|-----------|-------------|
| **pgvector extension** | Enables vector operations in PostgreSQL |
| **rag_chunks table** | Stores text chunks with 1536-dim embeddings |
| **Vector indexes** | IVFFlat index for fast similarity search |
| **match_chunks()** | Function for semantic search queries |
| **get_chunk_stats()** | Helper to check database statistics |
| **RLS policies** | Security rules for service/auth/anon access |

## Checklist

When setting up Supabase:

- [ ] Create new project at supabase.com (~2 min wait)
- [ ] Copy Project URL from Settings → API
- [ ] Copy anon key from Settings → API
- [ ] Copy service_role key from Settings → API
- [ ] Open SQL Editor in Supabase dashboard
- [ ] Copy entire contents of `sql/init_supabase.sql`
- [ ] Run the SQL script in Supabase
- [ ] Verify success messages appear
- [ ] Update `.env` with Supabase credentials
- [ ] Run `python test_setup.py` to verify
- [ ] Test `/healthz` endpoint

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| "Extension not found" | Make sure you ran the full SQL script |
| "Function does not exist" | Check if `match_chunks()` was created |
| "Permission denied" | Use service_role key for backend operations |
| Connection timeout | Check SUPABASE_URL is correct |
| Dimension mismatch | launch-rag uses 1536 (text-embedding-3-small) |

## Important Notes

- **Use service_role key** for backend operations (has full access)
- **Keep service_role secret** - never expose in frontend code
- **Vector dimension is 1536** - matches text-embedding-3-small
- The SQL file is **self-contained** - run it once on a fresh project
- Verification queries are included at the end of the SQL script

## Related Skills

- `rag-setup` - Clone and set up the launch-rag backend first
- Use this skill AFTER `rag-setup` to complete the database setup
