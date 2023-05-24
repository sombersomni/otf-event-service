import psycopg2
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Read the PostgreSQL connection details from environment variables
db_host = os.getenv("POSTGRES_DB_HOST")
db_port = os.getenv("POSTGRES_DB_PORT")
db_name = "tests"
db_user = os.getenv("POSTGRES_DB_USER")
db_password = os.getenv("POSTGRES_DB_PASSWORD")

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host=db_host,
    port=db_port,
    database=db_name,
    user=db_user,
    password=db_password
)

cursor = conn.cursor()
# SQL statement to drop the "Task" table
drop_table_query = "DROP TABLE IF EXISTS Task"

# Execute the SQL statement
cursor.execute(drop_table_query)

# Commit the changes to the database
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()

print("Table dropped successfully.")