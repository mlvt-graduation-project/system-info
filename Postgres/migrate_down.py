import psycopg2
import os
import yaml

def connectDb():
    """
    Establish connection to PostgreSQL using configuration from config.yaml
    
    Returns:
        connection: PostgreSQL connection instance
    """
    # Get the directory of the current file
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(base_dir, "config.yaml")
    
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
    
    return psycopg2.connect(
        host=config["POSTGRES_HOST"],
        database=config["POSTGRES_DB"],
        user=config["POSTGRES_USER"],
        password=config["POSTGRES_PASSWORD"]
    )

def runSqlFile(connection):
    drop_tables_sql = """
    DROP TABLE IF EXISTS orders;
    DROP TABLE IF EXISTS inventory;
    DROP TABLE IF EXISTS users;
    """
    
    with connection.cursor() as cursor:
        cursor.execute(drop_tables_sql)
        connection.commit()

def main():
    try:
        # Connect to the database
        connection = connectDb()
        print("Successfully connected to the database.")
        
        # Run the SQL to drop tables
        runSqlFile(connection)
        print("Tables dropped successfully.")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        
    finally:
        if connection:
            connection.close()
            print("Database connection closed.")

main()