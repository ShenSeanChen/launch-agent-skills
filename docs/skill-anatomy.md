# Directory: launch-agent-skills/docs/skill-anatomy.md
# Anatomy of a Claude Skill

This document explains the structure and components of a Claude Code skill file.

## Skill File Structure

A skill file (`skill.md`) follows a progressive disclosure pattern:

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
Step-by-step guide for Claude.

## Example
Input/output example.
```

## Components Explained

### 1. Metadata (Always Loaded)

The YAML frontmatter at the top is **always loaded** by Claude. It tells Claude:
- What the skill is called
- What it does (briefly)
- When to use it (trigger keywords)

```yaml
---
name: WhatsApp Chat Parser
description: Parse WhatsApp chat exports into structured JSON
triggers:
  - whatsapp
  - chat export
  - parse chat
---
```

**Best Practices:**
- Keep `name` concise (2-4 words)
- Make `description` fit in one line
- Use 3-5 specific trigger keywords
- Triggers should be things users actually say

### 2. Body/Instructions (Loaded On Demand)

The main content is loaded **when Claude determines the skill is relevant**. This prevents overwhelming Claude's context with unused instructions.

**Sections to Include:**

| Section | Purpose |
|---------|---------|
| **Purpose** | Why this skill exists |
| **Instructions** | Step-by-step process |
| **Examples** | Input/output samples |
| **Edge Cases** | What to do in unusual situations |
| **Related Skills** | Links to complementary skills |

### 3. Resources (Referenced)

Skills can reference external files like scripts or templates:

```markdown
## Resources

See `scripts/parse_whatsapp.py` for the reference implementation.
```

Resources are only loaded when Claude needs to use them.

## Progressive Disclosure in Action

```
User: "Parse my WhatsApp chat"
         │
         ▼
┌─────────────────────────────────┐
│ 1. Claude scans skill METADATA  │
│    - Sees "whatsapp" trigger    │
│    - Matches user query         │
└─────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│ 2. Claude loads skill BODY      │
│    - Reads full instructions    │
│    - Understands the format     │
└─────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│ 3. Claude references RESOURCES  │
│    - May read helper script     │
│    - Uses as implementation ref │
└─────────────────────────────────┘
```

## Skill Design Principles

### 1. Be Specific
❌ Bad: "Parse data into something useful"
✅ Good: "Parse WhatsApp .txt exports into JSON with timestamp, sender, and content fields"

### 2. Include Examples
Show don't tell. Include concrete input/output examples.

### 3. Handle Edge Cases
What should Claude do when:
- File format is unexpected?
- Data is malformed?
- User asks for something slightly different?

### 4. One Skill = One Capability
Don't try to do everything in one skill. Chain multiple skills instead.

### 5. Make It Testable
Include expected outputs so Claude can verify its work.

## Skill Chaining

Skills can reference and work with other skills:

```markdown
## Related Skills

- `whatsapp-parser` - Parse raw chat files first
- `action-extractor` - Find TODOs in parsed chats
```

This allows composable workflows:
1. User asks: "Analyze my WhatsApp chat and find action items"
2. Claude uses `whatsapp-parser` skill first
3. Then applies `action-extractor` skill to the result
4. Returns combined output

## Folder Structure

Recommended organization:

```
skills/
├── whatsapp-parser/
│   └── skill.md
├── chat-summarizer/
│   └── skill.md
└── action-extractor/
    └── skill.md
```

Each skill gets its own folder to allow for:
- Multiple files per skill (if needed)
- Skill-specific resources
- Clear organization

## Testing Your Skills

1. **Create test cases** in `examples/`
2. **Run Claude** with specific prompts
3. **Verify outputs** match expected results
4. **Iterate** on instructions based on failures

Example test prompts:
- "Use the whatsapp-parser skill on examples/sample-whatsapp-chat.txt"
- "Parse and summarize this chat"
- "What action items are in this conversation?"
