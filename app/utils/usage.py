from pymongo import MongoClient
import sys
sys.path.append('/Users/kenz/Documents/Multi-language video/system-info')

from app.database.MongoDB_connect import MongoDBManager
import logging
import os

logger = logging.getLogger(__name__)

class MediaCounter(MongoDBManager):
    """
    A class derived from MongoDBManager that provides specific functionality to count different types of media and tokens.
    """
    
    def CountTotalTokens(self, collectionName: str) -> int:
        """
        Count the total number of tokens in a collection.
        Input:
            - collectionName (str): Name of the collection.
        Output:
            - int: The total number of tokens in the collection.
        """
        return self.db[collectionName].count_documents({})

    def CountTokensByUser(self, collectionName: str, userId: int) -> int:
        """
        Count the number of tokens associated with a specific user ID.
        Input:
            - collectionName (str): Name of the collection.
            - userId (int): User ID to filter tokens.
        Output:
            - int: The number of tokens associated with the given user ID.
        """
        query = {"UserId": userId}
        return self.db[collectionName].count_documents(query)
    
    def CountTokensByDescription(self, collectionName: str, description: str) -> int:
        """
        Count the number of tokens with a specific description in a collection.
        Input:
            - collectionName (str): Name of the collection.
            - description (str): Description of the tokens to count.
        Output:
            - int: The number of tokens with the specified description.
        """
        query = {"Description": description}
        return self.db[collectionName].count_documents(query)

    def CountAllDescriptions(self, collectionName: str):
        """
        Count the number of tokens for each specific description in a collection.
        Input:
            - collectionName (str): Name of the collection.
        Output:
            - Dict: A dictionary with descriptions as keys and counts as values.
        """
        descriptions = ["Speech to text", "Text to text", "Text to speech", "Voice cloning", "Lipsync", "Fullpipeline"]
        counts = {}
        for description in descriptions:
            counts[description] = self.CountTokensByDescription(collectionName, description)
        return counts

def main():
    media_counter = MediaCounter()
    media_counter.connect()

    # Insert some sample data into the 'media' collection
    documents = [
        {"UserId": 1, "Description": "Text to text", "Status": "normal", "Timestamp": 170003432, "Reason": None},
        # {"UserId": 123, "Description": "Voice cloning", "Status": "success", "Timestamp": 170003699, "Reason": None},
        # {"UserId": 123, "Description": "Text to speech", "Status": "failed", "Timestamp": 170003900, "Reason": "video duration is higher than 15 minutes"},
        # {"UserId": 123, "Description": "Lipsync", "Status": "failed", "Timestamp": 170003900, "Reason": "video duration is higher than 15 minutes"},
        # {"UserId": 123, "Description": "Fullpipeline", "Status": "success", "Timestamp": 170003699, "Reason": None},
    ]

    collection_name = "usage"
    media_counter.insertMany(collection_name, documents)

    # Execute counting functions
    print("Total tokens:", media_counter.CountTotalTokens(collection_name))
    print("Tokens by User 1:", media_counter.CountTokensByUser(collection_name, 1))
    print("Tokens by description 'Voice cloning':", media_counter.CountTokensByDescription(collection_name, "Voice cloning"))
    print("Count of all descriptions:", media_counter.CountAllDescriptions(collection_name))

    media_counter.disconnect()

    # Print current working directory
    # print("Current Working Directory: ", os.getcwd())

if __name__ == "__main__":
    main()