{{ config(materialized='table') }}

SELECT
    issue_id,
    issue_number,
    repo_id,

    title,
    body,
    issue_state,
    state_reason,
    issue_locked,
    author_association,

    issue_comments,
    created_at,
    updated_at,
    closed_at,

    assignee_id,
    assignee_login,
    assignee_type,
    assignee_site_admin,

    closed_by_id,
    closed_by_login,
    closed_by_type,
    closed_by_site_admin,

    labels_json,
    assignees_json,
    milestone_json,

    sub_issues_summary_total,
    sub_issues_summary_completed,
    sub_issues_summary_percent_completed,

    issue_dependencies_summary_blocked_by,
    issue_dependencies_summary_total_blocked_by,
    issue_dependencies_summary_blocking,
    issue_dependencies_summary_total_blocking,

    reaction_total_count,
    reaction_plus,
    reaction_minus,
    reaction_laugh,
    reaction_hooray,
    reaction_confused,
    reaction_heart,
    reaction_rocket,
    reaction_eyes,

    html_url

FROM {{ ref('stg_issues') }}
