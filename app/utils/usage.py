from pymongo import MongoClient
import logging

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

    def CounTokensByUser(self, collectionName: str, userId: int) -> int:
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
