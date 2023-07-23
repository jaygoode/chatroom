import requests


def get_access_token(client_id, client_secret, code, redirect_uri):
    token_url = "https://eu.battle.net/oauth/token"
    payload = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "redirect_uri": redirect_uri
    }

    response = requests.post(token_url, data=payload)

    if response.status_code == 200:
        data = response.json()
        access_token = data.get("access_token")
        if access_token:
            return access_token
        else:
            print("Access token not found in response.")
    else:
        print(
            f"Failed to obtain access token. Error code: {response.status_code}")
        return None


def search_item(api_key, item_name):
    base_url = f"eu.api.blizzard.com"
    namespace = "static-eu"
    locale = "en_EU"

    item_search_url = f"{base_url}/data/wow/search/item"
    headers = {"Authorization": f"Bearer {api_key}"}

    params = {
        "namepace": namespace,
        "locale": locale,
        "name.en_EU": item_name
    }

    response = requests.get(item_search_url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        if "results" in data and data["results"]:
            for result in data["results"]:
                print(
                    f"Item ID: {result['data']['id']}, Name: {result['data']['name']['en_US']}")
            else:
                print("no item found with the given name.")
        else:
            print(
                f"Failed to retrieve data Error code: {response.status_code}")


if __name__ == "__main__":
    # Replace these values with your own credentials and settings
    CLIENT_ID = "YOUR_CLIENT_ID"
    CLIENT_SECRET = "YOUR_CLIENT_SECRET"
    AUTHORIZATION_CODE = "THE_AUTHORIZATION_CODE_RECEIVED_AFTER_USER_GRANT"
    REDIRECT_URI = "YOUR_REDIRECT_URI"

    access_token = get_access_token(
        CLIENT_ID, CLIENT_SECRET, AUTHORIZATION_CODE, REDIRECT_URI)

    if access_token:
        print(f"Access Token: {access_token}")
        API_KEY = "YOUR_API_KEY_HERE"
        # Replace this with the item name you want to search for
        item_name_to_search = "Shadowmourne"
        search_item(API_KEY, item_name_to_search)
