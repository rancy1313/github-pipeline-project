# insert data into staging tables
from psycopg2.extras import Json

# flatten dictionaries in repo
def flatten_repo_dictionaries(repo):

    # get the current repo dictionary 
    # return empty dict as back up
    owner = repo.get("owner") or {}
    permissions = repo.get("permissions") or {} 
    license = repo.get("license") or {}

    # keep only owner id
    repo["owner_id"] = owner.get("id")

    # flatten repo dicts
    repo["permissions_admin"] = permissions.get("admin")
    repo["permissions_maintain"] = permissions.get("maintain")
    repo["permissions_push"] = permissions.get("push")
    repo["permissions_triage"] = permissions.get("triage")
    repo["permissions_pull"] = permissions.get("pull")

    repo["license_key"] = license.get("key")
    repo["license_name"] = license.get("name")
    repo["license_spdx_id"] = license.get("spdx_id")
    repo["license_url"] = license.get("url")
    repo["license_node_id"] = license.get("node_id")
    
    repo.pop("owner", None)
    repo.pop("permissions", None)
    repo.pop("license", None)

# flatten commit dictionaries while truncating noise
def flatten_repo_commit_dictionaries(commit, repo_id):
        
    # commit dict
    commit_info = commit.get("commit") or {}

    # dicts within commit
    git_author = commit_info.get("author") or {}
    git_committer = commit_info.get("committer") or {}
    tree = commit_info.get("tree") or {}
    verification = commit_info.get("verification") or {}

    # remaining dicts
    author = commit.get("author") or {}
    committer = commit.get("committer") or {}
    parents = commit.get("parents") or []

    # set repo_id
    commit["repo_id"] = repo_id

    # flatten dicts
    commit["message"] = commit_info.get("message")
    commit["comment_count"] = commit_info.get("comment_count")

    commit["git_author_name"] = git_author.get("name")
    commit["git_author_email"] = git_author.get("email")
    commit["git_author_date"] = git_author.get("date")

    commit["git_committer_name"] = git_committer.get("name")
    commit["git_committer_email"] = git_committer.get("email")
    commit["git_committer_date"] = git_committer.get("date")

    commit["author_login"] = author.get("login")
    commit["author_id"] = author.get("id")
    commit["author_type"] = author.get("type")
    commit["author_site_admin"] = author.get("site_admin")
    commit["author_user_view_type"] = author.get("user_view_type")

    commit["committer_login"] = committer.get("login")
    commit["committer_id"] = committer.get("id")
    commit["committer_type"] = committer.get("type")
    commit["committer_site_admin"] = committer.get("site_admin")
    commit["committer_user_view_type"] = committer.get("user_view_type")

    commit["tree_sha"] = tree.get("sha")
    commit["tree_url"] = tree.get("url")

    commit["verified"] = verification.get("verified")
    commit["verification_reason"] = verification.get("reason")
    commit["verification_signature"] = verification.get("signature")
    commit["verification_payload"] = verification.get("payload")
    commit["verified_at"] = verification.get("verified_at")

    # keep only the values in a list
    commit["parent_shas"] = [parent.get("sha") for parent in parents]

    # remove dicts from commit
    commit.pop("commit", None)
    commit.pop("author", None)
    commit.pop("committer", None)
    commit.pop("parents", None)

# flatten the repo issues dicts
def flatten_repo_issues_dictionaries(issue, repo_id):

    # get the dicts in the current issue
    user = issue.get("user") or {}
    sub_issues_summary = issue.get("sub_issues_summary") or {}
    issue_dependencies_summary = issue.get("issue_dependencies_summary") or {}
    reactions = issue.get("reactions") or {}
    assignee = issue.get("assignee") or {}
    closed_by = issue.get("closed_by") or {}

    # to flatten dicts in labels list
    issue_labels = []

    # set user id/repo id
    issue["user_id"] = user.get("id")
    issue["repo_id"] = repo_id

    # flatten nested issue dictionaries
    issue["sub_issues_summary_total"] = sub_issues_summary.get("total")
    issue["sub_issues_summary_completed"] = sub_issues_summary.get("completed")
    issue["sub_issues_summary_percent_completed"] = sub_issues_summary.get("percent_completed")

    issue["issue_dependencies_summary_blocked_by"] = issue_dependencies_summary.get("blocked_by")
    issue["issue_dependencies_summary_total_blocked_by"] = issue_dependencies_summary.get("total_blocked_by")
    issue["issue_dependencies_summary_blocking"] = issue_dependencies_summary.get("blocking")
    issue["issue_dependencies_summary_total_blocking"] = issue_dependencies_summary.get("total_blocking")

    issue["reaction_total_count"] = reactions.get("total_count")
    issue["reaction_plus"] = reactions.get("+1")
    issue["reaction_minus"] = reactions.get("-1")
    issue["reaction_laugh"] = reactions.get("laugh")
    issue["reaction_hooray"] = reactions.get("hooray")
    issue["reaction_confused"] = reactions.get("confused")
    issue["reaction_heart"] = reactions.get("heart")
    issue["reaction_rocket"] = reactions.get("rocket")
    issue["reaction_eyes"] = reactions.get("eyes")

    issue["assignee_id"] = assignee.get("id")
    issue["assignee_login"] = assignee.get("login")
    issue["assignee_type"] = assignee.get("type")
    issue["assignee_site_admin"] = assignee.get("site_admin")

    issue["closed_by_id"] = closed_by.get("id")
    issue["closed_by_login"] = closed_by.get("login")
    issue["closed_by_type"] = closed_by.get("type")
    issue["closed_by_site_admin"] = closed_by.get("site_admin")

    # store as structured data (col type JSONB)
    # labels and assignees are repeated nested structures, so JSONB preserves them
    issue["labels_json"] = Json(issue.get("labels") or [])
    issue["assignees_json"] = Json(issue.get("assignees") or [])
    issue["milestone_json"] = Json(issue.get("milestone") or [])

    # remove dicts from issue
    issue.pop("user", None)
    issue.pop("sub_issues_summary", None)
    issue.pop("issue_dependencies_summary", None)
    issue.pop("reactions", None)
    issue.pop("pull_request", None)
    issue.pop("pinned_comment", None)
    issue.pop("draft", None)
    issue.pop("type", None)
    issue.pop("assignee", None)
    issue.pop("closed_by", None)
    issue.pop("labels", None)
    issue.pop("assignees", None)
    issue.pop("milestone", None)

# rename cols to avoid naming issues ( SQL keywords) when creating staging table
def normalize_data_columns(data, rename_map):

    # for each col that needs to be renamed, create the new col and pop the old one
    for old_key, new_key in rename_map.items():
        data[new_key] = data.get(old_key)
        data.pop(old_key, None)