from btry.api import RapidAPI
from btry.utilities import get_var_from_env
from btry.utilities import MONGO_COLLECTIONS, MongoDBHandler
from loguru import logger

if __name__ == "__main__":
    rapid_api = RapidAPI()
    mongo_db_hangler = MongoDBHandler(
        connection_string = get_var_from_env(var_name="MONGO_CONNECTION_STRING"),
        database_name = get_var_from_env(var_name="MONGO_DB_NAME")
    )
    mongo_db_hangler.connect()
    # data = rapid_api.get_teams(league_id=39, season=2024)
    # mongo_db_hangler.insert_document(collection_name=MONGO_COLLECTIONS['teams'], document=data)
    teams = mongo_db_hangler.find_documents(collection_name=MONGO_COLLECTIONS['teams'])
    for team in teams[0]['response']:
        logger.info("Getting player of team", team['team']['name'])
        players = rapid_api.get_team_players(team_id=team["team"]["id"])
        mongo_db_hangler.insert_document(collection_name=MONGO_COLLECTIONS['players'], document=players)