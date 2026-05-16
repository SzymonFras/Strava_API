from google.cloud import bigquery
import google.auth
import os
from dotenv import load_dotenv
load_dotenv()
credentials, project_id = google.auth.default()
DATASET_NAME = os.getenv('BQ_DATASET', 'strava')
def client():
    client = bigquery.Client()
    return client
def table(project_id = project_id, DATASET_NAME = DATASET_NAME):
    table_id = f"`{project_id}.{DATASET_NAME}.activities_v1`"
    return table_id
def table_stage(project_id = project_id, DATASET_NAME = DATASET_NAME):
    table_id = f"`{project_id}.{DATASET_NAME}.activities_staging`"
    return table_id
def get_date(client=client()):
    query = f"""SELECT max(start_date_local) as max_date FROM `{project_id}.{DATASET_NAME}.activities_v1`"""
    try:
        result = client.query(query).result()
        row = next(result)
        if row.max_date:
            return row.max_date
        return "2010-01-01T00:00:00Z"
    except:
        return "2010-01-01T00:00:00Z"
def upsert_activities(df,client=client(),staging_table=table_stage(),target_table=table()):
    target_table = target_table.replace("`", "")
    staging_table = staging_table.replace("`", "")
    client.load_table_from_dataframe(df, staging_table).result()
    merge_query = f"""
    MERGE `{target_table}` T
    USING `{staging_table}` S
    ON T.id = S.id
    WHEN NOT MATCHED THEN
      INSERT ROW
    """
    client.query(merge_query).result()

    client.query(f"TRUNCATE TABLE `{staging_table}`").result()

def setup_tables(client=client(), staging_table=table_stage(),target_table=table()):
    schema = [
        bigquery.SchemaField("id", bigquery.enums.SqlTypeNames.INT64),
        bigquery.SchemaField("moving_time", bigquery.enums.SqlTypeNames.INT64),
        bigquery.SchemaField("elapsed_time", bigquery.enums.SqlTypeNames.INT64),
        bigquery.SchemaField("achievement_count", bigquery.enums.SqlTypeNames.INT64),
        bigquery.SchemaField("kudos_count", bigquery.enums.SqlTypeNames.INT64),
        bigquery.SchemaField("comment_count", bigquery.enums.SqlTypeNames.INT64),
        bigquery.SchemaField("athlete_count", bigquery.enums.SqlTypeNames.INT64),
        bigquery.SchemaField("photo_count", bigquery.enums.SqlTypeNames.INT64),
        bigquery.SchemaField("pr_count", bigquery.enums.SqlTypeNames.INT64),
        bigquery.SchemaField("total_photo_count", bigquery.enums.SqlTypeNames.INT64),
        bigquery.SchemaField("workout_type", bigquery.enums.SqlTypeNames.INT64),
        bigquery.SchemaField("distance", bigquery.enums.SqlTypeNames.FLOAT64),
        bigquery.SchemaField("total_elevation_gain", bigquery.enums.SqlTypeNames.FLOAT64),
        bigquery.SchemaField("average_speed", bigquery.enums.SqlTypeNames.FLOAT64),
        bigquery.SchemaField("max_speed", bigquery.enums.SqlTypeNames.FLOAT64),
        bigquery.SchemaField("average_cadence", bigquery.enums.SqlTypeNames.FLOAT64),
        bigquery.SchemaField("average_temp", bigquery.enums.SqlTypeNames.FLOAT64),
        bigquery.SchemaField("average_watts", bigquery.enums.SqlTypeNames.FLOAT64),
        bigquery.SchemaField("max_watts", bigquery.enums.SqlTypeNames.FLOAT64),
        bigquery.SchemaField("weighted_average_watts", bigquery.enums.SqlTypeNames.FLOAT64),
        bigquery.SchemaField("kilojoules", bigquery.enums.SqlTypeNames.FLOAT64),
        bigquery.SchemaField("elev_high", bigquery.enums.SqlTypeNames.FLOAT64),
        bigquery.SchemaField("elev_low", bigquery.enums.SqlTypeNames.FLOAT64),
        bigquery.SchemaField("average_heartrate", bigquery.enums.SqlTypeNames.FLOAT64),
        bigquery.SchemaField("max_heartrate", bigquery.enums.SqlTypeNames.FLOAT64),
        bigquery.SchemaField("suffer_score", bigquery.enums.SqlTypeNames.FLOAT64),
        bigquery.SchemaField("name", bigquery.enums.SqlTypeNames.STRING),
        bigquery.SchemaField("type", bigquery.enums.SqlTypeNames.STRING),
        bigquery.SchemaField("sport_type", bigquery.enums.SqlTypeNames.STRING),
        bigquery.SchemaField("timezone", bigquery.enums.SqlTypeNames.STRING),
        bigquery.SchemaField("visibility", bigquery.enums.SqlTypeNames.STRING),
        bigquery.SchemaField("gear_id", bigquery.enums.SqlTypeNames.STRING),
        bigquery.SchemaField("trainer", bigquery.enums.SqlTypeNames.BOOL),
        bigquery.SchemaField("commute", bigquery.enums.SqlTypeNames.BOOL),
        bigquery.SchemaField("manual", bigquery.enums.SqlTypeNames.BOOL),
        bigquery.SchemaField("flagged", bigquery.enums.SqlTypeNames.BOOL),
        bigquery.SchemaField("device_watts", bigquery.enums.SqlTypeNames.BOOL),
        bigquery.SchemaField("start_date_local", bigquery.enums.SqlTypeNames.TIMESTAMP),
        bigquery.SchemaField("start_latlng", bigquery.enums.SqlTypeNames.GEOGRAPHY),
        bigquery.SchemaField("end_latlng", bigquery.enums.SqlTypeNames.GEOGRAPHY),
    ]
    target_table= target_table.replace("`", "")
    staging_table = staging_table.replace("`", "")
    for table_id in [target_table, staging_table]:
        bq_table = bigquery.Table(table_id, schema=schema)
        bq_table = client.create_table(bq_table, exists_ok=True)
        print(f"INFO: Table {table_id} was created or existed")