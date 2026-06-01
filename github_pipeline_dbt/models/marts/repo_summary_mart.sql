{{ config(materialized='table') }}

WITH repo_summarized_cte AS (
	SELECT 
		repo_id,
		repo_name,
		owner_id AS repo_owner_id,
		repo_language,
		created_at AS repo_created_at,
		fork,
		visibility,
		LENGTH(description) AS repo_description_length
	FROM {{ ref('dim_repos') }}
), repo_commits_summarized_cte AS (
	SELECT 
		repo_id,
		COUNT(*) AS total_commits,
		-- cast git auther id to TEXT for compatible data type with git author email
		-- this coalesce func is here as a fallback to not undercount contributors when author id is null
		COUNT(DISTINCT COALESCE(author_id::TEXT, git_author_email)) AS unique_commit_contributors,
		MIN(NOW() - git_author_date) AS days_since_last_commit,
		MAX(NOW() - git_author_date) AS days_since_first_commit,
		MAX(git_author_date) - MIN(git_author_date) AS commit_activity_span,
		COUNT(DISTINCT git_author_date::DATE) AS active_commit_days,
		-- cast COUNT(*) NUMERIC to avoid integer division that will truncate decimals
		-- (PRECAUTION) if count 0 then null to avoid divide by 0 
		ROUND(COUNT(*)::NUMERIC / NULLIF(COUNT(DISTINCT git_author_date::DATE), 0), 2) AS avg_commits_per_active_day
	FROM {{ ref('fact_commits') }}
	GROUP BY repo_id
), repo_issues_summarized_cte AS (
	SELECT 
		repo_id,
		COUNT(*) AS total_issues,
		-- case when issue 1 then sum to get open issues
		SUM(CASE WHEN issue_state = 'open' THEN 1 ELSE 0 END) AS total_open_issues,
		SUM(CASE WHEN issue_state = 'closed' THEN 1 ELSE 0 END) AS total_closed_issues,
		ROUND(AVG(issue_comments), 2) AS avg_comments_per_issue,
		ROUND(AVG(LENGTH(title))) AS avg_issues_title_length,
		COUNT(DISTINCT created_at::DATE) AS active_issue_days,
		MIN(NOW() - created_at) AS time_since_last_issue,
		MAX(NOW() - created_at) AS time_since_first_issue,
		COUNT(DISTINCT issue_creator_id) AS unique_issue_authors,
		SUM(reaction_total_count) AS total_issue_reactions
	from {{ ref('fact_issues') }}
	GROUP BY repo_id
)

SELECT 
	*
FROM repo_summarized_cte
INNER JOIN repo_commits_summarized_cte RCSC
USING(repo_id)
INNER JOIN repo_issues_summarized_cte RISC
USING(repo_id)
