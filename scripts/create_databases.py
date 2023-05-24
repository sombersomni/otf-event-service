import psycopg2
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Read the PostgreSQL connection details from environment variables
db_host = os.getenv("POSTGRES_DB_HOST")
db_port = os.getenv("POSTGRES_DB_PORT")
db_name = "postgres"
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

# Set autocommit mode to True
conn.autocommit = True

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Create a new database
cursor.execute("CREATE DATABASE tests")

# Commit the changes to the default database
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()

print("Database created successfully.")
