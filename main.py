import json

import httpx

from config import config, get_access_token

result = []

url = f"https://api.spotify.com/v1/playlists/{config["PLAYLIST_ID"]}/tracks"

try:
    while True:
        response = httpx.get(
            url,
            headers={"Authorization": f"Bearer {get_access_token()}"},
        )
        response.raise_for_status()

        filtered_response = [item["track"] for item in response.json()["items"]]
        for track in filtered_response:
            result.append(
                {
                    "name": track["name"],
                    'artists': [artist["name"] for artist in track["artists"]],
                    'album': track["album"]["name"]
                }
            )

        if not response.json()["next"]:
            print(len(result))
            break

        url = response.json()["next"]
except httpx.HTTPStatusError as exception:
    print(exception)

with open("result.json", "w") as file:
    json.dump(result, file, indent=4, ensure_ascii=False)
