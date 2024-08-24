import logging
from endpoints import get_endpoints_data, get_auth, save_to_duck_db
import os
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)

load_dotenv()

auth_url = os.getenv("AUTH_URL")
base_url = os.getenv("BASE_URL")
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
website_id = os.getenv("WEBSITE_ID")
base_url = os.getenv("BASE_URL")

if __name__ == "__main__":
    bearer = get_auth(auth_url, client_id, client_secret)

    endpoints = ["sessions", "events", "query"]

    for endpoint in endpoints:
        get_endpoints_data(base_url, endpoint, website_id, bearer)
        save_to_duck_db(endpoint)
