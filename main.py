from os import environ

import httpx
from dotenv import load_dotenv

load_dotenv()


def get_access_token():
    response = httpx.post(
        "https://accounts.spotify.com/api/token",
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data={
            "grant_type": "client_credentials",
            "client_id": environ["CLIENT_ID"],
            "client_secret": environ["CLIENT_SECRET"],
        },
    )

    return response.json()["access_token"]


access_token = get_access_token()
