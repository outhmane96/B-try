import boto3
from botocore.exceptions import ClientError
from decimal import Decimal
from loguru import logger


class DynamoDBHandler:
    def __init__(self, table_name):
        """
        Initialize the DynamoDBHandler with a table name.
        :param table_name: The name of the DynamoDB table to interact with.
        """
        self.table_name = table_name
        self.dynamodb = boto3.resource("dynamodb")
        self.table = self.dynamodb.Table(self.table_name)

    def _convert_floats_to_decimals(self, obj):
        """
        Recursively convert floats to Decimal in a nested object (dict or list).
        """
        if isinstance(obj, list):
            return [self._convert_floats_to_decimals(item) for item in obj]
        elif isinstance(obj, dict):
            return {k: self._convert_floats_to_decimals(v) for k, v in obj.items()}
        elif isinstance(obj, float):
            return Decimal(str(obj))  # Convert float to Decimal
        else:
            return obj

    def insert_document(self, document):
        """
        Insert a single document into the DynamoDB table.
        :param document: The document to insert (as a dictionary).
        :return: The response from DynamoDB.
        """
        try:
            # Convert id to string if it exists and is a number
            if "id" in document and isinstance(document["id"], (int, float)):
                document["id"] = str(document["id"])
            document = self._convert_floats_to_decimals(document)
            response = self.table.put_item(Item=document)
            logger.info(f"Document inserted: {document}")
            return response
        except ClientError as e:
            logger.error(f"Failed to insert document: {e}")
            raise
        
    def insert_documents_batch(self, documents):
        """
        Insert multiple documents into the DynamoDB table using batch_writer.
        :param documents: A list of documents to insert.
        """
        try:
            with self.table.batch_writer() as batch:
                for document in documents:
                    # Convert id to string if it exists and is a number
                    if "id" in document and isinstance(document["id"], (int, float)):
                        document["id"] = str(document["id"])
                    # Convert floats to Decimal
                    document = self._convert_floats_to_decimals(document)
                    # Add document to batch
                    batch.put_item(Item=document)
            logger.info(f"Batch inserted {len(documents)} documents.")
        except ClientError as e:
            logger.error(f"Failed to insert batch: {e}")
            raise



    def find_documents(self, query=None):
        """
        Retrieve documents from DynamoDB based on a query.
        :param query: Optional query (not used for simplicity; scans all items).
        :return: A list of matching documents.
        """
        try:
            response = self.table.scan()
            documents = response.get("Items", [])
            logger.info(f"Retrieved {len(documents)} documents.")
            return documents
        except ClientError as e:
            logger.error(f"Failed to retrieve documents: {e}")
            raise

    def update_document(self, key, update_data):
        """
        Update a document in the DynamoDB table.
        :param key: The key of the document to update (e.g., {"PlayerID": "123"}).
        :param update_data: The data to update.
        :return: The response from DynamoDB.
        """
        try:
            update_expression = "SET " + ", ".join(f"{k} = :{k}" for k in update_data.keys())
            expression_values = {f":{k}": v for k, v in update_data.items()}

            response = self.table.update_item(
                Key=key,
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_values,
                ReturnValues="UPDATED_NEW",
            )
            logger.info(f"Updated document with key {key}: {update_data}")
            return response
        except ClientError as e:
            logger.error(f"Failed to update document: {e}")
            raise
