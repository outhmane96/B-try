from btry.api import FantasyAPI
from btry.utilities.dynamodb_handler import DynamoDBHandler
from loguru import logger

def lambda_handler(event, context):
    # Initialize FantasyAPI
    fantasy_api = FantasyAPI()

    # Initialize DynamoDB Handler
    dynamo_handler = DynamoDBHandler(table_name="FantasyPlayersData")

    try:
        # Fetch all players using FantasyAPI
        logger.info("Fetching players data...")
        players = fantasy_api.get_players()

        logger.info(f"Fetched {len(players)} players from the Fantasy API.")

        # Insert each player into DynamoDB
        # for player in players:
        #     # Insert the full player JSON into DynamoDB
        #     dynamo_handler.insert_document(player)
        #     logger.info(f"Inserted player {player['web_name']} (ID: {player['id']}) into DynamoDB.")
            
        dynamo_handler.insert_documents_batch(players)
        

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise
    return {"statusCode": 200, "body": f"Successfully processed {len(players)} players."}

    #return {"statusCode": 200, "body": "All player data successfully inserted into DynamoDB."}
