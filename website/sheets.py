import gspread
import json
import os
from google.oauth2.service_account import Credentials

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


def get_sheet(tab_name):
    creds_json = os.environ.get('GOOGLE_CREDENTIALS_JSON', '')
    sheet_id = os.environ.get('GOOGLE_SHEETS_ID', '')
    if not creds_json or not sheet_id:
        return None
    creds = Credentials.from_service_account_info(json.loads(creds_json), scopes=SCOPES)
    client = gspread.authorize(creds)
    return client.open_by_key(sheet_id).worksheet(tab_name)


def log_to_sheets(tab_name, row_data):
    """Agrega una fila al tab especificado. Silencioso si falla."""
    try:
        sheet = get_sheet(tab_name)
        if sheet:
            sheet.append_row(row_data, value_input_option='USER_ENTERED')
            print(f"✅ Google Sheets: fila agregada en '{tab_name}'")
    except Exception as e:
        print(f"⚠️ Google Sheets error ({tab_name}): {str(e)}")
