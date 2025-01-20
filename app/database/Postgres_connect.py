from psycopg2.pool import SimpleConnectionPool
from psycopg2.extras import RealDictCursor
from app.config import POSTGRES_DB, POSTGRES_HOST, POSTGRES_PASSWORD, POSTGRES_USER
from typing import List, Dict, Any
from app.utils.logging_setup import logger

class PostgresManager:
    _instance = None
    _pool: SimpleConnectionPool = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(PostgresManager, cls).__new__(cls)
        return cls._instance

    def initializePool(self, minConn: int = 1, maxConn: int = 20):
        """
        Initialize the connection pool.
        """
        if not self._pool:
            self._pool = SimpleConnectionPool(
                minConn, maxConn,
                host=POSTGRES_HOST,
                database=POSTGRES_DB,
                user=POSTGRES_USER,
                password=POSTGRES_PASSWORD
            )
            logger.info("Database connection pool initialized.")

    def closePool(self):
        """
        Close all connections in the pool.
        """
        if self._pool:
            self._pool.closeall()
            self._pool = None
            logger.info("Database connection pool closed.")

    def getConnection(self):
        """
        Get a connection from the pool.
        """
        if not self._pool:
            raise RuntimeError("Connection pool is not initialized.")
        return self._pool.getconn()

    def releaseConnection(self, conn):
        """
        Release a connection back to the pool.
        """
        if self._pool:
            self._pool.putconn(conn)

    def executeQuery(self, query: str, params: tuple = None) -> List[Dict]:
        """
        Execute a query that return results
        Args:
            query: SQL query string
            params: Query parameters to prevent SQL injection
        Returns:
            List[Dict]: List of records as dictionaries
        """
        conn = self.getConnection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, params)
                return cur.fetchall()
        finally:
            self.releaseConnection(conn)

    def executeNonQuery(self, query: str, params: tuple = None) -> int:
        """
        Execute an INSERT, UPDATE, or DELETE query and return number of affected rows
        Args:
            query: SQL query string
            params: Query parameters to prevent SQL injection
        Returns:
            int: Number of rows affected
        """
        conn = self.getConnection()
        try:
            with conn.cursor() as cur:
                cur.execute(query, params)
                conn.commit()
                return cur.rowcount
        finally:
            self.releaseConnection(conn)

    def executeTransaction(self, queries: List[tuple]) -> bool:
        """
        Execute multiple queries in a transaction
        Args:
            queries: List of tuples containing (query, params)
        Returns:
            bool: True if transaction successful, False otherwise
        """
        conn = self.getConnection()
        try:
            with conn.cursor() as cur:
                for query, params in queries:
                    cur.execute(query, params)
                conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print(f"Transaction failed: {e}")
            return False
        finally:
            self.releaseConnection(conn)

# usage of class
def main():
    # Initialize the PostgresManager instance
    dbManager = PostgresManager()
    
    # Initialize the connection pool with a minimum of 1 and a maximum of 10 connections
    dbManager.initializePool(minConn=1, maxConn=10)
    
    try:
        # Example: Using executeQuery to run a SELECT query
        print("Executing SELECT query...")
        selectQuery = "SELECT NOW() AS current_time;"
        selectResult = dbManager.executeQuery(selectQuery)
        print(f"SELECT Result: {selectResult}")


        # Example: Using executeNonQuery to run an INSERT query
        print("Executing INSERT query...")
        insertQuery = """
            INSERT INTO example_table (name, age)
            VALUES (%s, %s)
            RETURNING id;
        """
        insertParams = ("John Doe", 30)
        insertResult = dbManager.executeQuery(insertQuery, insertParams)
        print(f"INSERT Result: {insertResult}")


        # Example: Using executeNonQuery to run an UPDATE query
        print("Executing UPDATE query...")
        updateQuery = "UPDATE example_table SET age = age + 1 WHERE name = %s;"
        updateParams = ("John Doe",)
        rowsUpdated = dbManager.executeNonQuery(updateQuery, updateParams)
        print(f"Rows Updated: {rowsUpdated}")


        # Example: Using executeTransaction to execute multiple queries in a single transaction
        print("Executing Transaction...")
        transactionQueries = [
            ("INSERT INTO example_table (name, age) VALUES (%s, %s);", ("Jane Doe", 28)),
            ("UPDATE example_table SET age = %s WHERE name = %s;", (35, "John Doe"))
        ]
        transactionSuccess = dbManager.executeTransaction(transactionQueries)
        if transactionSuccess:
            print("Transaction executed successfully.")
        else:
            print("Transaction failed.")


    except Exception as e:
        # Handle any errors during query execution
        print(f"An error occurred: {e}")
    finally:
        # Close the connection pool to release resources
        dbManager.closePool()
