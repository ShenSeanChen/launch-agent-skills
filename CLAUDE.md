# Directory: launch-agent-skills/CLAUDE.md
# Claude Code Project Instructions

This repository demonstrates Agent Skills for Claude Code. Use this as a learning resource and reference implementation.

## Project Overview

This is a tutorial repository for learning Agent Skills. It contains:
- `skills/` - Reusable skill definitions
- `examples/` - Sample data for testing skills
- `scripts/` - Helper scripts that skills can reference

## Available Skills

### WhatsApp Skills (Video 1)
- `skills/whatsapp-parser/skill.md` - Parse WhatsApp chat exports
- `skills/chat-summarizer/skill.md` - Summarize conversations
- `skills/action-extractor/skill.md` - Extract TODOs and action items

### Project Setup Skills (Video 2)
- `skills/fastapi-setup/skill.md` - FastAPI project scaffolding
- `skills/supabase-setup/skill.md` - Supabase database setup

## How to Use Skills

When the user asks about:
- WhatsApp, chat parsing, messages → load `whatsapp-parser` skill
- Summaries, conversation overview → load `chat-summarizer` skill
- TODOs, action items, follow-ups → load `action-extractor` skill
- FastAPI, API setup, project structure → load `fastapi-setup` skill
- Supabase, database, vector DB → load `supabase-setup` skill

## Code Standards

- Use Google-style docstrings for Python
- Add file directory comments at the top of each file
- Keep code clean and well-commented
- Follow existing patterns in the codebase
