import pandas as pd
import time
import json
import requests
import os
def get_access_token(client_id, client_secret, refresh_token):
    r = requests.post(
        "https://www.strava.com/oauth/token",
        data={
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token
        }
    )
    r.raise_for_status()
    return r.json()["access_token"]
def fetch_all_activities(token, after_date):
    #after = int(datetime.strptime(after_date, "%Y-%m-%d").timestamp())
    page = 1
    activities = []

    while True:
        r = requests.get(
            "https://www.strava.com/api/v3/athlete/activities",
            headers={"Authorization": f"Bearer {token}"},
            params={
                "after": after_date,
                "per_page": 200,
                "page": page
            }
        )
        r.raise_for_status()
        data = r.json()

        if not data:
            break

        activities.extend(data)
        page += 1
        time.sleep(1)  # rate limit safe

    return activities

def load_data(token,after_date='2014-01-01'):
    data = fetch_all_activities(token, after_date=after_date)
    data = pd.DataFrame(data)
    df = data.copy()
    df = prepare_df(df)
    return df
def prepare_df(df):
    int_cols = [
        "id", "moving_time", "elapsed_time",
        "achievement_count", "kudos_count", "comment_count",
        "athlete_count", "photo_count",
        "pr_count", "total_photo_count",
        "workout_type"
    ]

    for c in int_cols:
        df[c] = df[c].astype("Int64")
    float_cols = [
        "distance", "total_elevation_gain",
        "average_speed", "max_speed",
        "average_cadence", "average_temp",
        "average_watts", "max_watts",
        "weighted_average_watts",
        "kilojoules", "elev_high", "elev_low",
        "average_heartrate", "max_heartrate",
        "suffer_score"
    ]

    for c in float_cols:
        df[c] = df[c].astype("float64")
    string_cols = [
        "name", "type", "sport_type",
        "timezone", "visibility", "gear_id"
    ]

    for c in string_cols:
        df[c] = df[c].astype("string")
    bool_cols = [
        "trainer", "commute", "manual",
        "flagged", "device_watts"
    ]

    for c in bool_cols:
        df[c] = df[c].astype("bool")
    df["start_date_local"] = pd.to_datetime(df["start_date_local"], utc=True)
    df["start_latlng"] = df["start_latlng"].apply(latlng_to_wkt)
    df["start_latlng"] = (
        df["start_latlng"]
        .replace(["None", "null", "nan", ""], None)
    )
    df["start_latlng"] = df["start_latlng"].where(df["start_latlng"].notna(),None)
    df["end_latlng"] = df["end_latlng"].apply(latlng_to_wkt)
    df["end_latlng"] = df["end_latlng"].where(df["end_latlng"].notna(), None)
    df = df[
        [
            "id", "name", "distance", "moving_time", "elapsed_time",
            "total_elevation_gain", "type", "sport_type", "workout_type",
            "start_date_local", "timezone",
            "achievement_count", "kudos_count", "comment_count",
            "athlete_count", "photo_count",
            "trainer", "commute", "manual", "flagged",
            "visibility", "gear_id",
            "average_speed", "max_speed", "average_cadence", "average_temp",
            "average_watts", "max_watts", "weighted_average_watts",
            "device_watts", "kilojoules",
            "elev_high", "elev_low",
            "pr_count", "total_photo_count",
            "average_heartrate", "max_heartrate", "suffer_score",
            "start_latlng", "end_latlng"
        ]
    ]
    print(df.dtypes)
    return df
def latlng_to_wkt(val):
    if isinstance(val, list) and len(val) == 2:
        lat, lng = val
        return f"POINT({lng} {lat})"
    return None
