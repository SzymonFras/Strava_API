from prepare_data import prepare_data
import bigquery_functions as bq
def sync_strava_activities(request):
    """
        Cloud Function: pobiera nowe aktywności ze Stravy od ostatniego start_date
        w BigQuery i wstawia je do głównej tabeli bez duplikatów.
        """
    # 1. Download new activities
    try:
        df_new = prepare_data()

    # 2. Jeśli są nowe wiersze, wrzuć do BigQuery
        if not df_new.empty:
            print(f"Wstawiam {len(df_new)} wierszy do BQ")
            bq.upsert_activities(df_new)
        else:
            print("Brak nowych danych do wstawienia")

        return {"status": "ok", "new_rows": len(df_new)}
    except Exception as e:
        print(f"BŁĄD: {str(e)}") # To pojawi się w Logs Explorer
        return {"status": "error", "message": str(e)}, 500
