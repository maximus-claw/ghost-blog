#!/usr/bin/env python3
import os
import json
import time
import jwt
import requests
import markdown
import frontmatter
import argparse
from pathlib import Path

def get_credentials():
    cred_path = Path.home() / ".ghost" / "credentials.json"
    if not cred_path.exists():
        raise FileNotFoundError(f"Credentials file not found at {cred_path}")
    with open(cred_path, 'r') as f:
        return json.load(f)

def create_jwt(api_key):
    # Split the key into ID and SECRET
    try:
        key_id, secret = api_key.split(':')
    except ValueError:
        raise ValueError("Invalid API Key format. Expected ID:SECRET")

    # Prepare header and payload
    iat = int(time.time())
    header = {'alg': 'HS256', 'typ': 'JWT', 'kid': key_id}
    payload = {
        'iat': iat,
        'exp': iat + 5 * 60,
        'aud': '/admin/'
    }

    # Create the token (secret needs to be in bytes for HS256)
    token = jwt.encode(payload, bytes.fromhex(secret), algorithm='HS256', headers=header)
    return token

def publish_post(md_path, title_override=None, status="draft"):
    creds = get_credentials()
    url = creds['admin_api_url'].rstrip('/')
    api_key = creds['admin_api_key']

    # Read markdown and frontmatter
    post = frontmatter.load(md_path)
    content_html = markdown.markdown(post.content, extensions=['fenced_code', 'tables'])
    
    title = title_override or post.get('title', 'Untitled Post')
    excerpt = post.get('excerpt', post.get('description', ''))
    tags = post.get('tags', [])
    
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(',')]

    # Create JWT
    token = create_jwt(api_key)

    # Prepare request
    endpoint = f"{url}/ghost/api/admin/posts/"
    headers = {'Authorization': f'Ghost {token}'}
    
    post_data = {
        "posts": [{
            "title": title,
            "html": content_html,
            "status": status,
            "custom_excerpt": excerpt,
            "tags": [{"name": tag} for tag in tags]
        }]
    }

    response = requests.post(endpoint, json=post_data, headers=headers)
    
    if response.status_code == 201:
        print(f"Successfully created post: {title}")
        print(f"Status: {status}")
        return response.json()
    else:
        print(f"Error publishing post: {response.status_code}")
        print(response.text)
        response.raise_for_status()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Publish Markdown to Ghost")
    parser.add_argument("file", help="Path to markdown file")
    parser.add_argument("--title", help="Override title")
    parser.add_argument("--status", choices=["draft", "published"], default="draft", help="Post status")
    
    args = parser.parse_args()
    
    try:
        publish_post(args.file, args.title, args.status)
    except Exception as e:
        print(f"Fatal error: {e}")
