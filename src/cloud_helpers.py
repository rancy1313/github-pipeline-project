# connect to datawarehouse
from google.cloud import bigquery

# read data from db to upload to datawarehouse
import pandas as pd

# upload data to BigQuery
def upload_to_datawarehouse(tables, conn, client):

    # truncate existing tables to avoid uploading dupes
    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_TRUNCATE"
    )

    # for each table in the db, retrieve all rows and upload to BQ
    for table in tables:

        table_id = ("github-pipeline-498414.github_analytics." + table)

        df = pd.read_sql(f"SELECT * FROM {table}", conn)

        job = client.load_table_from_dataframe(df, table_id, job_config=job_config)

        job.result()

        print(f"Loaded {table}: {len(df)} rows")