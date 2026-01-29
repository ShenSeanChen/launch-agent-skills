#!/usr/bin/env python3
"""
Export WhatsApp chat analysis to Google Docs.

This script takes parsed chat data (JSON) and creates a formatted Google Doc
with the summary, action items, and key decisions.

Setup:
1. Create a Google Cloud project: https://console.cloud.google.com/
2. Enable Google Docs API: https://console.cloud.google.com/apis/library/docs.googleapis.com
3. Create OAuth credentials (Desktop app)
4. Download credentials.json to this directory
5. Run this script - it will open a browser for first-time authorization

Usage:
    python export_to_google_docs.py <input_json_file>

Example:
    python export_to_google_docs.py ../examples/chat_analysis.json
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the token.json file
SCOPES = ['https://www.googleapis.com/auth/documents']

def get_credentials():
    """Get valid user credentials from storage or run OAuth flow."""
    creds = None
    token_path = Path(__file__).parent / 'token.json'
    credentials_path = Path(__file__).parent / 'credentials.json'

    # Token stores the user's access and refresh tokens
    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)

    # If there are no (valid) credentials, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not credentials_path.exists():
                print("Error: credentials.json not found!")
                print("\nSetup instructions:")
                print("1. Go to https://console.cloud.google.com/")
                print("2. Create a project (or select existing)")
                print("3. Enable Google Docs API")
                print("4. Create OAuth 2.0 credentials (Desktop app)")
                print("5. Download credentials.json to scripts/ directory")
                sys.exit(1)

            flow = InstalledAppFlow.from_client_secrets_file(
                str(credentials_path), SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for next run
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    return creds


def create_document(service, title):
    """Create a new Google Doc and return the document ID."""
    doc = service.documents().create(body={'title': title}).execute()
    return doc.get('documentId')


def build_content(data):
    """Build formatted content from parsed chat data."""
    requests = []

    # Title
    title = f"WhatsApp Chat Analysis - {datetime.now().strftime('%B %d, %Y')}\n\n"

    # Build text content
    content = title

    # TL;DR Section
    if 'summary' in data and 'tldr' in data['summary']:
        content += "📊 TL;DR\n"
        content += f"{data['summary']['tldr']}\n\n"

    # Key Decisions
    if 'summary' in data and 'key_decisions' in data['summary']:
        content += "✅ Key Decisions\n"
        for decision in data['summary']['key_decisions']:
            content += f"• {decision}\n"
        content += "\n"

    # Topics Discussed
    if 'summary' in data and 'topics' in data['summary']:
        content += "💬 Topics Discussed\n"
        for i, topic in enumerate(data['summary']['topics'], 1):
            if isinstance(topic, dict):
                content += f"{i}. {topic.get('topic', 'Unknown')}: {topic.get('description', '')}\n"
            else:
                content += f"{i}. {topic}\n"
        content += "\n"

    # Action Items
    if 'action_items' in data:
        content += "📋 Action Items\n\n"

        # Group by priority
        high_priority = [item for item in data['action_items'] if item.get('priority') == 'high']
        medium_priority = [item for item in data['action_items'] if item.get('priority') == 'medium']
        low_priority = [item for item in data['action_items'] if item.get('priority') == 'low']

        if high_priority:
            content += "🔴 High Priority\n"
            for item in high_priority:
                status = "☑" if item.get('completed') else "☐"
                content += f"{status} {item['task']} - @{item.get('assignee', 'Unassigned')}"
                if item.get('deadline'):
                    content += f" - Due: {item['deadline']}"
                content += "\n"
                if item.get('context'):
                    content += f"   Context: {item['context']}\n"
            content += "\n"

        if medium_priority:
            content += "🟡 Medium Priority\n"
            for item in medium_priority:
                status = "☑" if item.get('completed') else "☐"
                content += f"{status} {item['task']} - @{item.get('assignee', 'Unassigned')}"
                if item.get('deadline'):
                    content += f" - Due: {item['deadline']}"
                content += "\n"
            content += "\n"

        if low_priority:
            content += "🟢 Low Priority\n"
            for item in low_priority:
                status = "☑" if item.get('completed') else "☐"
                content += f"{status} {item['task']} - @{item.get('assignee', 'Unassigned')}"
                if item.get('deadline'):
                    content += f" - Due: {item['deadline']}"
                content += "\n"
            content += "\n"

    # Statistics
    if 'metadata' in data:
        content += "📈 Conversation Statistics\n"
        if 'participants' in data['metadata']:
            content += f"Participants: {', '.join(data['metadata']['participants'])}\n"
        if 'message_count' in data['metadata']:
            content += f"Total messages: {data['metadata']['message_count']}\n"
        if 'date_range' in data['metadata']:
            date_range = data['metadata']['date_range']
            content += f"Date range: {date_range.get('start', 'N/A')} - {date_range.get('end', 'N/A')}\n"
        content += "\n"

    # Footer
    content += f"\n---\nGenerated by Agent Skills Demo\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    return content


def insert_text(document_id, content):
    """Insert text into the Google Doc."""
    return [
        {
            'insertText': {
                'location': {'index': 1},
                'text': content
            }
        }
    ]


def apply_formatting(content):
    """Apply text formatting (bold headers, etc.)."""
    requests = []

    # Find all emoji headers (🔴, 🟡, 🟢, 📊, ✅, 💬, 📋, 📈)
    lines = content.split('\n')
    current_index = 1

    for line in lines:
        line_length = len(line) + 1  # +1 for newline

        # Make emoji headers bold
        if any(emoji in line for emoji in ['📊', '✅', '💬', '📋', '📈', '🔴', '🟡', '🟢']):
            requests.append({
                'updateTextStyle': {
                    'range': {
                        'startIndex': current_index,
                        'endIndex': current_index + line_length - 1
                    },
                    'textStyle': {
                        'bold': True,
                        'fontSize': {
                            'magnitude': 12,
                            'unit': 'PT'
                        }
                    },
                    'fields': 'bold,fontSize'
                }
            })

        current_index += line_length

    return requests


def export_to_google_docs(json_file_path):
    """Main function to export JSON data to Google Docs."""
    try:
        # Load the JSON data
        with open(json_file_path, 'r') as f:
            data = json.load(f)

        print(f"✓ Loaded data from {json_file_path}")

        # Get credentials
        print("Authenticating with Google...")
        creds = get_credentials()
        print("✓ Authenticated successfully")

        # Build the service
        service = build('docs', 'v1', credentials=creds)

        # Create document
        print("Creating Google Doc...")
        doc_title = f"WhatsApp Analysis - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        document_id = create_document(service, doc_title)
        print(f"✓ Created document: {doc_title}")

        # Build content
        content = build_content(data)

        # Insert text
        print("Adding content...")
        text_requests = insert_text(document_id, content)
        service.documents().batchUpdate(
            documentId=document_id,
            body={'requests': text_requests}
        ).execute()
        print("✓ Content added")

        # Apply formatting
        print("Applying formatting...")
        format_requests = apply_formatting(content)
        if format_requests:
            service.documents().batchUpdate(
                documentId=document_id,
                body={'requests': format_requests}
            ).execute()
        print("✓ Formatting applied")

        # Generate shareable link
        doc_url = f"https://docs.google.com/document/d/{document_id}/edit"

        print("\n" + "="*60)
        print("✅ SUCCESS! Google Doc created")
        print("="*60)
        print(f"\n📄 Document: {doc_title}")
        print(f"🔗 URL: {doc_url}")
        print("\nYou can now:")
        print("  • Share this link with your team")
        print("  • Edit the doc in your browser")
        print("  • Export to PDF/Word from Google Docs\n")

        return document_id, doc_url

    except FileNotFoundError:
        print(f"Error: File not found: {json_file_path}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in file: {json_file_path}")
        sys.exit(1)
    except HttpError as error:
        print(f"Google API Error: {error}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


def main():
    """CLI entry point."""
    if len(sys.argv) != 2:
        print("Usage: python export_to_google_docs.py <input_json_file>")
        print("\nExample:")
        print("  python export_to_google_docs.py ../examples/chat_analysis.json")
        sys.exit(1)

    json_file = sys.argv[1]

    if not os.path.exists(json_file):
        print(f"Error: File not found: {json_file}")
        sys.exit(1)

    export_to_google_docs(json_file)


if __name__ == '__main__':
    main()
