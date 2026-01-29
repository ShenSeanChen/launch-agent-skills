# Directory: launch-agent-skills/README.md
# Launch Agent Skills

> **Learn Claude Skills: Teach AI to Follow Your Playbooks**

📹 **YouTube Tutorial**: [Agent Skills Explained with Real Examples](#) _(link coming soon)_

🚀 **X Post**: [Link](#)  
💻 **Related Repos**: [launch-rag](https://github.com/ShenSeanChen/launch-rag) | [launch-agentic-rag](https://github.com/ShenSeanChen/launch-agentic-rag) | [launch-mcp-demo](https://github.com/ShenSeanChen/launch-mcp-demo)  
☕️ **Buy me a coffee**: [Cafe Latte](https://buy.stripe.com/5kA176bA895ggog4gh)  
🤖 **Discord**: [Join our community](https://discord.com/invite/TKKPzZheua)

---

## 🎬 Video Story: What You'll Learn

This tutorial teaches you **Claude Skills** - a way to create reusable AI playbooks so you never have to re-explain the same instructions again.

### The Journey

**Part 1: The Problem (WhatsApp Example)**
You export a WhatsApp chat and want to:
- Parse it into structured data
- Get a summary of key decisions
- Extract all action items

Without skills, you'd need to explain the format, edge cases, and expected output every single time.

**Part 2: The Solution (Skills)**
Define the knowledge **once** in `skill.md` files, and Claude references them whenever needed.

We'll build:
1. **WhatsApp Parser** - Extract messages into structured JSON
2. **Chat Summarizer** - Generate executive summaries with key topics
3. **Action Extractor** - Find all TODOs and action items

**Part 3: Real-World Application (RAG Backend)**
Then we'll use skills to set up a production-ready FastAPI backend:
- **RAG Setup Skill** - Clone and configure [launch-rag](https://github.com/ShenSeanChen/launch-rag) or [launch-agentic-rag](https://github.com/ShenSeanChen/launch-agentic-rag)
- **Database Skill** - Set up Supabase with pgvector for vector search
- **Tools Skill** - (Optional) Add Google Calendar/Gmail integration

From simple chat parsing to full AI backend - all using the same skill pattern.

---

## 🧠 Core Concepts

### What Are Skills?

**Skills** are markdown files that teach Claude domain-specific knowledge. They follow a "progressive disclosure" pattern:

| Component | When Loaded | Purpose |
|-----------|-------------|---------|
| **Metadata** | Always | Name, description, trigger keywords |
| **Body** | On demand | Detailed instructions, step-by-step guide |
| **Resources** | Referenced | Scripts, templates, examples |

### Skills vs MCP vs Subagents

| Concept | What It Does | Analogy |
|---------|--------------|---------|
| **Skills** | Teaches Claude HOW to do something | A playbook or recipe |
| **MCP** | Connects Claude to external data/tools | A key to the library |
| **Subagents** | Spawns specialized workers for subtasks | A team of specialists |

**Key insight**: 
- MCP = **Access** (can I read this file?)
- Skills = **Knowledge** (how do I parse this format?)
- Subagents = **Orchestration** (who handles what part?)

> 💡 **Note**: This tutorial focuses on **Skills**. Subagents are typically implemented at the framework level (LangGraph, CrewAI) or through Claude's natural task decomposition. Skills provide the "playbooks" that any agent (main or sub) can use.

---

## 📁 Repository Structure

```
launch-agent-skills/
├── CLAUDE.md                          # Project instructions for Claude Code
├── README.md                          # This file
│
├── skills/                            # 🎯 The Skills (main content)
│   │
│   ├── whatsapp-parser/               # Part 1: WhatsApp Skills
│   │   └── skill.md                   # Parse WhatsApp chat exports
│   ├── whatsapp-summarizer/
│   │   └── skill.md                   # Summarize conversations
│   ├── whatsapp-action-extractor/
│   │   └── skill.md                   # Extract TODOs and action items
│   │
│   ├── rag-setup/                     # Part 2: RAG Backend Skills
│   │   └── skill.md                   # FastAPI project setup (launch-rag/agentic-rag)
│   ├── rag-database/
│   │   └── skill.md                   # Supabase + pgvector setup
│   └── rag-tools/
│       └── skill.md                   # Google Calendar/Gmail (optional)
│
├── examples/                          # Test data
│   ├── sample-whatsapp-chat.txt       # Synthetic WhatsApp conversation
│   └── expected-output.json           # Reference output
│
├── scripts/
│   ├── export_to_google_docs.py       # Export analysis to Google Docs
│   ├── requirements.txt               # Script dependencies
│   └── README.md                      # Script setup and usage
│
└── docs/
    ├── skill-anatomy.md               # Deep dive on skill structure
    └── mcp-vs-skills.md               # MCP vs Skills comparison
```

---

## 🧪 Testing the Skills

**📋 See [TESTING.md](TESTING.md) for detailed step-by-step testing guide with exact prompts and expected outcomes.**

### Quick Start

```bash
# Clone the repo
git clone https://github.com/ShenSeanChen/launch-agent-skills.git
cd launch-agent-skills

# Open in Claude Code
claude .
```

### Sample Test Prompts

Try these prompts in Claude Code:

#### Part 1: WhatsApp Skills

**1. Parse WhatsApp Export**
```
Parse the WhatsApp chat in examples/sample-whatsapp-chat.txt
```
Expected: Structured JSON with participants, message count, and messages array.

**2. Summarize Conversation**
```
Summarize the WhatsApp chat in examples/sample-whatsapp-chat.txt
```
Expected: Executive summary, key topics discussed, decisions made, participant stats.

**3. Extract Action Items**
```
Extract all action items and TODOs from examples/sample-whatsapp-chat.txt
```
Expected: List of action items with assignees, deadlines, and priority levels.

**4. Chain All WhatsApp Skills**
```
Parse the sample WhatsApp chat, summarize it, and extract all action items
```
Expected: Claude uses all 3 skills in sequence for comprehensive analysis.

#### Part 2: RAG Backend Skills

**5. Set Up FastAPI RAG Backend**
```
Set up a FastAPI backend for my new AI agent project using launch-rag
```
Expected: Claude clones repo, sets up environment, installs dependencies, configures .env.

**6. Configure Supabase Database**
```
Set up Supabase with pgvector for my RAG application
```
Expected: Automated CLI setup with project creation, API keys, SQL migrations.

**7. Add Agent Tools (Optional)**
```
Set up Google Calendar and Gmail tools for my agentic RAG agent
```
Expected: Service account setup, API enablement, credentials configuration.

### Sample Data Explanation

The `examples/sample-whatsapp-chat.txt` contains a **synthetic B2B sales conversation** (no real data) between:
- **Marcus Chen** - Sales rep at DataFlow Analytics (SaaS analytics platform)
- **Jennifer Wu** - Buyer at TechRetail (VP of Sales, potential customer)

The conversation includes:
- **Prospecting** - LinkedIn connection, discovery of pain points
- **Needs analysis** - Scaling from 12→40 reps, forecast accuracy problems
- **Solution pitch** - Real-time analytics, AI forecasting ($3,500/month)
- **Multi-threading** - Looping in Raj (Head of Sales Ops) for technical buy-in
- **Demo scheduling** - Thursday 2pm PST with specific requirements
- **Objection handling** - Security concerns (SOC 2, GDPR compliance)
- **Trial close** - 30-day trial, board meeting alignment (Feb 20th)
- **Expansion discovery** - Additional needs uncovered (SDR tracking)
- Multiple action items: prepare security docs, custom demo, trial setup

**Perfect for automanus.io use cases:**
- B2B sales teams managing deals over WhatsApp
- Sales conversation tracking and action item extraction
- Multi-stakeholder coordination and next steps
- Discovery question analysis and pain point identification
- Demo/meeting scheduling and follow-up tracking
- Deal progression and timeline management

This gives you realistic B2B sales patterns to test all skills without any privacy concerns!

---

## 🤖 AI + Automation: How It Works Together

**Claude (AI Skills)** handles the smart stuff:
- 🧠 Parsing WhatsApp chats with context understanding
- 💡 Extracting action items intelligently (not just regex)
- 📊 Summarizing with business insights
- 🎯 Identifying decision makers and buying signals
- 🔍 Detecting sentiment and deal risk

**Scripts (Automation)** handle the integration:
- 📄 Exporting to Google Docs, Notion, PDFs
- 🔗 Syncing to CRMs (Salesforce, HubSpot)
- 📅 Creating calendar reminders
- 💬 Posting to Slack/Teams
- 🔄 Batch processing and workflows

**Example workflow:**
```bash
# 1. Ask Claude to analyze (AI does the thinking)
"Analyze examples/sample-whatsapp-chat.txt and save as JSON"

# 2. Export to Google Docs (automation distributes results)
python scripts/export_to_google_docs.py examples/chat_analysis.json

# 3. Share with team
# Google Doc link → ready to collaborate!
```

See [scripts/README.md](scripts/README.md) for setup instructions.

---

## 📝 Skill File Anatomy

Every skill follows this structure:

```markdown
---
name: Skill Name
description: One-line description
triggers:
  - keyword1
  - keyword2
---

# Skill Title

## Purpose
What this skill accomplishes.

## Instructions
Step-by-step guide for Claude to follow.

## Example
Input/output examples.

## Edge Cases
How to handle unusual situations.

## Related Skills
Links to complementary skills.
```

### How Claude Discovers Skills

1. **Trigger keywords** in metadata match user query
2. **CLAUDE.md** project file tells Claude which skills exist
3. Claude loads the relevant skill body on demand
4. If multiple skills apply, Claude chains them

---

## 🎨 Visual Guide (Diagram Ideas)

_Use these ASCII diagrams as references for creating Excalidraw visuals._

### Diagram 1: Skills Progressive Disclosure

Shows how Claude loads skill components on-demand:

```
┌─────────────────────────────────────────────────────────────┐
│                    Progressive Disclosure                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   ┌─────────────────┐                                       │
│   │    METADATA     │ ◄── Always loaded (lightweight)       │
│   │   - name        │     Claude scans these to find        │
│   │   - description │     relevant skills                   │
│   │   - triggers    │                                       │
│   └────────┬────────┘                                       │
│            │                                                │
│            ▼  (user query matches trigger keyword)          │
│   ┌─────────────────┐                                       │
│   │      BODY       │ ◄── Loaded on demand (detailed)       │
│   │  - instructions │     Full step-by-step guide           │
│   │  - examples     │     loaded only when needed           │
│   │  - edge cases   │                                       │
│   └────────┬────────┘                                       │
│            │                                                │
│            ▼  (if implementation needed)                    │
│   ┌─────────────────┐                                       │
│   │    RESOURCES    │ ◄── Referenced (external files)       │
│   │  - scripts      │     Helper code, templates            │
│   │  - templates    │     loaded as needed                  │
│   └─────────────────┘                                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Diagram 2: MCP vs Skills vs Subagents

Visual comparison showing what each concept provides:

```
┌─────────────────────────────────────────────────────────────┐
│               MCP vs Skills vs Subagents                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐   │
│  │      MCP      │  │    SKILLS     │  │   SUBAGENTS   │   │
│  │   (ACCESS)    │  │  (KNOWLEDGE)  │  │   (WORKERS)   │   │
│  ├───────────────┤  ├───────────────┤  ├───────────────┤   │
│  │               │  │               │  │               │   │
│  │  "Can I read  │  │  "How do I    │  │  "Who does    │   │
│  │  this file?"  │  │  parse it?"   │  │  what task?"  │   │
│  │               │  │               │  │               │   │
│  ├───────────────┤  ├───────────────┤  ├───────────────┤   │
│  │ • File system │  │ • skill.md    │  │ • LangGraph   │   │
│  │ • Supabase    │  │   files       │  │ • CrewAI      │   │
│  │ • Stripe API  │  │ • Domain      │  │ • Claude task │   │
│  │ • GitHub      │  │   knowledge   │  │   breakdown   │   │
│  │ • Notion      │  │ • Playbooks   │  │               │   │
│  └───────┬───────┘  └───────┬───────┘  └───────┬───────┘   │
│          │                  │                  │           │
│          └──────────────────┼──────────────────┘           │
│                             │                              │
│                      ┌──────▼──────┐                       │
│                      │   POWERFUL  │                       │
│                      │    AGENT    │                       │
│                      │             │                       │
│                      │ Access +    │                       │
│                      │ Knowledge + │                       │
│                      │ Workers     │                       │
│                      └─────────────┘                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Diagram 3: WhatsApp Analyzer Skill Chaining

Shows how multiple skills work together:

```
┌─────────────────────────────────────────────────────────────┐
│            WhatsApp Analyzer - Skill Chaining                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌───────────┐                                              │
│  │   User    │  "Parse, summarize, and extract actions      │
│  │   Query   │   from my WhatsApp chat"                     │
│  └─────┬─────┘                                              │
│        │                                                    │
│        ▼                                                    │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐       │
│  │  WhatsApp   │──▶│    Chat     │──▶│   Action    │       │
│  │   Parser    │   │ Summarizer  │   │  Extractor  │       │
│  │   Skill     │   │   Skill     │   │   Skill     │       │
│  └──────┬──────┘   └──────┬──────┘   └──────┬──────┘       │
│         │                 │                 │              │
│         ▼                 ▼                 ▼              │
│  ┌───────────┐     ┌───────────┐     ┌───────────┐        │
│  │  Parsed   │     │  Summary  │     │  Action   │        │
│  │   JSON    │     │  Report   │     │   Items   │        │
│  │           │     │           │     │           │        │
│  │ • 42 msgs │     │ • Topics  │     │ • 6 TODOs │        │
│  │ • 3 users │     │ • Decisions│    │ • 2 high  │        │
│  │ • 1 media │     │ • Sentiment│    │ • owners  │        │
│  └───────────┘     └───────────┘     └───────────┘        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Diagram 4: Skill File Structure

Simple breakdown of a skill.md file:

```
┌─────────────────────────────────────────────────────────────┐
│                     skill.md Structure                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  --- (YAML frontmatter) ─────────────────────┐              │
│  │  name: WhatsApp Parser                    │ METADATA     │
│  │  description: Parse chat exports          │ (always      │
│  │  triggers:                                │  loaded)     │
│  │    - whatsapp                             │              │
│  │    - chat export                          │              │
│  ---  ───────────────────────────────────────┘              │
│                                                             │
│  # WhatsApp Parser  ─────────────────────────┐              │
│                                              │              │
│  ## Purpose                                  │              │
│  Parse WhatsApp exports into JSON.           │ BODY         │
│                                              │ (loaded      │
│  ## Instructions                             │  on demand)  │
│  1. Read the file                            │              │
│  2. Parse with regex                         │              │
│  3. Extract metadata                         │              │
│                                              │              │
│  ## Example                                  │              │
│  Input: [28/01/2026, 09:15] Alice: Hi        │              │
│  Output: { "sender": "Alice", ... }          │              │
│                                              │              │
│  ## Edge Cases                               │              │
│  - Multi-line messages                       │              │
│  - Media placeholders                        │              │
│  ────────────────────────────────────────────┘              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Excalidraw Tips

When creating these in Excalidraw:
- Use **boxes with rounded corners** for components
- Use **arrows** to show flow/relationships  
- Use **color coding**: 
  - 🟢 Green for Skills
  - 🔵 Blue for MCP
  - 🟡 Yellow for User input
  - 🟣 Purple for Output
- Keep **text minimal** - diagrams should be glanceable
- Add **icons** where possible (📁 files, 🔧 tools, 👤 user)

---

## 🛠 Creating Your Own Skills

### Step 1: Create the folder
```bash
mkdir -p skills/my-skill
touch skills/my-skill/skill.md
```

### Step 2: Write the skill
```markdown
---
name: My Custom Skill
description: Does something specific
triggers:
  - my trigger
  - related keyword
---

# My Custom Skill

## Purpose
Explain what this skill does.

## Instructions
1. First, do this
2. Then, do that
3. Finally, return this format

## Example
Input: ...
Output: ...
```

### Step 3: Update CLAUDE.md
Add your skill to the project instructions so Claude knows it exists.

### Best Practices

| Do | Don't |
|----|-------|
| Be specific about formats | Leave instructions vague |
| Include input/output examples | Assume Claude will figure it out |
| Handle edge cases explicitly | Ignore error scenarios |
| One skill = one capability | Cram everything into one skill |

---

## 🔗 Related Resources

- **MCP Demo**: [launch-mcp-demo](https://github.com/ShenSeanChen/launch-mcp-demo) - Learn Model Context Protocol
- **RAG Tutorial**: [launch-rag](https://github.com/ShenSeanChen/launch-rag) - Build a RAG system with Supabase
- **Agentic RAG**: [launch-agentic-rag](https://github.com/ShenSeanChen/launch-agentic-rag) - Add tool calling to RAG

---

## 👤 Connect

- **YouTube**: [@SeanAIStories](https://youtube.com/@SeanAIStories)
- **Twitter/X**: [@ShenSeanChen](https://twitter.com/ShenSeanChen)
- **LinkedIn**: [in/shen-sean-chen](https://linkedin.com/in/shen-sean-chen)
- **Discord**: [Join our community](https://discord.com/invite/TKKPzZheua)
- **GitHub**: [@ShenSeanChen](https://github.com/ShenSeanChen)

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

**Built with ❤️ for the developer community**

_Define once, use forever. That's the power of Agent Skills._
