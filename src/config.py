# to get my token from .env
from dotenv import load_dotenv

# get token
import os

# get token from .env

# load .env
load_dotenv()

# get token
TOKEN = os.getenv("GITHUB_TOKEN")

# get DB name
DB_NAME = os.getenv("DB_NAME")

# get DB password
PASSWORD = os.getenv("PASSWORD")

# declare headers with TOKEN

headers = {
    "Authorization": f"Bearer {TOKEN}"
}

# rename GitHub REST API columns to match table columns
rename_users_map = {
    "id": "user_id",
    "type": "user_type",
    "name": "user_name",
    "location": "user_location",
    "following": "user_following"
}

rename_repos_map = {
    "id": "repo_id",
    "language": "repo_language",
    "size": "repo_size",
    "name": "repo_name"
}

rename_commits_map = {
    "message": "repo_message"
}

rename_issues_map = {
    "id": "issue_id",
    "comments": "issue_comments",
    "number": "issue_number",
    "locked": "issue_locked",
    "state": "issue_state",
    "assignees": "assignees_json"
}