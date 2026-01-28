# Directory: launch-agent-skills/skills/whatsapp-action-extractor/skill.md
---
name: Action Item Extractor
description: Extract TODOs, commitments, follow-ups, and action items from chat conversations
triggers:
  - action items
  - todos
  - follow ups
  - commitments
  - tasks
  - what needs to be done
---

# Action Item Extractor

## Purpose

Identify and extract actionable items from conversations:
- Explicit TODOs ("I'll do X")
- Implicit commitments ("Let me check on that")
- Requests ("Can you...?")
- Deadlines and due dates
- Follow-up items

## Instructions

### Step 1: Identify Action Patterns

```python
action_patterns = {
    # Explicit commitments
    'self_commitment': [
        r"i('ll| will) (do|send|check|review|update|fix|create|schedule)",
        r"let me (do|send|check|handle|take care of)",
        r"i('m going to|'ll) (work on|look into|investigate)",
        r"will do",
        r"on it",
        r"i can (do|handle|take) (that|this|it)"
    ],
    
    # Requests to others
    'request': [
        r"can you (please )?(do|send|check|review|update|fix|create)",
        r"could you (please )?(do|send|check|review|update|fix|create)",
        r"please (do|send|check|review|update|fix|create)",
        r"(would|could) you mind",
        r"need you to",
        r"(your|you're) (task|job|responsibility)"
    ],
    
    # Explicit TODO markers
    'explicit_todo': [
        r"TODO:",
        r"ACTION:",
        r"TASK:",
        r"REMINDER:",
        r"\[ \]",  # Unchecked checkbox
        r"don't forget to",
        r"remember to",
        r"make sure to"
    ],
    
    # Deadline indicators
    'deadline': [
        r"by (monday|tuesday|wednesday|thursday|friday|saturday|sunday)",
        r"by (tomorrow|today|tonight|EOD|end of day|end of week|EOW)",
        r"before \d{1,2}(:\d{2})?\s*(am|pm)?",
        r"due (on|by|date)",
        r"deadline",
        r"ASAP",
        r"urgent(ly)?",
        r"as soon as possible"
    ],
    
    # Follow-up indicators
    'follow_up': [
        r"follow up",
        r"circle back",
        r"check (back|in) (on|with|later)",
        r"let('s| us) (revisit|discuss|talk about) (this|that) (later|tomorrow|next week)",
        r"ping me",
        r"remind me",
        r"keep me (posted|updated)"
    ]
}
```

### Step 2: Extract Context

For each action item found:
- **Who**: Assignee (who should do it)
- **What**: The actual task
- **When**: Due date/deadline if mentioned
- **Why**: Context from surrounding messages
- **Priority**: Inferred from language (ASAP = high, etc.)

### Step 3: Structure Output

```json
{
  "action_items": [
    {
      "id": 1,
      "type": "commitment",
      "task": "Review Bob's PR #142",
      "assignee": "Alice Developer",
      "deadline": "EOD today",
      "priority": "high",
      "context": "Bob submitted the auth bug fix",
      "source_message": "Action item: Review Bob's PR #142",
      "timestamp": "28/01/2026 14:35:22"
    },
    {
      "id": 2,
      "type": "request",
      "task": "Update the README",
      "assignee": "Bob Engineer",
      "deadline": "Before PR merge",
      "priority": "medium",
      "context": "Documentation needs updating",
      "source_message": "Can you also update the README?",
      "timestamp": "28/01/2026 09:16:45"
    }
  ],
  "summary": {
    "total_items": 2,
    "by_assignee": {
      "Alice Developer": 1,
      "Bob Engineer": 1
    },
    "by_priority": {
      "high": 1,
      "medium": 1,
      "low": 0
    },
    "overdue": 0,
    "due_today": 1
  }
}
```

### Step 4: Format for Output

**Markdown Format:**

```markdown
## Action Items Extracted

### High Priority 🔴
- [ ] **Review Bob's PR #142** - @Alice Developer - Due: EOD today
  > Context: Bob submitted the auth bug fix

### Medium Priority 🟡
- [ ] **Update the README** - @Bob Engineer - Due: Before PR merge
  > Context: Documentation needs updating

### Summary
| Assignee | Tasks | Completed |
|----------|-------|-----------|
| Alice Developer | 1 | 0 |
| Bob Engineer | 1 | 0 |
```

## Priority Inference Rules

| Indicator | Priority Level |
|-----------|---------------|
| ASAP, urgent, critical, immediately | 🔴 High |
| Today, EOD, tonight | 🔴 High |
| Tomorrow, this week | 🟡 Medium |
| When you can, eventually, sometime | 🟢 Low |
| No deadline mentioned | 🟡 Medium (default) |

## Assignee Resolution

When assignee is ambiguous:
1. Check for "@name" mentions
2. Check for "you" (addressee of message)
3. Check for "I/I'll" (message sender)
4. If still unclear, mark as "TBD"

## Example Usage

**User**: "Extract action items from the parsed chat"

**Claude should**:
1. Scan all messages for action patterns
2. Resolve assignees and deadlines
3. Prioritize based on language cues
4. Present in actionable format (checkboxes)
5. Provide summary statistics

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Completed items (✅, done, finished) | Mark as completed, still include |
| Cancelled items | Note as cancelled if explicit |
| Duplicate tasks | Deduplicate, note recurrence |
| Vague commitments ("I'll think about it") | Include with low confidence flag |

## Related Skills

- `whatsapp-parser` - Parse raw chat first
- `whatsapp-summarizer` - Get broader context
