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

This tutorial walks you through **Claude Skills** - a way to teach Claude reusable knowledge so you don't have to explain the same thing over and over.

### The Problem
Every time you want Claude to do something specific (like parse a WhatsApp export), you have to explain the format, the edge cases, and the expected output. That's tedious.

### The Solution: Skills
Define the knowledge **once** in a `skill.md` file, and Claude references it whenever needed.

### What We'll Build
A **WhatsApp Chat Analyzer** that:
1. **Parses** WhatsApp export files into structured JSON
2. **Summarizes** conversations with key topics and decisions  
3. **Extracts** action items, TODOs, and follow-ups

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
├── CLAUDE.md                    # Project instructions for Claude Code
├── README.md                    # This file
│
├── skills/                      # 🎯 The Skills (main content)
│   ├── whatsapp-parser/
│   │   └── skill.md            # Parse WhatsApp exports
│   ├── chat-summarizer/
│   │   └── skill.md            # Generate summaries
│   ├── action-extractor/
│   │   └── skill.md            # Find TODOs & action items
│   ├── fastapi-setup/
│   │   └── skill.md            # FastAPI project scaffolding
│   └── supabase-setup/
│       └── skill.md            # Supabase + pgvector setup
│
├── examples/                    # Test data
│   ├── sample-whatsapp-chat.txt # Synthetic WhatsApp conversation
│   └── expected-output.json     # Reference output
│
├── scripts/
│   └── parse_whatsapp.py        # Standalone parser (skill resource)
│
└── docs/
    ├── skill-anatomy.md         # Deep dive on skill structure
    └── mcp-vs-skills.md         # MCP vs Skills comparison
```

---

## 🧪 Testing the Skills

### Prerequisites

- [Claude Code](https://claude.ai/code) installed (`npm install -g @anthropic-ai/claude-code`)
- Or Claude Pro/Max subscription with Claude Code access

### Quick Start

```bash
# Clone the repo
git clone https://github.com/ShenSeanChen/launch-agent-skills.git
cd launch-agent-skills

# Open in Claude Code
claude .
```

### Sample Test Prompts

Try these prompts in Claude Code to test the skills:

#### 1. Test WhatsApp Parser Skill
```
Parse the WhatsApp chat in examples/sample-whatsapp-chat.txt
```

**Expected**: Claude reads the skill, parses the file, returns structured JSON with participants, message count, and messages array.

#### 2. Test Chat Summarizer Skill
```
Summarize the WhatsApp chat in examples/sample-whatsapp-chat.txt
```

**Expected**: Executive summary, key topics discussed, decisions made, participant stats.

#### 3. Test Action Extractor Skill
```
Extract all action items and TODOs from examples/sample-whatsapp-chat.txt
```

**Expected**: List of action items with assignees, deadlines, and priority levels.

#### 4. Test Skill Chaining
```
Parse the sample WhatsApp chat, summarize it, and extract all action items
```

**Expected**: Claude uses all 3 skills in sequence, providing comprehensive analysis.

#### 5. Test FastAPI Setup Skill
```
Use the fastapi-setup skill to create a new project structure for a REST API
```

**Expected**: Claude generates folder structure, main.py, config files following the skill's patterns.

#### 6. Test Supabase Setup Skill
```
Show me how to set up Supabase with pgvector for a RAG application
```

**Expected**: SQL initialization script, Python client code, environment variables.

### Sample Data Explanation

The `examples/sample-whatsapp-chat.txt` contains a **synthetic conversation** (no real data) between:
- **Alice Developer** - Frontend engineer
- **Bob Engineer** - Backend engineer  
- **Carol PM** - Project manager

The conversation includes:
- Sprint planning discussion
- Bug fix and PR workflow (PR #142)
- Feature planning meeting
- Decisions: FastAPI + Supabase for new microservice
- Multiple TODOs and action items
- Emojis, media placeholders, and multi-message threads

This gives you realistic patterns to test all skills without any privacy concerns.

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
