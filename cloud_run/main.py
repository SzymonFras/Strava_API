from prepare_data import prepare_data
import bigquery_functions as bq
def sync_strava_activities(request):
    try:
        df_new = prepare_data()
        if not df_new.empty:
            print(f"Wstawiam {len(df_new)} wierszy do BQ")
            bq.upsert_activities(df_new)
        else:
            print("Brak nowych danych do wstawienia")

        return {"status": "ok", "new_rows": len(df_new)}
    except Exception as e:
        print(f"BŁĄD: {str(e)}") # To pojawi się w Logs Explorer
        return {"status": "error", "message": str(e)}, 500
