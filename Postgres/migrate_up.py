# init_db.py

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

def runSqlFile(filename, connection):
    with open(filename, 'r') as file:
        sql = file.read()
    
    with connection.cursor() as cursor:
        cursor.execute(sql)
        connection.commit()

def main():
    try:
        # Kết nối tới cơ sở dữ liệu
        connection = connectDb()
        print("Successfully connected to the database.")
        
        # Run the SQL file
        runSqlFile('init_postgres.sql', connection)
        print("SQL file executed successfully.")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        
    finally:
        if connection:
            connection.close()
            print("Database connection closed.")

if __name__ == '__main__':
    main()