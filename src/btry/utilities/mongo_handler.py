from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
from loguru import logger

class MongoDBHandler:
    def __init__(self, connection_string, database_name):
        """
        Initialize the MongoDBHandler with a connection string and database name.

        :param connection_string: The MongoDB connection string (URI).
        :param database_name: The name of the database to interact with.
        """
        self.connection_string = connection_string
        self.database_name = database_name
        self.client = None
        self.db = None

    def connect(self):
        """
        Connect to the MongoDB database.

        :raises ConnectionFailure: If the connection to MongoDB fails.
        """
        try:
            self.client = MongoClient(self.connection_string)
            # The `server_info` call will trigger a connection attempt.
            self.client.server_info()
            self.db = self.client[self.database_name]
            logger.info("Connected to MongoDB successfully!")
        except ConnectionFailure as e:
            logger.exception(f"Failed to connect to MongoDB: {e}")
            raise

    def disconnect(self):
        """
        Disconnect from the MongoDB database.
        """
        if self.client:
            self.client.close()
            logger.info("Disconnected from MongoDB.")

    def insert_document(self, collection_name, document):
        """
        Insert a single document into a collection.

        :param collection_name: The name of the collection.
        :param document: The document to insert (as a dictionary).
        :return: The inserted document's ID.
        :raises OperationFailure: If the insert operation fails.
        """
        try:
            collection = self.db[collection_name]
            result = collection.insert_one(document)
            logger.info(f"Document inserted with ID: {result.inserted_id}")
            return result.inserted_id
        except OperationFailure as e:
            logger.exception(f"Failed to insert document: {e}")
            raise

    def find_documents(self, collection_name, query=None):
        """
        Find documents in a collection that match a query.

        :param collection_name: The name of the collection.
        :param query: The query to filter documents (default is None, which returns all documents).
        :return: A list of matching documents.
        :raises OperationFailure: If the find operation fails.
        """
        try:
            collection = self.db[collection_name]
            if query:
                documents = collection.find(query)
            else:
                documents = collection.find()
            return list(documents)
        except OperationFailure as e:
            logger.exception(f"Failed to find documents: {e}")
            raise

    def update_document(self, collection_name, query, update_data, upsert=False):
        """
        Update a document in a collection.

        :param collection_name: The name of the collection.
        :param query: The query to find the document to update.
        :param update_data: The data to update in the document.
        :param upsert: If True, insert a new document if no document matches the query (default is False).
        :return: The result of the update operation.
        :raises OperationFailure: If the update operation fails.
        """
        try:
            collection = self.db[collection_name]
            result = collection.update_one(query, {"$set": update_data}, upsert=upsert)
            logger.info(f"Matched {result.matched_count} document(s) and modified {result.modified_count} document(s).")
            return result
        except OperationFailure as e:
            logger.exception(f"Failed to update document: {e}")
            raise

    def delete_document(self, collection_name, query):
        """
        Delete a document from a collection.

        :param collection_name: The name of the collection.
        :param query: The query to find the document to delete.
        :return: The result of the delete operation.
        :raises OperationFailure: If the delete operation fails.
        """
        try:
            collection = self.db[collection_name]
            result = collection.delete_one(query)
            logger.info(f"Deleted {result.deleted_count} document(s).")
            return result
        except OperationFailure as e:
            logger.exception(f"Failed to delete document: {e}")
            raise

    def count_documents(self, collection_name, query=None):
        """
        Count the number of documents in a collection that match a query.

        :param collection_name: The name of the collection.
        :param query: The query to filter documents (default is None, which counts all documents).
        :return: The count of matching documents.
        :raises OperationFailure: If the count operation fails.
        """
        try:
            collection = self.db[collection_name]
            if query:
                count = collection.count_documents(query)
            else:
                count = collection.count_documents({})
            return count
        except OperationFailure as e:
            logger.exception(f"Failed to count documents: {e}")
            raise