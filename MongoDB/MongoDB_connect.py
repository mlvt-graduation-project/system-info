from pymongo import MongoClient
import time
import yaml
from typing import Dict, Any
import os

def connectDb():
    """
    Establish connection to MongoDB using configuration from config.yaml
    
    Returns:
        database: MongoDB database instance
    """
    baseDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    configPath = os.path.join(baseDir, "config.yaml")
    with open(configPath, "r") as file:
        config = yaml.safe_load(file)
    client = MongoClient(config["MONGO_URI"])  
    return client[config["MONGO_DB"]]  

def getCollection(db, collectionName: str):
    """
    Retrieve all documents from a collection
    
    Args:
        db: MongoDB database instance
        collectionName: Name of the collection to query
    
    Returns:
        cursor: MongoDB cursor containing all documents
    """
    return db[collectionName].find({})

def getOne(db, collectionName: str, query: Dict):
    """
    Retrieve a single document from a collection that matches the query
    
    Args:
        db: MongoDB database instance
        collectionName: Name of the collection to query
        query: Dictionary containing query parameters
    
    Returns:
        dict: Single document matching the query or None if not found
    """
    return db[collectionName].find_one(query)

def insertOne(db, collectionName: str, document: Dict):
    """
    Insert a single document into a collection
    
    Args:
        db: MongoDB database instance
        collectionName: Name of the collection to insert into
        document: Dictionary containing the document data
    
    Returns:
        InsertOneResult: Result object containing inserted_id
    """
    return db[collectionName].insert_one(document)

def insertMany(db, collectionName: str, documents: list):
    """
    Insert multiple documents into a collection
    
    Args:
        db: MongoDB database instance
        collectionName: Name of the collection to insert into
        documents: List of dictionaries containing the documents data
    
    Returns:
        InsertManyResult: Result object containing inserted_ids
    """
    return db[collectionName].insert_many(documents)

def updateOne(db, collectionName: str, query: Dict, newValues: Dict):
    """
    Update a single document in a collection
    
    Args:
        db: MongoDB database instance
        collectionName: Name of the collection to update
        query: Dictionary containing query parameters to find the document
        newValues: Dictionary containing the fields to update
    
    Returns:
        UpdateResult: Result object containing modified_count and matched_count
    """
    return db[collectionName].update_one(query, {"$set": newValues})

def updateMany(db, collectionName: str, query: Dict, newValues: Dict):
    """
    Update multiple documents in a collection
    
    Args:
        db: MongoDB database instance
        collectionName: Name of the collection to update
        query: Dictionary containing query parameters to find documents
        newValues: Dictionary containing the fields to update
    
    Returns:
        UpdateResult: Result object containing modified_count and matched_count
    """
    return db[collectionName].update_many(query, {"$set": newValues})

def deleteOne(db, collectionName: str, query: Dict):
    """
    Delete a single document from a collection
    
    Args:
        db: MongoDB database instance
        collectionName: Name of the collection to delete from
        query: Dictionary containing query parameters to find the document
    
    Returns:
        DeleteResult: Result object containing deleted_count
    """
    return db[collectionName].delete_one(query)

def deleteMany(db, collectionName: str, query: Dict):
    """
    Delete multiple documents from a collection
    
    Args:
        db: MongoDB database instance
        collectionName: Name of the collection to delete from
        query: Dictionary containing query parameters to find documents
    
    Returns:
        DeleteResult: Result object containing deleted_count
    """
    return db[collectionName].delete_many(query)


# Usage examples:
def main():
    # Initialize database connection
    db = connectDb()
    # Insert a document
    newPost = {
        "title": "Test Post",
        "content": "This is a test post",
        "created_at": time.time()
    }
    insertOne(db, "posts", newPost)

    # Update a document
    updateOne(db, "posts", 
              {"title": "Test Post"}, 
              {"content": "Updated content"})

    # Delete a document
    # deleteOne(db, "posts", {"title": "Test Post"})

    # Get and print all documents
    posts = getCollection(db, "posts")
    for post in posts:
        print(post)
main()
