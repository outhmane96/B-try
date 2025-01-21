import boto3
from botocore.exceptions import ClientError
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

    def insert_document(self, document):
        """
        Insert a single document into the DynamoDB table.
        :param document: The document to insert (as a dictionary).
        :return: The response from DynamoDB.
        """
        try:
            response = self.table.put_item(Item=document)
            logger.info(f"Document inserted: {document}")
            return response
        except ClientError as e:
            logger.error(f"Failed to insert document: {e}")
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
