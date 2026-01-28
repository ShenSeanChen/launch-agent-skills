# Directory: launch-agent-skills/skills/rag-tools/skill.md
---
name: Agent Tools Setup
description: Configure Google Calendar and Gmail tools for launch-agentic-rag agent capabilities
triggers:
  - agent tools
  - google calendar
  - gmail integration
  - tool setup
  - agentic tools
  - service account
---

# Agent Tools Setup Skill

## Purpose

Configure optional tool integrations for [launch-agentic-rag](https://github.com/ShenSeanChen/launch-agentic-rag) to enable:
- 📅 **Google Calendar** - Schedule and manage meetings
- 📧 **Gmail** - Send emails on behalf of user
- 🔧 **Custom Tools** - Framework for adding more tools

**IMPORTANT**:
- This skill is **ONLY for launch-agentic-rag** (not needed for launch-rag)
- These tools are **optional** - the agent works without them
- Requires Google Cloud project and service account

## Prerequisites

- launch-agentic-rag cloned and set up (use `rag-setup` skill)
- Google Cloud account
- Basic understanding of service accounts and OAuth

## Instructions

### Step 0: Check If Needed

**Ask the user:**
```
Do you want to set up Google Calendar/Gmail tools?

These are optional for launch-agentic-rag. Without them:
✅ Agent still works for Q&A and reasoning
❌ Can't schedule meetings or send emails

Set up tools now? [y/n]
```

If "n" or "no": Skip this skill entirely.

### Step 1: Create Google Cloud Project

**Guide the user:**

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Click **Select Project** → **New Project**
3. Name it: `agentic-rag-tools` (or user preference)
4. Click **Create**
5. Wait for project creation (~30 seconds)

### Step 2: Enable APIs

**In Google Cloud Console:**

1. Go to **APIs & Services** → **Library**
2. Search and enable:
   - ✅ **Google Calendar API**
   - ✅ **Gmail API**

**Via gcloud CLI (alternative):**
```bash
# Enable required APIs
gcloud services enable calendar-json.googleapis.com
gcloud services enable gmail.googleapis.com

echo "✅ APIs enabled"
```

### Step 3: Create Service Account

**In Google Cloud Console:**

1. Go to **IAM & Admin** → **Service Accounts**
2. Click **Create Service Account**
3. Fill in:
   - **Name**: `agentic-rag-agent`
   - **Description**: "Service account for RAG agent tool access"
4. Click **Create and Continue**
5. Skip role assignment (click **Continue**)
6. Click **Done**

### Step 4: Generate Service Account Key

**In Google Cloud Console:**

1. Find your service account in the list
2. Click the **three dots** → **Manage Keys**
3. Click **Add Key** → **Create New Key**
4. Choose **JSON** format
5. Click **Create**
6. **Save the downloaded JSON file** (e.g., `service-account-key.json`)

⚠️ **IMPORTANT**: Keep this file secure - it has access to your account!

### Step 5: Move Credentials to Project

```bash
# Create credentials directory
mkdir -p credentials

# Move the downloaded key
mv ~/Downloads/service-account-key.json credentials/

# Secure the file
chmod 600 credentials/service-account-key.json

echo "✅ Service account credentials stored securely"
```

### Step 6: Update .env File

**Use Edit tool to add to .env:**

```bash
# Google Cloud Configuration (for agent tools)
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_APPLICATION_CREDENTIALS=credentials/service-account-key.json

# Tool Configuration
ENABLE_CALENDAR_TOOL=true
ENABLE_EMAIL_TOOL=true
```

**To get your project ID:**
```bash
# From the JSON file
cat credentials/service-account-key.json | grep project_id

# Or from gcloud
gcloud config get-value project
```

### Step 7: Grant Calendar/Gmail Access

**IMPORTANT**: Service accounts need delegated access to use Calendar/Gmail.

**Option A: Domain-Wide Delegation (G Suite/Workspace)**

If you have Google Workspace:
1. Go to [Admin Console](https://admin.google.com)
2. Navigate to **Security** → **API Controls** → **Domain-wide Delegation**
3. Click **Add new**
4. Enter service account **Client ID** (from JSON file)
5. Add OAuth scopes:
   ```
   https://www.googleapis.com/auth/calendar
   https://www.googleapis.com/auth/gmail.send
   ```
6. Click **Authorize**

**Option B: User Impersonation (Personal Gmail)**

For personal accounts, you'll need OAuth2:
1. Create OAuth2 credentials in Google Cloud Console
2. Configure consent screen
3. Use user authentication flow instead of service account

⚠️ **Note**: Service accounts work best with Google Workspace. Personal Gmail requires OAuth2 setup.

### Step 8: Test Tools Configuration

```bash
# Test if credentials are valid
python -c "
from google.oauth2 import service_account
import json

with open('credentials/service-account-key.json') as f:
    creds = service_account.Credentials.from_service_account_file(
        'credentials/service-account-key.json',
        scopes=[
            'https://www.googleapis.com/auth/calendar',
            'https://www.googleapis.com/auth/gmail.send'
        ]
    )
    print('✅ Credentials loaded successfully')
    print(f'Service account: {creds.service_account_email}')
"
```

### Step 9: Verify in Application

Start the server and test tool endpoints:

```bash
# Start server
uvicorn main:app --reload --port 8000

# Test calendar tool
curl -X POST http://localhost:8000/agent/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Schedule a meeting tomorrow at 2pm"}'

# Test email tool
curl -X POST http://localhost:8000/agent/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Send an email to test@example.com saying hello"}'
```

## Checklist

- [ ] Google Cloud project created
- [ ] Google Calendar API enabled
- [ ] Gmail API enabled
- [ ] Service account created
- [ ] Service account key downloaded (JSON)
- [ ] Credentials moved to `credentials/` directory
- [ ] File permissions set to 600
- [ ] .env updated with GOOGLE_APPLICATION_CREDENTIALS
- [ ] (If Workspace) Domain-wide delegation configured
- [ ] (If personal) OAuth2 flow set up
- [ ] Credentials test passed
- [ ] Tools work in application

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Permission denied" error | Check domain-wide delegation or OAuth setup |
| "Credentials not found" | Verify GOOGLE_APPLICATION_CREDENTIALS path |
| "API not enabled" | Enable Calendar/Gmail APIs in Cloud Console |
| "Invalid grant" | Service account needs delegated access |
| Personal Gmail not working | Use OAuth2 instead of service account |

## Important Notes

- 🔒 **Keep credentials secure** - Add `credentials/` to `.gitignore`
- 🏢 **Best for Workspace** - Service accounts work best with Google Workspace
- 👤 **Personal accounts** - Require OAuth2, more setup required
- 🔧 **Optional feature** - Agent works without tools for Q&A
- 🆓 **Free tier** - Google Cloud free tier covers typical usage

## Related Skills

- `rag-setup` - Set up launch-agentic-rag first
- `rag-database` - Configure database after this

## What This Enables

With tools configured, your agent can:
- ✅ **Schedule meetings**: "Schedule a meeting with John tomorrow at 3pm"
- ✅ **Send emails**: "Email the team about the project update"
- ✅ **Reason about actions**: Agent decides when to use tools vs just answer
- ✅ **Multi-step workflows**: Retrieve info → Schedule meeting → Send confirmation

Without tools, agent only does Q&A with RAG retrieval.
