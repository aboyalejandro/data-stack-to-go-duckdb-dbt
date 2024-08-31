import duckdb
import os
import pandas as pd
import logging
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Set up logging
logging.basicConfig(level=logging.INFO)

# Connect to DuckDB
conn = duckdb.connect(database=os.environ["DUCKDB_PATH"])
# List of tables to query
tables = ["traffic_performance", "attribution", "visitors_snapshot", "visitors"]

# Query each table and save as CSV
for table in tables:
    df = conn.execute(f"SELECT * FROM {table}").fetchdf()
    path = "exports/"
    csv_file_name = f"{table}.csv"
    df.to_csv(path + csv_file_name, index=False)
    print(f"Saved {csv_file_name}")

conn.close()


# Set up credentials
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SERVICE_ACCOUNT_FILE = os.environ["SERVICE_ACCOUNT_JSON"]

try:
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
except Exception as e:
    logging.error(f"Error with authentication: {e}")
    exit(1)

# The ID of your spreadsheet
SPREADSHEET_ID = os.environ["SPREADSHEET_ID"]
service = build("sheets", "v4", credentials=creds)
sheet = service.spreadsheets()

# List of tables (CSV files)
tables = ["traffic_performance", "attribution", "visitors_snapshot", "visitors"]

# Read each CSV file and upload to Google Sheets
for table in tables:
    path = "exports/"
    csv_file_name = f"{table}.csv"

    # Read the CSV file
    try:
        df = pd.read_csv(path + csv_file_name)
        logging.info(f"Successfully read {csv_file_name}.")
    except FileNotFoundError:
        logging.error(f"File {csv_file_name} not found. Skipping.")
        continue
    except Exception as e:
        logging.error(f"Error reading {csv_file_name}: {e}")
        continue

    # Handle NaN values by converting them to empty strings
    df = df.where(pd.notnull(df), "")

    # Check if the worksheet already exists
    existing_sheets = []
    try:
        spreadsheet = sheet.get(spreadsheetId=SPREADSHEET_ID).execute()
        existing_sheets = {
            s["properties"]["title"]: s["properties"]["sheetId"]
            for s in spreadsheet["sheets"]
        }
    except HttpError as e:
        logging.error(f"Error accessing spreadsheet: {e}")
        continue

    # Check if the sheet already exists
    if table in existing_sheets:
        logging.info(f"Sheet '{table}' already exists. Overriding data.")
        worksheet_id = existing_sheets[table]
    else:
        # Create a new worksheet if it doesn't exist
        worksheet_body = {"properties": {"title": table}}
        response = sheet.batchUpdate(
            spreadsheetId=SPREADSHEET_ID,
            body={"requests": [{"addSheet": worksheet_body}]},
        ).execute()
        worksheet_id = response["replies"][0]["addSheet"]["properties"]["sheetId"]
        logging.info(f"Created new sheet '{table}'.")

    # Update the worksheet with the DataFrame data
    values = [df.columns.tolist()] + df.values.tolist()
    body = {"values": values}
    sheet.values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=f"{table}!A1",  # Specify the range to start updating from A1
        valueInputOption="RAW",
        body=body,
    ).execute()
    logging.info(f"Uploaded {csv_file_name} to Google Sheets tab '{table}'")
