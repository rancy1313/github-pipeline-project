{{ config(materialized='table') }}

-- leave url cols in stg users
SELECT
    user_id,
    login,
    html_url,
    user_type,
    user_view_type,
    site_admin,
    user_name,
    company,
    blog,
    user_location,
    email,
    hireable,
    bio,
    twitter_username,
    public_repos,
    public_gists,
    followers,
    user_following,
    created_at,
    updated_at
FROM {{ ref('stg_users') }}
