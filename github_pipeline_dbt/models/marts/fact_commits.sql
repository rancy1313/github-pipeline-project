{{ config(materialized='table')}}

-- cut noise
SELECT
	sha,

    	repo_id,
	repo_message,
	
	comment_count,
	
	git_author_name,
	git_author_email,
	git_author_date,
	git_committer_name,
	git_committer_email,
	git_committer_date::TIMESTAMPTZ,
	
	author_login,
	author_id,
	author_type,
	author_site_admin,
	author_user_view_type,
	
	committer_login,
	committer_id,
	committer_type,
	committer_site_admin,
	committer_user_view_type,
	
	tree_sha,
	
	verified,
	verification_reason,
	verified_at,
	
	parent_shas

	html_url
	
FROM {{ ref('stg_commits')}}
