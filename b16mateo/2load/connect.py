import psycopg2


def connect_to_db(dbname, user, password, host, port):
    conn = None
    cur = None
    try:
        conn = psycopg2.connect(
            dbname=dbname, user=user, password=password, host=host, port=port
        )
        print("Successfully connected to PostgreSQL!")
        # Create a cursor
        cur = conn.cursor()
    except Exception as e:
        if conn:
            conn.rollback()  # Rollback the transaction if an error occurs
        print(f"Error: {e}")
    return cur, conn
