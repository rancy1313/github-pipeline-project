# insert data into staging tables
from psycopg2.extras import execute_values

# db adapter
import psycopg2

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

# get the most recent user id to get user data from after the latest user
# GITHUB REST API uses since keyword to retrieve user data
# so if id
def retrieve_last_user_id(DB_NAME, PASSWORD):

    # make connection to retrieve most recent user_id
    conn = psycopg2.connect(f"dbname={DB_NAME} user=postgres password={PASSWORD}")

    cur = conn.cursor()

    # select max id since ids increment and if null then 0
    sql_query = """
        SELECT COALESCE(MAX(user_id), 0)
        FROM users 
    """

    cur.execute(sql_query)

    # if no recent user id exists then 0 to get data starting from first user in the API
    recent_user_id = cur.fetchone()[0]

    cur.close()
    conn.close()

    return recent_user_id