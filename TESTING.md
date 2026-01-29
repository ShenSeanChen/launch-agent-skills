# Directory: launch-agent-skills/TESTING.md
# Testing Agent Skills - Step-by-Step Guide

This guide provides **exact prompts** you can copy-paste into Claude Code to test each skill, along with the expected outcomes.

---

## Prerequisites

1. **Clone this repository**:
   ```bash
   git clone https://github.com/ShenSeanChen/launch-agent-skills.git
   cd launch-agent-skills
   ```

2. **Open in Claude Code**:
   ```bash
   claude .
   ```

3. **Verify Claude loads CLAUDE.md**: Claude Code will automatically read the project instructions.

---

## Part 1: WhatsApp Skills

### Test 1: Parse WhatsApp Export

**Copy this prompt**:
```
Parse the WhatsApp chat in examples/sample-whatsapp-chat.txt
```

**Expected outcome**:
- ✅ Claude reads [skills/whatsapp-parser/skill.md](skills/whatsapp-parser/skill.md)
- ✅ Parses 46 messages from the sample chat
- ✅ Returns structured JSON with:
  - `metadata`: participants, message_count, date_range
  - `messages`: array with timestamp, sender, content
  - `statistics`: messages per person, media count

**What you'll see**:
```json
{
  "metadata": {
    "participants": ["Alice Developer", "Bob Engineer", "Carol PM"],
    "message_count": 46,
    "date_range": {
      "start": "28/01/2026, 09:15:30",
      "end": "28/01/2026, 16:45:12"
    }
  },
  "messages": [...],
  "statistics": {...}
}
```

---

### Test 2: Summarize Conversation

**Copy this prompt**:
```
Summarize the WhatsApp chat in examples/sample-whatsapp-chat.txt
```

**Expected outcome**:
- ✅ Claude reads [skills/whatsapp-summarizer/skill.md](skills/whatsapp-summarizer/skill.md)
- ✅ May automatically use `whatsapp-parser` skill first if needed
- ✅ Returns summary with:
  - **TL;DR**: 2-3 sentence overview
  - **Key Topics**: Main discussion themes
  - **Decisions**: What was agreed upon
  - **Conversation Stats**: Activity metrics

**What you'll see**:
```markdown
## Chat Summary: Jan 28, 2026

### TL;DR
Team discussed auth bug fix (PR #142), planned new microservice using FastAPI + Supabase,
and scheduled feature planning meeting for next week.

### Key Decisions
- ✅ Use FastAPI for new microservice backend
- ✅ Deploy Supabase for vector database (pgvector)
- ✅ Schedule deep dive meeting for Thursday 2pm

### Topics Discussed
1. **Bug Fix & PR Review** - Auth issue fixed in PR #142
2. **Architecture Planning** - New microservice stack decision
3. **Sprint Planning** - Feature prioritization for next sprint
```

---

### Test 3: Extract Action Items

**Copy this prompt**:
```
Extract all action items and TODOs from examples/sample-whatsapp-chat.txt
```

**Expected outcome**:
- ✅ Claude reads [skills/whatsapp-action-extractor/skill.md](skills/whatsapp-action-extractor/skill.md)
- ✅ Identifies explicit TODOs and implicit commitments
- ✅ Returns prioritized list with:
  - Assignee
  - Deadline
  - Priority level (🔴 High, 🟡 Medium, 🟢 Low)
  - Context

**What you'll see**:
```markdown
## Action Items Extracted

### High Priority 🔴
- [ ] **Review Bob's PR #142** - @Alice Developer - Due: EOD today
  > Context: Auth bug fix ready for review

### Medium Priority 🟡
- [ ] **Update README** - @Bob Engineer - Due: Before merge
  > Context: Documentation needs updating
- [ ] **Schedule feature planning** - @Carol PM - Due: This week
  > Context: Deep dive on Thursday 2pm

### Summary
Total: 7 items | Completed: 4 (58%) | High priority: 2
```

---

### Test 4: Chain All WhatsApp Skills

**Copy this prompt**:
```
Parse the sample WhatsApp chat, summarize it, and extract all action items
```

**Expected outcome**:
- ✅ Claude automatically chains 3 skills:
  1. `whatsapp-parser` → structured data
  2. `whatsapp-summarizer` → conversation overview
  3. `whatsapp-action-extractor` → actionable tasks
- ✅ Provides comprehensive analysis in one go

**What you'll see**: Combined output from all three skills above.

---

## Part 2: RAG Backend Skills

### Test 5: Set Up FastAPI RAG Backend

**Copy this prompt**:
```
Set up a FastAPI backend for my new AI agent project using launch-rag
```

**Expected outcome**:
- ✅ Claude reads [skills/rag-setup/skill.md](skills/rag-setup/skill.md)
- ✅ Asks which repo: launch-rag (basic) or launch-agentic-rag (advanced)
- ✅ Clones the selected repository as `fastapi-project/`
- ✅ Creates Python virtual environment
- ✅ Installs all dependencies from requirements.txt
- ✅ Copies `.env.example` to `.env`
- ✅ Reminds you to:
  - Add OpenAI API key to .env
  - Run `rag-database` skill next for Supabase setup

**What you'll see**:
```bash
✅ Cloned launch-rag to fastapi-project/
✅ Created virtual environment: fastapi-project/venv
✅ Installed dependencies
✅ Created .env from .env.example

⚠️ Next steps:
1. Add your OpenAI API key to fastapi-project/.env
2. Run the rag-database skill to set up Supabase
3. Start server: cd fastapi-project && source venv/bin/activate && uvicorn main:app --reload
```

---

### Test 6: Configure Supabase Database

