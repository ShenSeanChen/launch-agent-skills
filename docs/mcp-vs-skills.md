# Directory: launch-agent-skills/docs/mcp-vs-skills.md
# MCP vs Skills: Understanding the Difference

This document clarifies the distinction between MCP (Model Context Protocol) and Agent Skills.

## Quick Comparison

| Aspect | MCP | Skills |
|--------|-----|--------|
| **Purpose** | Connect to data/tools | Teach how to use data |
| **Analogy** | API/Database connection | Playbook/Instructions |
| **Provides** | Access | Knowledge |
| **Example** | "Access the file system" | "Parse WhatsApp format this way" |

## MCP: Connecting Claude to Data

**MCP (Model Context Protocol)** provides Claude with access to external systems:

- File systems (read/write files)
- Databases (query Supabase, PostgreSQL)
- APIs (Stripe, GitHub, etc.)
- Services (send emails, schedule meetings)

### MCP Example: File Access

```json
{
  "mcpServers": {
    "files": {
      "command": "python",
      "args": ["-m", "mcp_files"]
    }
  }
}
```

This gives Claude the **ability** to read files, but not the **knowledge** of how to interpret them.

## Skills: Teaching Claude What To Do

**Skills** teach Claude domain-specific knowledge:

- File formats and parsing rules
- Best practices and patterns
- Step-by-step workflows
- Edge case handling

### Skill Example: WhatsApp Parsing

```markdown
---
name: WhatsApp Parser
triggers: [whatsapp, chat export]
---

WhatsApp exports follow this format:
[DD/MM/YYYY, HH:MM:SS] Sender: Message

Parse by:
1. Extract timestamp with regex
2. Identify sender before colon
3. Handle multi-line messages
...
```

This gives Claude the **knowledge** to interpret WhatsApp files, regardless of how it accesses them.

## How They Work Together

```
┌─────────────────────────────────────────────────────────────┐
│                    THE COMPLETE PICTURE                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   User: "Parse my WhatsApp chat and find action items"      │
│                          │                                  │
│                          ▼                                  │
│   ┌──────────────────────────────────────────┐             │
│   │             Claude's Brain               │              │
│   │                                          │              │
│   │  ┌──────────────┐    ┌──────────────┐   │              │
│   │  │    Skills    │    │     MCP      │   │              │
│   │  │   (HOW to)   │    │ (ACCESS to)  │   │              │
│   │  │              │    │              │   │              │
│   │  │ - Parse fmt  │    │ - Read file  │   │              │
│   │  │ - Find TODOs │    │ - Write JSON │   │              │
│   │  │ - Summarize  │    │ - Call APIs  │   │              │
│   │  └──────────────┘    └──────────────┘   │              │
│   │                                          │              │
│   └──────────────────────────────────────────┘             │
│                          │                                  │
│                          ▼                                  │
│            Structured output with action items              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Real-World Analogy

**MCP** is like giving someone:
- A key to the library
- Access to a database
- Login credentials

**Skills** are like giving someone:
- Knowledge of the Dewey Decimal System
- Understanding of SQL query optimization
- Training on the software

You need **both** to be effective:
- MCP without Skills = Access but confusion
- Skills without MCP = Knowledge but no access

## When to Use What

### Use MCP When:
- You need Claude to access external data
- Connecting to APIs or databases
- Enabling actions (send email, create PR)
- Reading/writing files on disk

### Use Skills When:
- Teaching domain-specific knowledge
- Defining parsing rules or formats
- Establishing workflows and patterns
- Handling edge cases

### Use Both When:
- Building complete solutions
- Claude needs both access AND knowledge
- Creating reusable, intelligent agents

## Example: Complete RAG System

**MCP Components:**
- Supabase MCP (database access)
- File system MCP (document ingestion)

**Skill Components:**
- Document chunking skill (how to split documents)
- Embedding skill (what model to use, dimensions)
- Query skill (how to search and rank results)

Together, they create an intelligent RAG agent that:
1. **Accesses** documents (MCP)
2. **Knows how to** chunk them (Skill)
3. **Stores** in Supabase (MCP)
4. **Retrieves** intelligently (Skill + MCP)

## Summary

| Question | MCP Answers | Skills Answer |
|----------|-------------|---------------|
| Can I read files? | ✅ Yes | — |
| How do I parse WhatsApp? | — | ✅ This way |
| Can I query Supabase? | ✅ Yes | — |
| How do I structure the schema? | — | ✅ Best practices |
| Can I send emails? | ✅ Yes | — |
| What should the email say? | — | ✅ Templates |

**Remember**: MCP = Capability, Skills = Knowledge. Use both for powerful AI agents.
