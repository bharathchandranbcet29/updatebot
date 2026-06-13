import requests
import json
import os
import base64

USERNAME = "bharathchandranbcet29"

# Generate projects.json
url = f"https://api.github.com/users/{USERNAME}/repos"
repos = requests.get(url).json()

projects = []

for repo in repos:
    projects.append(
        {
            "title": repo["name"],
            "description": repo["description"] or "GitHub Automation Project",
            "github": repo["html_url"]
        }
    )

json_content = json.dumps(projects, indent=4)

# Update portfolio repository
print("PAT exists:", os.getenv("PAT_TOKEN") is not None)
TOKEN = os.getenv("PAT_TOKEN")
print("PAT length:", len(TOKEN) if TOKEN else 0)

headers = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github+json"
}

repo_api = "https://api.github.com/repos/bharathchandranbcet29/portfolio/contents/projects.json"

# Get current file SHA
response = requests.get(repo_api, headers=headers)

print(response.status_code)
print(response.text)

current = response.json()

payload = {
    "message": "Auto update projects.json",
    "content": base64.b64encode(json_content.encode()).decode(),
    "sha": current["sha"]
}

response = requests.put(
    repo_api,
    headers=headers,
    json=payload
)

print(response.status_code)
print("Portfolio projects.json updated!")