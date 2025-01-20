# Table of Contents

1. [MongoDB Manager User Guide](#mongodb-manager-user-guide)

    - [Setting Up](#setting-up)
        - [Prerequisites](#prerequisites)
        - [Initialization](#initialization)
    - [CRUD Operations](#crud-operations)
        - [1. Create Operations](#1-create-operations)
        - [2. Read Operations](#2-read-operations)
        - [3. Update Operations](#3-update-operations)
        - [4. Delete Operations](#4-delete-operations)
    - [Connection Management](#connection-management)
    - [Error Handling](#error-handling)
    - [Example Workflow](#example-workflow-1)

2. [PostgresManager User Guide](#postgresmanager-user-guide)
    - [Setting Up](#setting-up-1)
        - [Prerequisites](#prerequisites-1)
        - [Initialization](#initialization-1)
    - [CRUD Operations](#crud-operations-1)
        - [1. Read Operations](#1-read-operations)
        - [2. Create, Update, Delete Operations](#2-create-update-delete-operations)
        - [3. Transaction Management](#3-transaction-management)
    - [Error Handling](#error-handling-1)
    - [Example Workflow](#example-workflow-2)
    - [Notes](#notes)

# 1. MongoDB Manager User Guide

## Setting Up

### Prerequisites

-   MongoDB running and accessible.
-   A valid `MONGO_URI` and `MONGO_DB_NAME` configured in `app.config`.

### Initialization

1. Import `MongoDBManager` into your project:
    ```python
    from app.database.MongoDB_connect import MongoDBManager
    ```
2. Initialize the manager and establish a connection:
    ```python
    mongoManager = MongoDBManager()
    mongoManager.connect()
    ```

---

## CRUD Operations

### 1. Create Operations

#### Insert a Single Document

```python
# Document to insert
document = {"name": "John Doe", "age": 30, "city": "New York"}

# Insert document
inserted_id = mongoManager.insertOne("collection_name", document)
print(f"Inserted Document ID: {inserted_id}")
```

#### Insert Multiple Documents

```python
# List of documents
documents = [
    {"name": "Jane Doe", "age": 28, "city": "Chicago"},
    {"name": "Alice", "age": 35, "city": "San Francisco"}
]

# Insert documents
inserted_ids = mongoManager.insertMany("collection_name", documents)
print(f"Inserted Document IDs: {inserted_ids}")
```

---

### 2. Read Operations

#### Retrieve All Documents

```python
# Retrieve all documents from a collection
all_docs = mongoManager.getCollection("collection_name")
print("All Documents:", all_docs)
```

#### Retrieve a Single Document

```python
# Query to match the document
query = {"name": "John Doe"}

# Retrieve document
doc = mongoManager.getOne("collection_name", query)
print("Retrieved Document:", doc)
```

---

### 3. Update Operations

#### Update a Single Document

```python
# Query to find the document
query = {"name": "John Doe"}

# Fields to update
new_values = {"city": "Boston"}

# Update document
updated_count = mongoManager.updateOne("collection_name", query, new_values)
print(f"Number of Documents Updated: {updated_count}")
```

#### Update Multiple Documents

```python
# Query to find documents
query = {"city": "Chicago"}

# Fields to update
new_values = {"state": "Illinois"}

# Update documents
updated_count = mongoManager.updateMany("collection_name", query, new_values)
print(f"Number of Documents Updated: {updated_count}")
```

---

### 4. Delete Operations

#### Delete a Single Document

```python
# Query to match the document
query = {"name": "Alice"}

# Delete document
deleted_count = mongoManager.deleteOne("collection_name", query)
print(f"Number of Documents Deleted: {deleted_count}")
```

#### Delete Multiple Documents

```python
# Query to match documents
query = {"city": "Boston"}

# Delete documents
deleted_count = mongoManager.deleteMany("collection_name", query)
print(f"Number of Documents Deleted: {deleted_count}")
```

---

## Connection Management

### Connecting to MongoDB

To establish a connection, use:

```python
mongoManager.connect()
```

### Disconnecting from MongoDB

To close the connection:

```python
mongoManager.disconnect()
```

---

## Error Handling

Surround your operations with try-except blocks to handle exceptions:

```python
try:
    # Your operation here
    document = mongoManager.getOne("collection_name", {"name": "Nonexistent"})
    print(document)
except Exception as e:
    print(f"Error: {e}")
```

---

## Example Workflow

Below is a complete example of using the `MongoDBManager`:

```python
mongoManager = MongoDBManager()
mongoManager.connect()

try:
    # Insert a document
    document = {"name": "John", "age": 29, "city": "Seattle"}
    inserted_id = mongoManager.insertOne("users", document)
    print(f"Inserted ID: {inserted_id}")

    # Retrieve documents
    all_users = mongoManager.getCollection("users")
    print("All Users:", all_users)

    # Update a user
    query = {"name": "John"}
    new_data = {"age": 30}
    mongoManager.updateOne("users", query, new_data)

    # Delete a user
    mongoManager.deleteOne("users", {"name": "John"})
finally:
    mongoManager.disconnect()
```

# 2. PostgresManager User Guide

## Setting Up

### Prerequisites

-   PostgreSQL running and accessible.
-   A valid PostgreSQL configuration in `app.config` with the following variables:
    -   `POSTGRES_HOST`
    -   `POSTGRES_DB`
    -   `POSTGRES_USER`
    -   `POSTGRES_PASSWORD`

### Initialization

1. Import the `PostgresManager` class:
    ```python
    from app.database.Postgres_connect import PostgresManager
    ```
2. Initialize the manager and the connection pool:
    ```python
    dbManager = PostgresManager()
    dbManager.initializePool(minConn=1, maxConn=10)
    ```
3. Close the pool when done:
    ```python
    dbManager.closePool()
    ```

---

## CRUD Operations

### 1. Read Operations

#### Execute a SELECT Query

```python
# Example SELECT query
selectQuery = "SELECT NOW() AS current_time;"
result = dbManager.executeQuery(selectQuery)
print("Query Result:", result)
```

#### Execute a SELECT Query with Parameters

```python
# Example query with parameters
query = "SELECT * FROM users WHERE age > %s;"
params = (25,)
result = dbManager.executeQuery(query, params)
print("Query Result:", result)
```

---

### 2. Create, Update, Delete Operations

#### Insert a Record

```python
# INSERT query
insertQuery = """
INSERT INTO example_table (name, age)
VALUES (%s, %s)
RETURNING id;
"""
params = ("John Doe", 30)
insertedId = dbManager.executeQuery(insertQuery, params)
print("Inserted ID:", insertedId)
```

#### Update a Record

```python
# UPDATE query
updateQuery = "UPDATE example_table SET age = age + 1 WHERE name = %s;"
params = ("John Doe",)
rowsUpdated = dbManager.executeNonQuery(updateQuery, params)
print(f"Rows Updated: {rowsUpdated}")
```

#### Delete a Record

```python
# DELETE query
deleteQuery = "DELETE FROM example_table WHERE name = %s;"
params = ("John Doe",)
rowsDeleted = dbManager.executeNonQuery(deleteQuery, params)
print(f"Rows Deleted: {rowsDeleted}")
```

---

### 3. Transaction Management

#### Execute Multiple Queries in a Transaction

```python
transactionQueries = [
    ("INSERT INTO example_table (name, age) VALUES (%s, %s);", ("Jane Doe", 28)),
    ("UPDATE example_table SET age = %s WHERE name = %s;", (35, "John Doe"))
]

success = dbManager.executeTransaction(transactionQueries)
if success:
    print("Transaction executed successfully.")
else:
    print("Transaction failed.")
```

---

## Error Handling

Use try-except blocks to handle exceptions during query execution:

```python
try:
    result = dbManager.executeQuery("SELECT * FROM nonexistent_table;")
except Exception as e:
    print(f"Error: {e}")
```

---

## Example Workflow

```python
# Initialize the PostgresManager instance
dbManager = PostgresManager()
dbManager.initializePool(minConn=1, maxConn=10)

try:
    # SELECT query
    result = dbManager.executeQuery("SELECT NOW();")
    print("Current Time:", result)

    # INSERT query
    insertQuery = "INSERT INTO example_table (name, age) VALUES (%s, %s) RETURNING id;"
    params = ("John Doe", 30)
    insertedId = dbManager.executeQuery(insertQuery, params)
    print("Inserted ID:", insertedId)

    # UPDATE query
    updateQuery = "UPDATE example_table SET age = age + 1 WHERE name = %s;"
    rowsUpdated = dbManager.executeNonQuery(updateQuery, ("John Doe",))
    print(f"Rows Updated: {rowsUpdated}")

    # Transaction
    queries = [
        ("INSERT INTO example_table (name, age) VALUES (%s, %s);", ("Jane Doe", 28)),
        ("DELETE FROM example_table WHERE name = %s;", ("John Doe",))
    ]
    transactionResult = dbManager.executeTransaction(queries)
    print("Transaction Result:", transactionResult)
finally:
    dbManager.closePool()
```

---

## Notes

-   Always initialize the connection pool before performing database operations.
-   Close the pool after all operations to release resources.
-   Use parameterized queries to prevent SQL injection.
