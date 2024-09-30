import json

import httpx
from dotenv import dotenv_values

config = dotenv_values(".env")

class SpotifyClient:
    def __init__(self) -> None:
        self.__verify_env()
        self.access_token = self.__get_access_token()
        self.result = []

    def __verify_env(self):
        for key, value in config.items():
            if not value:
                raise RuntimeError(f"{key} environment variable is empty")

    def __get_access_token(self):
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
            print(exception)

    def get_playlist(self):
        url = f"https://api.spotify.com/v1/playlists/{config["PLAYLIST_ID"]}/tracks"

        try:
            while True:
                response = httpx.get(
                    url,
                    headers={"Authorization": f"Bearer {self.access_token}"},
                )
                response.raise_for_status()

                filtered_response = [item["track"] for item in response.json()["items"]]
                for track in filtered_response:
                    self.result.append(
                        {
                            "name": track["name"],
                            'artists': [artist["name"] for artist in track["artists"]],
                            'album': track["album"]["name"]
                        }
                    )

                if not response.json()["next"]:
                    print(len(self.result))
                    break

                url = response.json()["next"]
        except httpx.HTTPStatusError as exception:
            print(exception)

    def export_as_json(self):
        with open("result.json", "w") as file:
            json.dump(self.result, file, indent=4, ensure_ascii=False)

client = SpotifyClient()
client.get_playlist()
client.export_as_json()
