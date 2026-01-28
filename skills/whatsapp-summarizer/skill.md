# Directory: launch-agent-skills/skills/whatsapp-summarizer/skill.md
---
name: Chat Summarizer
description: Generate concise summaries from parsed chat conversations, identifying key topics, decisions, and themes
triggers:
  - summarize chat
  - conversation summary
  - chat overview
  - what was discussed
  - meeting notes
---

# Chat Summarizer

## Purpose

Transform parsed chat data into actionable summaries including:
- Executive summary (2-3 sentences)
- Key topics discussed
- Decisions made
- Important dates/deadlines mentioned
- Sentiment analysis (optional)

## Prerequisites

This skill works best with **already parsed** chat data (from `whatsapp-parser` skill).
Can also work directly with raw text if needed.

## Instructions

### Step 1: Analyze Conversation Structure

Identify conversation segments:
- **Thread starters**: Messages that introduce new topics
- **Responses**: Replies and reactions
- **Transitions**: Topic changes

### Step 2: Extract Key Elements

Look for these patterns:

```python
key_patterns = {
    'decisions': [
        r"let's go with",
        r"we'll do",
        r"decided to",
        r"agreed on",
        r"confirmed",
        r"approved"
    ],
    'deadlines': [
        r"by (monday|tuesday|wednesday|thursday|friday|tomorrow|EOD|end of day)",
        r"due (on|by) \w+",
        r"deadline",
        r"before \d{1,2}(am|pm)"
    ],
    'blockers': [
        r"blocked by",
        r"waiting on",
        r"can't proceed",
        r"need .* first",
        r"depends on"
    ],
    'questions': [
        r"\?$",
        r"^(what|when|where|who|why|how|can|could|should|would)"
    ]
}
```

### Step 3: Generate Summary Structure

```json
{
  "executive_summary": "Brief 2-3 sentence overview",
  "key_topics": [
    {
      "topic": "Code deployment",
      "discussed_by": ["Alice", "Bob"],
      "outcome": "Agreed to deploy Monday"
    }
  ],
  "decisions": [
    {
      "decision": "Use FastAPI for the new service",
      "made_by": "Alice",
      "context": "Performance requirements"
    }
  ],
  "open_questions": [
    "What's the budget for cloud hosting?"
  ],
  "deadlines": [
    {
      "item": "PR review",
      "due": "EOD today",
      "owner": "Bob"
    }
  ],
  "sentiment": "productive",
  "conversation_stats": {
    "duration": "2 hours",
    "most_active": "Alice (23 messages)",
    "response_time_avg": "3 minutes"
  }
}
```

### Step 4: Apply Summary Template

**For Professional/Work Chats:**

```markdown
## Chat Summary: [Date Range]

### TL;DR
[Executive summary in 2-3 sentences]

### Key Decisions
- [Decision 1] - by [Person]
- [Decision 2] - by [Person]

### Action Items
- [ ] [Task] - [Owner] - Due: [Date]

### Topics Discussed
1. **[Topic 1]**: [Brief description]
2. **[Topic 2]**: [Brief description]

### Open Questions
- [Question still needing answers]
```

**For Casual/Social Chats:**

```markdown
## Chat Highlights: [Date Range]

### What Happened
[Casual summary of the conversation]

### Fun Moments
- [Interesting/funny exchanges]

### Plans Made
- [Any meetups, events, or plans]
```

## Summarization Guidelines

| Aspect | Guideline |
|--------|-----------|
| **Length** | 10-20% of original content |
| **Tone** | Match the chat's formality level |
| **Names** | Preserve participant names |
| **Quotes** | Include 1-2 key quotes if impactful |
| **Dates** | Convert relative dates to absolute when possible |

## Example Usage

**User**: "Summarize the parsed WhatsApp chat"

**Claude should**:
1. Check if chat is already parsed (use `whatsapp-parser` if not)
2. Identify conversation type (work/casual)
3. Apply appropriate template
4. Highlight actionable items prominently

## Edge Cases

- **Very short chats** (< 10 messages): Provide brief overview, note limited content
- **Media-heavy chats**: Note media context, summarize text content
- **Multi-topic chats**: Create separate sections per topic
- **Emotional conversations**: Handle sensitively, focus on facts

## Related Skills

- `whatsapp-parser` - Parse raw chat files first
- `whatsapp-action-extractor` - Deep dive into action items
