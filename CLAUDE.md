# Directory: launch-agent-skills/CLAUDE.md
# Claude Code Project Instructions

This repository demonstrates Agent Skills for Claude Code. Use this as a learning resource and reference implementation.

## Project Overview

This is a tutorial repository for learning Agent Skills. It contains:
- `skills/` - Reusable skill definitions
- `examples/` - Sample data for testing skills
- `scripts/` - Helper scripts that skills can reference

## Available Skills

### WhatsApp Skills
- `skills/whatsapp-parser/skill.md` - Parse WhatsApp chat exports
- `skills/whatsapp-summarizer/skill.md` - Summarize conversations
- `skills/whatsapp-action-extractor/skill.md` - Extract TODOs and action items

### RAG Setup Skills
- `skills/rag-setup/skill.md` - FastAPI RAG project setup (launch-rag or launch-agentic-rag)
- `skills/rag-database/skill.md` - Supabase + pgvector database setup
- `skills/rag-tools/skill.md` - Google Calendar/Gmail tools (agentic-rag only)

## How to Use Skills

When the user asks about:
- WhatsApp, chat parsing, messages → load `whatsapp-parser` skill
- Summaries, conversation overview → load `whatsapp-summarizer` skill
- TODOs, action items, follow-ups → load `whatsapp-action-extractor` skill
- FastAPI, RAG, API setup, launch-rag, launch-agentic-rag → load `rag-setup` skill
- Supabase, database, vector DB, pgvector → load `rag-database` skill
- Google Calendar, Gmail, agent tools → load `rag-tools` skill

## Code Standards

- Use Google-style docstrings for Python
- Add file directory comments at the top of each file
- Keep code clean and well-commented
- Follow existing patterns in the codebase
