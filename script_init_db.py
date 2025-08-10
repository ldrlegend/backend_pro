import subprocess
import psycopg2
from psycopg2 import sql
from app.db.session import SessionLocal
from app.models import user, product
from app.db.init_db import init_db
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="./.env")

# Fetch environment variables
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Function to drop the database
def drop_database():
    print("Dropping the database...")
    # Connect to the default database (usually postgres)
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    conn.autocommit = True
    cursor = conn.cursor()

    # Drop the target database
    cursor.execute("DROP DATABASE IF EXISTS mydb;")
    print("Database dropped!")
    cursor.close()
    conn.close()

# Function to create the database
def create_database():
    print("Creating the database...")
    # Connect to the default database (postgres)
    conn = psycopg2.connect(dbname="postgres", user="postgres", password="password", host="localhost")
    conn.autocommit = True
    cursor = conn.cursor()

    # Create the new database
    cursor.execute("CREATE DATABASE mydb;")
    print("Database created!")
    cursor.close()
    conn.close()

# Function to run Alembic migrations
def run_migrations():
    print("Running Alembic migrations...")
    # Run the Alembic command to generate and apply migrations
    subprocess.run(["alembic", "revision", "--autogenerate", "-m", "initial migration"], check=True)
    subprocess.run(["alembic", "upgrade", "head"], check=True)
    print("Migrations completed!")

# Function to seed the database with sample data
def insert_sample_data():
    print("Inserting sample data...")
    db = SessionLocal()

    # Insert sample users
    user1 = user.User(name="John Doe", email="johndoe@example.com")
    user2 = user.User(name="Jane Smith", email="janesmith@example.com")

    db.add(user1)
    db.add(user2)

    db.commit()  # Commit the changes
    db.close()   # Close the session

    print("Sample data inserted!")

# Main function to run all the steps
def main():
    # Drop and create the database
    drop_database()
    create_database()

    # Run Alembic migrations
    run_migrations()

    # Seed the database with sample data
    insert_sample_data()

if __name__ == "__main__":
    main()
