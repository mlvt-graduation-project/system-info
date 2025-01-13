# system-info

## Overview

This project provides a system for managing and interacting with MongoDB and PostgreSQL databases. It includes scripts for database migrations, connections, and basic CRUD operations.

## File Descriptions

-   **`MongoDB_connect.py`**: Contains functions to connect to a MongoDB database and perform CRUD operations on collections.

-   **`Postgres/Postgres_connect.py`**: Provides functions to connect to a PostgreSQL database and execute SQL queries, including SELECT, INSERT, UPDATE, DELETE, and transaction management.

-   **`Postgres/init_postgres.sql`**: SQL script to initialize the PostgreSQL database with necessary tables if they do not exist.

-   **`Postgres/migrate_up.py`**: Script to apply database migrations by executing the `init_postgres.sql` file.

-   **`Postgres/migrate_down.py`**: Script to reverse database migrations by dropping tables created by `init_postgres.sql`.

-   **`config.yaml`**: Configuration file containing database connection details for both MongoDB and PostgreSQL.

-   **`requirements.txt`**: Lists all Python dependencies required for the project, which can be installed using pip.

-   **`Makefile`**: Contains commands to automate common tasks such as running database scripts and installing dependencies.

## Makefile Commands

-   `postgres`: Runs the **`Postgres_connect.py`** script to interact with the PostgreSQL database. Usage: `make postgres`

-   `postgres_up`: Executes the **`migrate_up.py`** script to apply database migrations. Usage: `make postgres_up`

-   `postgres_down`: Executes the **`migrate_down.py`** script to reverse database migrations. Usage: `make postgres_down`

-   `mongo`: Runs the **`MongoDB_connect.py`** script to interact with the MongoDB database. Usage: `make mongo`

-   `install_requirement`: Installs all Python dependencies listed in **`requirements.txt`** using Python 3.11. Usage: `make install_requirement`
