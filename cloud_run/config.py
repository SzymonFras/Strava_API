import google.auth
from google.cloud import secretmanager
def get_secret(secret_name):
    credentials, project_id = google.auth.default()
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

def strava_keys():
    return get_secret("strava_client_id"), get_secret("strava_client_secret"), get_secret("strava_refresh_token")
    
