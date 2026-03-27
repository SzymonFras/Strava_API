from google.cloud import bigquery
def client():
    client = bigquery.Client()
    return client
def table(table_id= `{project_id}.dataset.table_main`):
    return table_id
def table_stage(table_id= `{project_id}.dataset.table_staging`):
    return table_id
def get_date(client=client()):
    query = """SELECT max(start_date_local) as max_date FROM `{project_id}.dataset.table_main`"""
    result = client.query(query).result()
    return next(result).max_date
def upsert_activities(df,client=client(),staging_table=table_stage(),target_table=table()):
    client.load_table_from_dataframe(df, staging_table).result()

    # 2. MERGE do target: tylko nowe id
    merge_query = f"""
    MERGE `{target_table}` T
    USING `{staging_table}` S
    ON T.id = S.id
    WHEN NOT MATCHED THEN
      INSERT ROW
    """
    client.query(merge_query).result()

    # 3. Opróżnij staging
    client.query(f"TRUNCATE TABLE `{staging_table}`").result()