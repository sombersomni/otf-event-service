import psycopg2
from dotenv import load_dotenv
import os
from faker import Faker

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

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Instantiate Faker object
fake = Faker()

# Generate and insert three fake tasks
for _ in range(3):
    name = fake.word()
    task_type = fake.random_element(["Type A", "Type B", "Type C"])
    created_by = fake.name()
    created_at = fake.date_time_this_decade()
    status = fake.random_element(["Pending", "In Progress", "Completed"])

    # SQL statement to insert a task
    insert_query = "INSERT INTO task (name, type, created_by, created_at, status) VALUES (%s, %s, %s, %s, %s)"

    # Execute the SQL statement
    cursor.execute(insert_query, (name, task_type, created_by, created_at, status))

# Commit the changes to the database
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()

print("Fake tasks inserted successfully.")