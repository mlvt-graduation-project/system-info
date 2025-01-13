import psycopg2
from psycopg2.extras import RealDictCursor
import yaml
from typing import Dict, List, Any, Union
import os

def connectDb():
    """
    Establish connection to PostgreSQL using configuration from config.yaml
    
    Returns:
        connection: PostgreSQL connection instance
    """
    # Get the directory of the current file
    baseDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    configPath = os.path.join(baseDir, "config.yaml")
    
    with open(configPath, "r") as file:
        config = yaml.safe_load(file)
    
    return psycopg2.connect(
        host=config["POSTGRES_HOST"],
        database=config["POSTGRES_DB"],
        user=config["POSTGRES_USER"],
        password=config["POSTGRES_PASSWORD"]
    )

def executeQuery(conn, query: str, params: tuple = None) -> List[Dict]:
    """
    Execute a SELECT query and return results
    
    Args:
        conn: PostgreSQL connection instance
        query: SQL query string
        params: Query parameters to prevent SQL injection
    
    Returns:
        List[Dict]: List of records as dictionaries
    """
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(query, params)
        return cur.fetchall()

def executeUpdate(conn, query: str, params: tuple = None) -> int:
    """
    Execute an UPDATE query and return number of affected rows
    
    Args:
        conn: PostgreSQL connection instance
        query: SQL query string
        params: Query parameters to prevent SQL injection
    
    Returns:
        int: Number of rows affected
    """
    with conn.cursor() as cur:
        cur.execute(query, params)
        conn.commit()
        return cur.rowcount

def executeInsert(conn, query: str, params: tuple = None) -> int:
    """
    Execute an INSERT query and return number of rows inserted
    
    Args:
        conn: PostgreSQL connection instance
        query: SQL query string
        params: Query parameters to prevent SQL injection
    
    Returns:
        int: Number of rows inserted
    """
    with conn.cursor() as cur:
        cur.execute(query, params)
        conn.commit()
        return cur.rowcount

def executeDelete(conn, query: str, params: tuple = None) -> int:
    """
    Execute a DELETE query and return number of affected rows
    
    Args:
        conn: PostgreSQL connection instance
        query: SQL query string
        params: Query parameters to prevent SQL injection
    
    Returns:
        int: Number of rows affected
    """
    with conn.cursor() as cur:
        cur.execute(query, params)
        conn.commit()
        return cur.rowcount

def executeTransaction(conn, queries: List[tuple]) -> bool:
    """
    Execute multiple queries in a transaction
    
    Args:
        conn: PostgreSQL connection instance
        queries: List of tuples containing (query, params)
    
    Returns:
        bool: True if transaction successful, False otherwise
    """
    try:
        with conn.cursor() as cur:
            for query, params in queries:
                cur.execute(query, params)
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"Transaction failed: {str(e)}")
        return False

def executeInsertReturning(conn, query: str, params: tuple = None) -> Any:
    """
    Execute an INSERT query with RETURNING clause and return the result
    
    Args:
        conn: PostgreSQL connection instance
        query: SQL query string with RETURNING clause
        params: Query parameters to prevent SQL injection
    
    Returns:
        Any: Result of the RETURNING clause
    """
    with conn.cursor() as cur:
        cur.execute(query, params)
        conn.commit()
        res = cur.fetchall()
        if len(res) > 1:
            return res
        else:
            return res[0]

# Usage examples:
def main():
    # Initialize database connection
    conn = connectDb()
    
    # Example SELECT query
    select_query = """
        SELECT * FROM users 
        WHERE age > %s AND city = %s
    """
    results = executeQuery(conn, select_query, (25, 'New York'))
    
    # Example INSERT query
    insert_query = """
        INSERT INTO users (name, email, age) 
        VALUES (%s, %s, %s)
        RETURNING id, name
    """
    (userId, userName) = executeInsertReturning(conn, insert_query, 
                           ('John Doe', 'john@example.com', 30))
    
    insert_query = """
        INSERT INTO inventory (stock) 
        VALUES (%s)
        RETURNING id
    """
    (productId) = executeInsertReturning(conn, insert_query, (10,))
    
    # Example UPDATE query
    update_query = """
        UPDATE users 
        SET age = %s 
        WHERE id = %s
    """
    rows_updated = executeUpdate(conn, update_query, (31, userId))
    
    # Example DELETE query
    # delete_query = """
    #     DELETE FROM users 
    #     WHERE id = %s
    # """
    # rows_deleted = executeDelete(conn, delete_query, (user_id,))
    
    # Example transaction
    transactionQueries = [
        (
            "INSERT INTO orders (user_id, product_id) VALUES (%s, %s)",
            (userId, productId)
        ),
        (
            "UPDATE inventory SET stock = stock - 1 WHERE id = %s",
            (productId,)
        )
    ]
    success = executeTransaction(conn, transactionQueries)
    
    # Close connection
    conn.close()

main()