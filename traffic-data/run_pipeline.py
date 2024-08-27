from endpoints import get_endpoints_data, get_auth, save_to_duck_db
import os

auth_url = os.environ["AUTH_URL"]
base_url = os.environ["BASE_URL"]
client_id = os.environ["CLIENT_ID"]
client_secret = os.environ["CLIENT_SECRET"]
website_id = os.environ["WEBSITE_ID"]
base_url = os.environ["BASE_URL"]

if __name__ == "__main__":
    bearer = get_auth(auth_url, client_id, client_secret)

    endpoints = ["sessions", "events", "query"]

    for endpoint in endpoints:
        get_endpoints_data(base_url, endpoint, website_id, bearer)
        save_to_duck_db(endpoint)
