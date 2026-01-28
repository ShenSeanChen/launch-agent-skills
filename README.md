# Directory: launch-agent-skills/README.md
# Launch Agent Skills

> **Learn Agent Skills, Claude Skills & Subagents with Real Examples**

This repository accompanies a two-part YouTube tutorial series showing you how to create and use Agent Skills in Claude Code.

📹 **Video 1**: [Agent Skills Explained - WhatsApp Analyzer Demo](#) _(coming soon)_  
📹 **Video 2**: [Build a Project Wizard with Subagents](#) _(coming soon)_

🚀 **X Post**: [Link](#)  
💻 **Related Repos**: [launch-rag](https://github.com/ShenSeanChen/launch-rag) | [launch-agentic-rag](https://github.com/ShenSeanChen/launch-agentic-rag) | [launch-mcp-demo](https://github.com/ShenSeanChen/launch-mcp-demo)  
☕️ **Buy me a coffee**: [Cafe Latte](#)  
🤖 **Discord**: [Join our community](#)

---

## What Are Agent Skills?

**Skills** are reusable instructions that teach Claude how to perform specific tasks. Instead of explaining the same thing every time, you define a skill once and Claude references it whenever relevant.

```
┌─────────────────────────────────────────────────────────────┐
│                    SKILLS vs MCP                            │
├─────────────────────────────────────────────────────────────┤
│  MCP = CONNECTS Claude to data        Skills = TEACHES      │
│  (APIs, databases, files)             Claude what to DO     │
├─────────────────────────────────────────────────────────────┤
│  Example: MCP gives Claude access     Example: Skill tells  │
│  to your WhatsApp chat files          Claude HOW to parse   │
│                                       the WhatsApp format   │
└─────────────────────────────────────────────────────────────┘
```

### Skill Anatomy (Progressive Disclosure)

| Component | When Loaded | Purpose |
|-----------|-------------|---------|
| **Metadata** | Always | Name, description, triggers |
| **Body** | On demand | Detailed instructions |
| **Resources** | Referenced | Scripts, templates |

---

## Repository Structure

```
launch-agent-skills/
├── CLAUDE.md                    # Claude Code project instructions
├── README.md                    # This file
│
├── skills/                      # 🎯 Agent Skills (the main content)
│   ├── whatsapp-parser/         # Video 1: WhatsApp skills
│   │   └── skill.md
│   ├── chat-summarizer/
│   │   └── skill.md
│   ├── action-extractor/
│   │   └── skill.md
│   ├── fastapi-setup/           # Video 2: Project setup skills
│   │   └── skill.md
│   └── supabase-setup/
│       └── skill.md
│
├── examples/                    # Sample data for demos
│   ├── sample-whatsapp-chat.txt
│   └── expected-output.json
│
├── scripts/                     # Helper scripts (skill resources)
│   └── parse_whatsapp.py
│
└── docs/                        # Additional documentation
    ├── skill-anatomy.md
    └── mcp-vs-skills.md
```

---

## Video 1: WhatsApp Analyzer (Agent Skills Intro)

**Goal**: Understand what Skills are and create your first useful skill.

### Skills Covered:

1. **WhatsApp Parser Skill** - Parse WhatsApp export format into structured data
2. **Chat Summarizer Skill** - Generate conversation summaries
3. **Action Extractor Skill** - Find TODOs, commitments, and follow-ups

### Quick Start:

```bash
# Clone the repo
git clone https://github.com/ShenSeanChen/launch-agent-skills.git
cd launch-agent-skills

# Open in Claude Code
claude .

# Try the WhatsApp parser skill
# In Claude Code, say: "Parse the sample WhatsApp chat in examples/"
```

---

## Video 2: FastAPI + Supabase Project Wizard (Subagents)

**Goal**: See how Skills combine with Subagents for complex tasks.

### Skills Covered:

1. **FastAPI Setup Skill** - Project structure, routing, best practices
2. **Supabase Setup Skill** - Database schema, pgvector, RLS policies

### Subagent Architecture:

```
Main Agent (Project Wizard)
    │
    ├── Database Subagent
    │       └── Uses: "Supabase Setup Skill"
    │
    └── API Subagent
            └── Uses: "FastAPI Setup Skill"
```

---

## How to Use Skills in Claude Code

### 1. Reference a Skill Directly

```
You: "Use the whatsapp-parser skill to parse this chat"
Claude: *loads skill* *follows instructions*
```

### 2. Let Claude Auto-Discover

```
You: "Parse my WhatsApp export"
Claude: *recognizes trigger words* *loads relevant skill*
```

### 3. Chain Multiple Skills

```
You: "Parse the chat, summarize it, and extract action items"
Claude: *loads 3 skills* *executes in sequence*
```

---

## Creating Your Own Skills

### Skill File Template

```markdown
---
name: Your Skill Name
description: One-line description
triggers:
  - keyword1
  - keyword2
---

# Skill Title

## Purpose
What this skill accomplishes.

## Instructions
Step-by-step guide for Claude.

## Example
Input/output example.
```

### Best Practices

1. **Be Specific** - Vague instructions = vague results
2. **Include Examples** - Show don't tell
3. **Define Edge Cases** - What should Claude do when X happens?
4. **Keep It Focused** - One skill = one capability

---

## Related Concepts

| Concept | What It Does | Example |
|---------|--------------|---------|
| **Skills** | Teaches Claude HOW | "Parse WhatsApp format this way" |
| **MCP** | Connects Claude to data | "Access the file system" |
| **Subagents** | Parallelizes work | "Spawn a research agent" |
| **Rules** | Enforces constraints | "Always use TypeScript" |

---

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/new-skill`)
3. Add your skill to `skills/`
4. Submit a Pull Request

---

## Social & Connect

- **YouTube**: [@SeanAIStories](https://youtube.com/@SeanAIStories)
- **Twitter/X**: [@ShenSeanChen](https://twitter.com/ShenSeanChen)
- **LinkedIn**: [in/shen-sean-chen](https://linkedin.com/in/shen-sean-chen)
- **Discord**: [Join our community](#)
- **GitHub**: [@ShenSeanChen](https://github.com/ShenSeanChen)

---

## License

MIT License - see [LICENSE](LICENSE) for details.

---

**Built with ❤️ for the developer community**

_This project demonstrates how to leverage Agent Skills to make AI assistants more capable and consistent._
