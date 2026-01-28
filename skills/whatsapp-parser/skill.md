# Directory: launch-agent-skills/skills/whatsapp-parser/skill.md
---
name: WhatsApp Chat Parser
description: Parse WhatsApp chat exports into structured JSON data with participants, timestamps, and messages
triggers:
  - whatsapp
  - chat export
  - parse chat
  - message history
  - chat file
---

# WhatsApp Chat Parser

## Purpose

Parse WhatsApp chat export files (.txt) and extract structured data including:
- Participant list
- Message count and date range
- Individual messages with timestamps and senders
- Media placeholders and system messages

## WhatsApp Export Format

WhatsApp exports follow this pattern (may vary by locale):

```
[DD/MM/YYYY, HH:MM:SS] Sender Name: Message content
```

### Format Variations

| Region | Date Format | Example |
|--------|-------------|---------|
| US | MM/DD/YY | [01/28/26, 9:15:32 AM] |
| EU/UK | DD/MM/YYYY | [28/01/2026, 09:15:32] |
| ISO | YYYY-MM-DD | [2026-01-28, 09:15:32] |

### Special Message Types

- **Media**: `<Media omitted>` or `<image omitted>`, `<video omitted>`
- **System**: Messages without sender (e.g., "Alice added Bob to the group")
- **Multi-line**: Continuation lines without timestamp prefix
- **Links**: URLs embedded in message text
- **Replies**: May include quoted text with formatting

## Instructions

### Step 1: Read the Chat File

```python
with open(chat_file_path, 'r', encoding='utf-8') as f:
    content = f.read()
```

### Step 2: Parse Messages Using Regex

```python
import re
from datetime import datetime

# Pattern for WhatsApp message format (handles multiple date formats)
patterns = [
    # EU format: [DD/MM/YYYY, HH:MM:SS]
    r'\[(\d{2}/\d{2}/\d{4}),\s*(\d{2}:\d{2}:\d{2})\]\s*([^:]+):\s*(.*)',
    # US format: [MM/DD/YY, H:MM:SS AM/PM]
    r'\[(\d{2}/\d{2}/\d{2}),\s*(\d{1,2}:\d{2}:\d{2}\s*[AP]M)\]\s*([^:]+):\s*(.*)',
]

messages = []
current_message = None

for line in content.split('\n'):
    matched = False
    for pattern in patterns:
        match = re.match(pattern, line)
        if match:
            if current_message:
                messages.append(current_message)
            
            date_str, time_str, sender, text = match.groups()
            current_message = {
                'date': date_str,
                'time': time_str,
                'sender': sender.strip(),
                'content': text.strip(),
                'is_media': '<media omitted>' in text.lower() or '<omitted>' in text.lower()
            }
            matched = True
            break
    
    # Handle multi-line messages
    if not matched and current_message and line.strip():
        current_message['content'] += '\n' + line

if current_message:
    messages.append(current_message)
```

### Step 3: Extract Metadata

```python
participants = list(set(msg['sender'] for msg in messages))
date_range = {
    'start': messages[0]['date'] if messages else None,
    'end': messages[-1]['date'] if messages else None
}
message_count = len(messages)
media_count = sum(1 for msg in messages if msg['is_media'])
```

### Step 4: Return Structured Output

```json
{
  "metadata": {
    "participants": ["Alice Developer", "Bob Engineer"],
    "message_count": 42,
    "media_count": 3,
    "date_range": {
      "start": "28/01/2026",
      "end": "28/01/2026"
    }
  },
  "messages": [
    {
      "timestamp": "28/01/2026 09:15:32",
      "sender": "Alice Developer",
      "content": "Hey Bob, did you push the code?",
      "is_media": false
    }
  ]
}
```

## Edge Cases

| Scenario | How to Handle |
|----------|---------------|
| System messages | Sender = "System" or skip |
| Empty lines | Skip or treat as message separator |
| Emoji-only messages | Parse normally, emoji preserved |
| Very long messages | No truncation, preserve full content |
| Non-UTF8 encoding | Try latin-1 fallback |

## Example Usage in Claude Code

**User**: "Parse the WhatsApp chat in examples/sample-whatsapp-chat.txt"

**Claude should**:
1. Read the file using the path provided
2. Apply the parsing logic above
3. Return structured JSON with metadata and messages
4. Highlight interesting stats (most active participant, busiest hour, etc.)

## Related Skills

- `whatsapp-summarizer` - Generate summaries from parsed chats
- `whatsapp-action-extractor` - Find TODOs and action items in messages
