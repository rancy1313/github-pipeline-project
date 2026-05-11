# insert data into staging tables
from psycopg2.extras import execute_values

# function to insert ingested data into staging tables
def table_insertion(conn, table_name, all_data):

    # create cursor of DB operations
    cur = conn.cursor()

    # get dict keys for list of columns
    dict_columns = list(all_data[0].keys())

    # query to insert data into DB table
    sql_query = f"""
        INSERT INTO {table_name} ({",".join(dict_columns)})
        VALUES %s
        """

    # convert data into list of tuples for insertion
    data = [
        tuple(row.get(col) for col in dict_columns)
        for row in all_data
    ]

    # load data in DB table
    execute_values(cur, sql_query, data)

    # commit and close cursor
    conn.commit()
    cur.close()