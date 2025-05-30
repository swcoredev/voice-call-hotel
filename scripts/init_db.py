import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection parameters
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB", "voice_hotel_db_test")

def init_database():
    # Connect to default PostgreSQL database
    engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/postgres")
    
    with engine.connect() as connection:
        connection.execute(text("COMMIT"))  # Close any open transactions
        
        # Create database if it doesn't exist
        try:
            connection.execute(text(f"CREATE DATABASE {DB_NAME}"))
            print(f"Database '{DB_NAME}' created successfully!")
        except Exception as e:
            print(f"Database '{DB_NAME}' already exists or error occurred: {e}")
        
    # Connect to our new database
    engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
    
    with engine.connect() as connection:
        # Create tables
        try:
            # Create calls table
            connection.execute(text("""
                CREATE TABLE IF NOT EXISTS calls (
                    id SERIAL PRIMARY KEY,
                    session_id UUID DEFAULT gen_random_uuid(),
                    start_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    end_time TIMESTAMP WITH TIME ZONE,
                    status VARCHAR(50)
                )
            """))
            
            # Create dialogs table
            connection.execute(text("""
                CREATE TABLE IF NOT EXISTS dialogs (
                    id SERIAL PRIMARY KEY,
                    call_id INTEGER REFERENCES calls(id),
                    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    user_input TEXT,
                    system_response TEXT,
                    intent VARCHAR(100),
                    confidence FLOAT
                )
            """))
            
            connection.execute(text("COMMIT"))
            print("Tables created successfully!")
            
        except Exception as e:
            print(f"Error creating tables: {e}")

if __name__ == "__main__":
    init_database() 