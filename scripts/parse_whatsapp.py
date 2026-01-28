# Directory: launch-agent-skills/scripts/parse_whatsapp.py
"""
WhatsApp Chat Parser Script.

A standalone helper script that can be used as a resource by the
whatsapp-parser skill or run directly from command line.

Usage:
    python scripts/parse_whatsapp.py examples/sample-whatsapp-chat.txt

Author: Shen Sean Chen
License: MIT
"""

import re
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path


def parse_whatsapp_chat(file_path: str) -> Dict[str, Any]:
    """
    Parse a WhatsApp chat export file into structured JSON.
    
    Args:
        file_path: Path to the WhatsApp chat export .txt file
        
    Returns:
        Dictionary containing metadata and parsed messages
    """
    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Regex patterns for different WhatsApp date formats
    patterns = [
        # EU format: [DD/MM/YYYY, HH:MM:SS]
        r'\[(\d{2}/\d{2}/\d{4}),\s*(\d{2}:\d{2}:\d{2})\]\s*([^:]+):\s*(.*)',
        # US format with AM/PM: [MM/DD/YY, H:MM:SS AM/PM]
        r'\[(\d{2}/\d{2}/\d{2}),\s*(\d{1,2}:\d{2}:\d{2}\s*[AP]M)\]\s*([^:]+):\s*(.*)',
        # Simple format: DD/MM/YYYY, HH:MM - Sender: Message
        r'(\d{2}/\d{2}/\d{4}),\s*(\d{2}:\d{2})\s*-\s*([^:]+):\s*(.*)',
    ]
    
    messages: List[Dict[str, Any]] = []
    current_message: Optional[Dict[str, Any]] = None
    
    for line in content.split('\n'):
        matched = False
        
        for pattern in patterns:
            match = re.match(pattern, line)
            if match:
                # Save previous message if exists
                if current_message:
                    messages.append(current_message)
                
                date_str, time_str, sender, text = match.groups()
                
                # Check if it's a media message
                is_media = any(marker in text.lower() for marker in [
                    '<media omitted>',
                    '<image omitted>',
                    '<video omitted>',
                    '<audio omitted>',
                    '<document omitted>',
                    '<sticker omitted>'
                ])
                
                current_message = {
                    'date': date_str.strip(),
                    'time': time_str.strip(),
                    'timestamp': f"{date_str.strip()} {time_str.strip()}",
                    'sender': sender.strip(),
                    'content': text.strip(),
                    'is_media': is_media
                }
                matched = True
                break
        
        # Handle multi-line messages (continuation without timestamp)
        if not matched and current_message and line.strip():
            current_message['content'] += '\n' + line
    
    # Don't forget the last message
    if current_message:
        messages.append(current_message)
    
    # Extract metadata
    participants = list(set(msg['sender'] for msg in messages))
    media_count = sum(1 for msg in messages if msg['is_media'])
    
    date_range = {
        'start': messages[0]['date'] if messages else None,
        'end': messages[-1]['date'] if messages else None
    }
    
    return {
        'metadata': {
            'participants': sorted(participants),
            'message_count': len(messages),
            'media_count': media_count,
            'date_range': date_range,
            'file_path': str(file_path)
        },
        'messages': messages
    }


def extract_action_items(parsed_chat: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Extract action items from parsed chat messages.
    
    Args:
        parsed_chat: Output from parse_whatsapp_chat()
        
    Returns:
        List of identified action items
    """
    action_patterns = {
        'todo': r'(?i)(TODO|ACTION|TASK|REMINDER):\s*(.+)',
        'commitment': r"(?i)i('ll| will)\s+(.+)",
        'request': r"(?i)(can|could) you\s+(please\s+)?(.+)\??",
        'deadline': r"(?i)by\s+(EOD|end of day|tomorrow|monday|tuesday|wednesday|thursday|friday)"
    }
    
    action_items = []
    item_id = 1
    
    for msg in parsed_chat['messages']:
        content = msg['content']
        
        # Check for explicit TODOs
        todo_match = re.search(action_patterns['todo'], content)
        if todo_match:
            action_items.append({
                'id': item_id,
                'type': 'explicit_todo',
                'task': todo_match.group(2).strip(),
                'assignee': msg['sender'],
                'timestamp': msg['timestamp'],
                'source_message': content
            })
            item_id += 1
            continue
        
        # Check for commitments ("I'll do X")
        commit_match = re.search(action_patterns['commitment'], content)
        if commit_match:
            action_items.append({
                'id': item_id,
                'type': 'commitment',
                'task': commit_match.group(2).strip(),
                'assignee': msg['sender'],
                'timestamp': msg['timestamp'],
                'source_message': content
            })
            item_id += 1
    
    return action_items


def generate_summary(parsed_chat: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate a summary of the chat conversation.
    
    Args:
        parsed_chat: Output from parse_whatsapp_chat()
        
    Returns:
        Summary dictionary with key insights
    """
    messages = parsed_chat['messages']
    metadata = parsed_chat['metadata']
    
    # Count messages per participant
    participant_counts = {}
    for msg in messages:
        sender = msg['sender']
        participant_counts[sender] = participant_counts.get(sender, 0) + 1
    
    # Find most active participant
    most_active = max(participant_counts.items(), key=lambda x: x[1])
    
    return {
        'participant_stats': participant_counts,
        'most_active': {
            'name': most_active[0],
            'message_count': most_active[1]
        },
        'total_messages': metadata['message_count'],
        'media_messages': metadata['media_count'],
        'text_messages': metadata['message_count'] - metadata['media_count'],
        'date_range': metadata['date_range']
    }


def main():
    """Command line interface for the parser."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python parse_whatsapp.py <chat_file.txt>")
        print("Example: python parse_whatsapp.py examples/sample-whatsapp-chat.txt")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    if not Path(file_path).exists():
        print(f"Error: File not found: {file_path}")
        sys.exit(1)
    
    print(f"Parsing: {file_path}\n")
    
    # Parse the chat
    parsed = parse_whatsapp_chat(file_path)
    
    # Print metadata
    print("=" * 50)
    print("CHAT METADATA")
    print("=" * 50)
    print(f"Participants: {', '.join(parsed['metadata']['participants'])}")
    print(f"Total Messages: {parsed['metadata']['message_count']}")
    print(f"Media Messages: {parsed['metadata']['media_count']}")
    print(f"Date Range: {parsed['metadata']['date_range']['start']} to {parsed['metadata']['date_range']['end']}")
    
    # Print summary
    summary = generate_summary(parsed)
    print(f"\nMost Active: {summary['most_active']['name']} ({summary['most_active']['message_count']} messages)")
    
    # Extract action items
    actions = extract_action_items(parsed)
    if actions:
        print("\n" + "=" * 50)
        print("ACTION ITEMS FOUND")
        print("=" * 50)
        for action in actions:
            print(f"  [{action['type']}] {action['task']}")
            print(f"    Assignee: {action['assignee']}")
            print(f"    Time: {action['timestamp']}")
            print()
    
    # Save full output to JSON
    output_file = file_path.replace('.txt', '_parsed.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'metadata': parsed['metadata'],
            'summary': summary,
            'action_items': actions,
            'messages': parsed['messages']
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\nFull output saved to: {output_file}")


if __name__ == '__main__':
    main()
