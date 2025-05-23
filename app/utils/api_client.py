import json
import requests


def fetch_users_from_api(amount: int) -> list[dict]:
    # raises requests.exceptions.HTTPError, requests.exceptions.JSONDecodeError, KeyError
    BASE_API_URL = 'https://randomuser.me/api/'

    response = requests.get(
        url=BASE_API_URL,
        params={
            'results': amount
        }
    )
    response.raise_for_status()

    return response.json()["results"]
