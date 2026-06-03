{{ config(materialized='table') }}

SELECT
        issue_id,
	(assignees ->> 'id')::BIGINT AS assignee_id,
	assignees ->> 'url' AS assignee_url,
        assignees ->> 'received_events_url' AS assignee_received_events_url,
	assignees ->> 'login' AS assignee_login,
	assignees ->> 'gists_url' AS assignee_gists_url,
	assignees ->> 'node_id' AS assignee_node_id,
	assignees ->> 'repos_url' AS assignee_repos_url,
	assignees ->> 'following_url' AS assignee_following_url,
	assignees ->> 'gravatar_id' AS assignee_gravatar_id,
	assignees ->> 'avatar_url' AS assignee_avatar_url,
	assignees ->> 'user_view_type' AS assignee_user_view_type,
	assignees ->> 'events_url' AS assignee_events_url,
	assignees ->> 'organizations_url' AS assignee_organizations_url,
	assignees ->> 'starred_url' AS assignee_starred_url,
	assignees ->> 'subscriptions_url' AS assignee_subscriptions_url,
	(assignees ->> 'site_admin')::BOOLEAN AS assignee_site_admin,
	assignees ->> 'type' AS assignee_type,
	assignees ->> 'html_url' AS assignee_html_url
FROM {{ ref('fact_issues') }},
jsonb_array_elements(assignees_json) AS assignees
