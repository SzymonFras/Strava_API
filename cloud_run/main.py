from prepare_data import prepare_data
import bigquery_functions as bq
def sync_strava_activities(request):
    try:
        bq.setup_tables()
        df_new = prepare_data()
        if not df_new.empty:
            print(f"Insert {len(df_new)} rows")
            bq.upsert_activities(df_new)
        else:
            print("No new activities to insert")

        return {"status": "ok", "new_rows": len(df_new)}
    except Exception as e:
        print(f"Error: {str(e)}")
        return {"status": "error", "message": str(e)}, 500
if __name__ == "__main__":
    class MockRequest:
        def __init__(self):
            self.args = {}
    result = sync_strava_activities(MockRequest())