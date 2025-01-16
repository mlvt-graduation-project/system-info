from pymongo import MongoClient
from typing import Dict, Any, List
from app.config import MONGO_URI, MONGO_DB_NAME
from app.utils.logging_setup import logger

class MongoDBManager:
    """
    A singleton class to manage MongoDB connections and CRUD operations.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(MongoDBManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.client = None
        self.db = None

    def connect(self):
        """
        Establish a connection to MongoDB and initialize the database instance.
        """
        if not self.client:
            self.client = MongoClient(MONGO_URI)
            self.db = self.client[MONGO_DB_NAME]
            logger.info(f"Connected to MongoDB: {MONGO_DB_NAME}")


    def disconnect(self):
        """
        Close the MongoDB connection.
        """
        if self.client:
            self.client.close()
            self.client = None
            logger.info("MongoDB connection closed.")

    def getCollection(self, collectionName: str) -> List[Dict]:
        """
        Retrieve all documents from a collection.
        Input:
            - collectionName (str): Name of the collection.
        Output:
            - List[Dict]: List of all documents in the collection.
        """
        return list(self.db[collectionName].find({}))

    def getOne(self, collectionName: str, query: Dict) -> Dict:
        """
        Retrieve a single document from a collection that matches the query.
        Input:
            - collectionName (str): Name of the collection.
            - query (Dict): Query to filter documents.
        Output:
            - Dict: The first document that matches the query, or None if not found.
        """
        return self.db[collectionName].find_one(query)

    def insertOne(self, collectionName: str, document: Dict) -> Any:
        """
        Insert a single document into a collection.
        Input:
            - collectionName (str): Name of the collection.
            - document (Dict): The document to insert.
        Output:
            - Any: The ID of the inserted document.
        """
        return self.db[collectionName].insert_one(document).inserted_id

    def insertMany(self, collectionName: str, documents: List[Dict]) -> List[Any]:
        """
        Insert multiple documents into a collection.
        Input:
            - collectionName (str): Name of the collection.
            - documents (List[Dict]): List of documents to insert.
        Output:
            - List[Any]: List of IDs of the inserted documents.
        """
        return self.db[collectionName].insert_many(documents).inserted_ids

    def updateOne(self, collectionName: str, query: Dict, newValues: Dict) -> int:
        """
        Update a single document in a collection.
        Input:
            - collectionName (str): Name of the collection.
            - query (Dict): Query to find the document to update.
            - newValues (Dict): Fields to update.
        Output:
            - int: The number of documents modified (1 or 0).
        """
        result = self.db[collectionName].update_one(query, {"$set": newValues})
        return result.modified_count

    def updateMany(self, collectionName: str, query: Dict, newValues: Dict) -> int:
        """
        Update multiple documents in a collection.
        Input:
            - collectionName (str): Name of the collection.
            - query (Dict): Query to find documents to update.
            - newValues (Dict): Fields to update.
        Output:
            - int: The number of documents modified.
        """
        result = self.db[collectionName].update_many(query, {"$set": newValues})
        return result.modified_count

    def deleteOne(self, collectionName: str, query: Dict) -> int:
        """
        Delete a single document from a collection.
        Input:
            - collectionName (str): Name of the collection.
            - query (Dict): Query to find the document to delete.
        Output:
            - int: The number of documents deleted (1 or 0).
        """
        result = self.db[collectionName].delete_one(query)
        return result.deleted_count

    def deleteMany(self, collectionName: str, query: Dict) -> int:
        """
        Delete multiple documents from a collection.
        Input:
            - collectionName (str): Name of the collection.
            - query (Dict): Query to find documents to delete.
        Output:
            - int: The number of documents deleted.
        """
        result = self.db[collectionName].delete_many(query)
        return result.deleted_count

# usage of class 
def main():
    # Initialize MongoDBManager instance
    mongoManager = MongoDBManager()
    
    # Connect to MongoDB
    mongoManager.connect()
    
    try:
        # Example: Insert a single document
        print("Inserting a single document...")
        document = {"name": "John Doe", "age": 30, "city": "New York"}
        insertedId = mongoManager.insertOne("users", document)
        print(f"Inserted document ID: {insertedId}")
        
        # Example: Insert multiple documents
        print("Inserting multiple documents...")
        documents = [
            {"name": "Jane Doe", "age": 28, "city": "Chicago"},
            {"name": "Alice", "age": 35, "city": "San Francisco"}
        ]
        insertedIds = mongoManager.insertMany("users", documents)
        print(f"Inserted document IDs: {insertedIds}")
        
        # Example: Retrieve all documents
        print("Retrieving all documents...")
        allDocuments = mongoManager.getCollection("users")
        print(f"All documents: {allDocuments}")
        
        # Example: Retrieve a single document
        print("Retrieving a single document...")
        query = {"name": "John Doe"}
        singleDocument = mongoManager.getOne("users", query)
        print(f"Single document: {singleDocument}")
        
        # Example: Update a single document
        print("Updating a single document...")
        updateQuery = {"name": "John Doe"}
        newValues = {"city": "Boston"}
        updatedCount = mongoManager.updateOne("users", updateQuery, newValues)
        print(f"Number of documents updated: {updatedCount}")
        
        # Example: Update multiple documents
        print("Updating multiple documents...")
        multiUpdateQuery = {"city": "Chicago"}
        newValues = {"state": "Illinois"}
        updatedCount = mongoManager.updateMany("users", multiUpdateQuery, newValues)
        print(f"Number of documents updated: {updatedCount}")
        
        # Example: Delete a single document
        print("Deleting a single document...")
        deleteQuery = {"name": "Alice"}
        deletedCount = mongoManager.deleteOne("users", deleteQuery)
        print(f"Number of documents deleted: {deletedCount}")
        
        # Example: Delete multiple documents
        print("Deleting multiple documents...")
        multiDeleteQuery = {"city": "Boston"}
        deletedCount = mongoManager.deleteMany("users", multiDeleteQuery)
        print(f"Number of documents deleted: {deletedCount}")
    
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        # Disconnect from MongoDB
        mongoManager.disconnect()

