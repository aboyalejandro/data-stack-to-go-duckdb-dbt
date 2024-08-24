import requests
import json
import pandas as pd
import duckdb
import os
import logging


def get_auth(url, client_id, client_secret):
    logging.info(f"Authenticating to website...")
    headers = {"Content-Type": "application/json"}

    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    bearer = response.json()["access_token"]
    return bearer


def get_payload(endpoint, website_id):

    if endpoint == "sessions":
        return json.dumps(
            {
                "website_id": website_id,
                "columns": [
                    {"column_id": "visitor_session_number"},
                    {"column_id": "visitor_returning"},
                    {"column_id": "source_medium"},
                    {"column_id": "campaign_name"},
                    {"column_id": "session_goals"},
                    {"column_id": "session_total_page_views"},
                    {"column_id": "session_total_events"},
                    {"column_id": "visitor_days_since_last_session"},
                    {"column_id": "visitor_days_since_first_session"},
                    {"column_id": "location_country_name"},
                ],
                "date_from": "2021-01-01",
                "date_to": "2021-03-30",
                "filters": {"operator": "and", "conditions": []},
                "offset": 0,
                "limit": 10000,
                "format": "json",
            }
        )
    elif endpoint == "events":
        return json.dumps(
            {
                "website_id": website_id,
                "columns": [
                    {"column_id": "event_index"},
                    {"column_id": "page_view_index"},
                    {"column_id": "custom_event_category"},
                    {"column_id": "custom_event_action"},
                    {"column_id": "custom_event_name"},
                    {"column_id": "event_url"},
                    {"column_id": "source_medium"},
                    {"column_id": "campaign_name"},
                    {"column_id": "goal_id"},
                ],
                "date_from": "2021-01-01",
                "date_to": "2021-03-30",
                "filters": {"operator": "and", "conditions": []},
                "offset": 0,
                "limit": 10000,
                "format": "json",
            }
        )
    else:
        return json.dumps(
            {
                "date_from": "2021-01-01",
                "date_to": "2021-03-30",
                "website_id": website_id,
                "offset": 0,
                "limit": 10000,
                "columns": [
                    {"transformation_id": "to_date", "column_id": "timestamp"},
                    {"column_id": "referrer_type"},
                    {"column_id": "source_medium"},
                    {"column_id": "campaign_name"},
                    {"column_id": "campaign_content"},
                    {"column_id": "session_entry_url"},
                    {"column_id": "visitor_returning"},
                    {"column_id": "location_country_name"},
                    {"column_id": "operating_system"},
                    {"column_id": "device_type"},
                    {"column_id": "location_city_name"},
                    {"column_id": "events"},
                    {"column_id": "visitors"},
                    {"column_id": "sessions"},
                    {"column_id": "page_views"},
                    {"column_id": "ecommerce_conversions"},
                    {"column_id": "cart_additions"},
                    {"column_id": "ecommerce_abandoned_carts"},
                    {"column_id": "consents_none"},
                    {"column_id": "consents_full"},
                ],
            }
        )


def save_to_duck_db(table_name):
    # Define the path to the files directory
    files_path = "files/"

    # Check if the directory exists
    if not os.path.exists(files_path):
        logging.error(f"The directory {files_path} does not exist.")
        return

    # Filter the list to include only .csv files
    files = [file for file in os.listdir(files_path) if file.endswith(".csv")]

    if not files:
        logging.info(f"No CSV files found in {files_path}")
        return

    logging.info("Converting CSV files into DuckDB tables.")
    con = duckdb.connect(f'{os.getenv("DUCKDB_PATH")}')

    for file in files:
        file_path = os.path.join(files_path, file)

        try:
            con.execute(
                f"CREATE OR REPLACE TABLE {table_name} AS (SELECT * FROM read_csv_auto('{file_path}', delim=',', header=true))"
            )
            logging.info(f"Table {table_name} created in DuckDB using {file}.")
        except Exception as e:
            logging.error(f"Error creating table {table_name} from {file}: {str(e)}")

    con.close()


def get_endpoints_data(url, endpoint, website_id, bearer):
    logging.info(f"Getting payload for {endpoint} endpoint...")
    payload = get_payload(endpoint, website_id)
    url = url + endpoint + "/"
    logging.info(f"Constructed URL: {url}")
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {bearer}"}

    response = requests.request("POST", url, headers=headers, data=payload)

    column_names = response.json()["meta"]["columns"]
    data = pd.DataFrame(columns=column_names)
    data = pd.DataFrame.from_dict(response.json()["data"])
    data.columns = column_names

    logging.info(f"Saving {endpoint} DataFrame to CSV file.")
    data.to_csv(f"files/{endpoint}.csv", index=False)

    return data
