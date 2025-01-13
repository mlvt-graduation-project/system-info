-- init.sql

-- Create users table if it does not exist
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    age INT NULL,
    city VARCHAR(100) NULL
);

-- Create orders table if it does not exist
CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Create inventory table if it does not exist
CREATE TABLE IF NOT EXISTS inventory (
    id SERIAL PRIMARY KEY,
    stock INT NOT NULL
);