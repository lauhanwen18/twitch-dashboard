"""
Collect a snapshot of Twitch live stream data and store it in the database.
Run with: python3 collect_data.py
"""

import os
import sqlite3
from datetime import datetime, timezone

import requests
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
CLIENT_SECRET = os.getenv("TWITCH_CLIENT_SECRET")
DB_PATH = "twitch_data.db"

if not CLIENT_ID or not CLIENT_SECRET:
    raise ValueError("Missing CLIENT_ID or CLIENT_SECRET. Check your .env file.")


def get_access_token():
    """Exchange Client ID + Client Secret for an access token."""
    url = "https://id.twitch.tv/oauth2/token"
    params = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials",
    }
    response = requests.post(url, params=params)
    response.raise_for_status()
    return response.json()["access_token"]


def get_top_streams(access_token, total=100):
    """
    Fetch live stream data from Twitch, handling pagination.
    Twitch returns max 100 results per page, so we page through
    using the 'cursor' value until we hit our target count.
    """
    url = "https://api.twitch.tv/helix/streams"
    headers = {
        "Client-Id": CLIENT_ID,
        "Authorization": f"Bearer {access_token}",
    }

    streams = []
    cursor = None

    while len(streams) < total:
        params = {"first": min(100, total - len(streams))}
        if cursor:
            params["after"] = cursor

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        payload = response.json()

        streams.extend(payload["data"])

        cursor = payload.get("pagination", {}).get("cursor")
        if not cursor:
            break  # no more pages available

    return streams


def save_snapshot(streams):
    """Insert the collected streams into the database as one snapshot."""
    snapshot_time = datetime.now(timezone.utc).isoformat()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    rows = [
        (
            snapshot_time,
            s["id"],
            s["user_name"],
            s["game_name"],
            s["viewer_count"],
            s["title"],
            s["language"],
            ",".join(s.get("tags", [])),
            s["started_at"],
        )
        for s in streams
    ]

    cursor.executemany(
        """
        INSERT INTO twitch_stream_snapshots (
            snapshot_time, stream_id, streamer_name, category_name,
            viewer_count, stream_title, language, tags, stream_started_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        rows,
    )

    conn.commit()
    conn.close()

    return len(rows)


if __name__ == "__main__":
    print("Fetching access token...")
    token = get_access_token()

    print("Collecting live stream data...")
    streams = get_top_streams(token, total=100)
    print(f"Retrieved {len(streams)} streams from the Twitch API.")

    print("Saving snapshot to database...")
    saved_count = save_snapshot(streams)
    print(f"Saved {saved_count} rows to twitch_stream_snapshots.")