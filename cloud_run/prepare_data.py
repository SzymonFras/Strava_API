import api_strava as strava
import bigquery_functions as bq
from config import strava_keys
def prepare_data():
    CLIENT_ID,CLIENT_SECRET,REFRESH_TOKEN = strava_keys()
    token = strava.get_access_token(CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN)
    df = strava.load_data(token,after_date=bq.get_date())
    return df
