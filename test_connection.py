"""
Test script: verify that the Twitch API connection works
Run with: python3 test_connection.py
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
CLIENT_SECRET = os.getenv("TWITCH_CLIENT_SECRET")

if not CLIENT_ID or not CLIENT_SECRET:
    raise ValueError("Missing CLIENT_ID or CLIENT_SECRET. Check your .env file.")
    


def get_access_token():
    """
    Step 1: exchange Client ID + Client Secret for an access token.
    Twitch API requires this token before calling any other endpoint.
    """
    url = "https://id.twitch.tv/oauth2/token"
    params = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials",
    }
    response = requests.post(url, params=params)
    response.raise_for_status()  # raises an error if the request failed
    return response.json()["access_token"]


def get_top_streams(access_token, first=5):
    """
    Step 2: use the token to call the Twitch API and fetch
    data for the top live streams.
    """
    url = "https://api.twitch.tv/helix/streams"
    headers = {
        "Client-Id": CLIENT_ID,
        "Authorization": f"Bearer {access_token}",
    }
    params = {"first": first}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()["data"]


if __name__ == "__main__":
    print("Fetching access token...")
    token = get_access_token()
    print("Access token acquired!\n")

    print("Fetching top live streams...")
    streams = get_top_streams(token)

    print(f"\nSuccessfully retrieved {len(streams)} stream(s):\n")
    for s in streams:
        print(f"Streamer: {s['user_name']:<20} Category: {s['game_name']:<20} Viewers: {s['viewer_count']}")