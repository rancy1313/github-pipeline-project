{{ config(materialized='table') }}

SELECT
        issue_id,
	(label ->> 'id')::BIGINT AS label_id,
	label ->> 'url' AS label_url,
        label ->> 'name' AS label_name,
	label ->> 'color' AS label_color,
	(label ->> 'default')::BOOLEAN AS label_default,
	label ->> 'node_id' AS label_node_id,
	label ->> 'description' AS label_description
FROM {{ ref('fact_issues') }},
jsonb_array_elements(labels_json) AS label
