# Scripts - Helper Utilities

This folder contains **utility scripts** that complement Claude's AI-powered skills. These are automation helpers, not replacements for Claude's intelligence.

## Available Scripts

### 📄 export_to_google_docs.py

Export Claude's WhatsApp chat analysis to a formatted Google Doc.

**What it does:**
- Takes JSON output from Claude's analysis (summary, action items, decisions)
- Creates a beautifully formatted Google Doc
- Returns shareable link
- Applies formatting (bold headers, emojis, checkboxes)

**Setup:**

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create Google Cloud credentials:**
   - Go to https://console.cloud.google.com/
   - Create a new project (or select existing)
   - Enable Google Docs API: https://console.cloud.google.com/apis/library/docs.googleapis.com
   - Go to Credentials → Create Credentials → OAuth 2.0 Client ID
   - Select "Desktop app" as application type
   - Download the JSON file and save as `credentials.json` in this `scripts/` directory

3. **First run (authorization):**
   ```bash
   python export_to_google_docs.py ../examples/chat_analysis.json
   ```
   - Script will open your browser for Google authorization
   - Click "Allow" to give access to Google Docs
   - A `token.json` file will be created (don't commit this!)

4. **Subsequent runs:**
   ```bash
   python export_to_google_docs.py <your_json_file>
   ```

**Usage in workflow:**

```bash
# Step 1: Ask Claude to analyze a WhatsApp chat
# "Parse and analyze examples/sample-whatsapp-chat.txt and save the output as JSON"

# Step 2: Export to Google Docs
python scripts/export_to_google_docs.py examples/chat_analysis.json

# Output: Google Doc link you can share with your team
```

**Expected JSON format:**

The script expects JSON with this structure (produced by Claude's analysis):

```json
{
  "metadata": {
    "participants": ["Person A", "Person B"],
    "message_count": 74,
    "date_range": {
      "start": "27/01/2026, 09:15:00",
      "end": "28/01/2026, 15:42:30"
    }
  },
  "summary": {
    "tldr": "Brief overview...",
    "key_decisions": [
      "Decision 1",
      "Decision 2"
    ],
    "topics": [
      {"topic": "Topic name", "description": "Details"}
    ]
  },
  "action_items": [
    {
      "task": "Task description",
      "assignee": "Person A",
      "deadline": "Thursday",
      "priority": "high",
      "context": "Why this matters",
      "completed": false
    }
  ]
}
```

## Why Scripts?

**Claude (AI) handles:**
- Parsing WhatsApp chats
- Understanding context and intent
- Extracting action items intelligently
- Summarizing conversations
- Identifying key decisions

**Scripts (Automation) handle:**
- Formatting output for external tools
- API integrations (Google Docs, Notion, CRMs)
- File conversions and exports
- Batch processing
- System automation

**Together = Powerful workflow**: AI analysis → Automated distribution

## Future Scripts (Ideas)

- `export_to_notion.py` - Export to Notion databases
- `send_to_slack.py` - Post summary to Slack channel
- `sync_to_crm.py` - Push action items to Salesforce/HubSpot
- `generate_pdf.py` - Create PDF report from analysis
- `schedule_reminders.py` - Set up calendar reminders for action items

## Security Notes

- **Never commit** `credentials.json` or `token.json` to git
- These files are already in `.gitignore`
- Credentials are personal - each user needs their own
- OAuth tokens are stored locally and refreshed automatically

## Need Help?

- Google Docs API docs: https://developers.google.com/docs/api
- OAuth setup guide: https://developers.google.com/workspace/guides/create-credentials
- GitHub Issues: https://github.com/ShenSeanChen/launch-agent-skills/issues
