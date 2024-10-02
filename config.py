import httpx
from dotenv import dotenv_values

config = dotenv_values(".env")


for key, value in config.items():
    if not value:
        raise RuntimeError(f"{key} environment variable is empty")


def get_access_token():
    try:
        response = httpx.post(
            "https://accounts.spotify.com/api/token",
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
            },
            data={
                "grant_type": "client_credentials",
                "client_id": config["CLIENT_ID"],
                "client_secret": config["CLIENT_SECRET"],
            },
        )
        response.raise_for_status()
        return response.json()["access_token"]
    except httpx.HTTPStatusError as exception:
        print(exception.response.text)