**Copy this prompt**:
```
Set up Supabase with pgvector for my RAG application. Project name: demo-agent-skills-rag
```

**Expected outcome**:
- ✅ Claude reads [skills/rag-database/skill.md](skills/rag-database/skill.md)
- ✅ Checks if Supabase CLI is installed
- ✅ Uses CLI automation (Option A):
  1. Generates secure database password (hidden)
  2. Creates Supabase project in YouTube organization
  3. Waits 2 minutes for initialization
  4. Retrieves API keys using table parsing (not JSON)
  5. Updates `.env` with Supabase credentials
  6. Runs SQL migrations from `sql/init_supabase.sql`
  7. Verifies database connection
- ✅ Detects if ANTHROPIC_API_KEY is placeholder
- ✅ Auto-switches to `AI_PROVIDER=openai` if needed

**What you'll see**:
```bash
✅ Generated secure database password (saved to .env)
✅ Creating Supabase project: demo-agent-skills-rag
⏳ Waiting 2 minutes for project initialization...
✅ Project created: https://bidnimhlhdjqsfqewkbd.supabase.co
✅ Retrieved API keys (masked for security)
✅ Updated .env with Supabase credentials
✅ Running SQL migrations...
✅ Database initialized with pgvector extension
✅ Created rag_chunks table with vector(1536) column
✅ Set up Row Level Security policies

🎉 Supabase setup complete! Your RAG backend is ready.

Test it: cd fastapi-project && source venv/bin/activate && uvicorn main:app --reload
Visit: http://localhost:8000/docs
```

---

### Test 7: Add Agent Tools (Optional - Agentic RAG Only)

**Copy this prompt**:
```
Set up Google Calendar and Gmail tools for my agentic RAG agent
```

**Expected outcome**:
- ✅ Claude reads [skills/rag-tools/skill.md](skills/rag-tools/skill.md)
- ✅ Verifies you're using launch-agentic-rag (not launch-rag)
- ✅ Provides step-by-step guidance for:
  1. Creating Google Cloud project
  2. Enabling Calendar & Gmail APIs
  3. Creating service account
  4. Downloading credentials JSON
  5. Saving to `tools/google-service-account.json`
  6. Granting domain-wide delegation (if needed)

**What you'll see**:
```markdown
🔧 Setting up Google Calendar & Gmail Tools

This skill requires manual setup via Google Cloud Console.
Follow these steps:

### 1. Create Google Cloud Project
Visit: https://console.cloud.google.com/projectcreate
- Project name: agent-rag-tools
- Organization: (optional)

### 2. Enable APIs
Visit: https://console.cloud.google.com/apis/library
Enable:
- ✅ Google Calendar API
- ✅ Gmail API

### 3. Create Service Account
... [detailed instructions]

✅ Once completed, your agent will have access to Calendar and Gmail!
```

---

## Verification Checklist

After running the skills, verify:

### WhatsApp Skills ✅
- [ ] Parsed JSON has correct message count
- [ ] Summary includes TL;DR and key topics
- [ ] Action items show assignees and deadlines
- [ ] Skills can be chained together

### RAG Backend Skills ✅
- [ ] `fastapi-project/` directory created
- [ ] Virtual environment activated
- [ ] Dependencies installed without errors
- [ ] `.env` file has all required variables
- [ ] Supabase project created and accessible
- [ ] Database has `rag_chunks` table with vector column
- [ ] Health check works: `curl http://localhost:8000/healthz`
- [ ] API docs visible: `http://localhost:8000/docs`
- [ ] Can seed documents: POST to `/seed`
- [ ] Can query RAG: POST to `/chat` with a question

---

## Troubleshooting

### Issue: "Skill not found"
**Solution**: Check that CLAUDE.md is in the root directory and contains skill paths.

### Issue: "Import errors when running FastAPI"
**Solution**: Activate virtual environment first:
```bash
cd fastapi-project
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows
```

### Issue: "401 authentication error from Anthropic"
**Solution**:
1. Check if `ANTHROPIC_API_KEY` in .env is a placeholder
2. Either add real Anthropic key OR set `AI_PROVIDER=openai`
3. OpenAI key is REQUIRED for embeddings regardless of provider

### Issue: "Supabase project creation fails"
**Solution**:
1. Check Supabase CLI is logged in: `supabase login`
2. Verify organization exists: `supabase orgs list`
3. If CLI automation fails, use Manual Setup (Option B) in the skill

### Issue: "Vector search returns no results"
**Solution**:
1. Seed the database first: POST to `http://localhost:8000/seed`
2. Verify embeddings were created: Check Supabase table editor
3. Check that `OPENAI_API_KEY` is valid

---

## Advanced Testing

### Test Skill Chaining with Custom Data

1. **Export your own WhatsApp chat** (Settings → More → Export chat)
2. Save to `examples/my-chat.txt`
3. Run: `Parse, summarize, and extract actions from examples/my-chat.txt`

### Test RAG Backend with Real Documents

1. **After setup is complete**, add your own documents
2. Modify `fastapi-project/data/sample_documents.json`
3. POST to `/seed` to ingest
4. POST to `/chat` to query

### Create Your Own Skills

See [docs/skill-anatomy.md](docs/skill-anatomy.md) for detailed guide on creating custom skills.

---

## Questions or Issues?

- **GitHub Issues**: [launch-agent-skills/issues](https://github.com/ShenSeanChen/launch-agent-skills/issues)
- **Discord Community**: [Join here](https://discord.com/invite/TKKPzZheua)
- **YouTube**: [@SeanAIStories](https://youtube.com/@SeanAIStories)

---

**Happy skill testing!** 🚀
