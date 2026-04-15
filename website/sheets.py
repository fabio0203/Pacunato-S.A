import gspread
import json
import os
from google.oauth2.service_account import Credentials

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


def get_sheet(tab_name):
    creds_json = os.environ.get('GOOGLE_CREDENTIALS_JSON', '')
    sheet_id = os.environ.get('GOOGLE_SHEETS_ID', '')

    if not creds_json:
        print("⚠️ Google Sheets: GOOGLE_CREDENTIALS_JSON no configurado en Render")
        return None
    if not sheet_id:
        print("⚠️ Google Sheets: GOOGLE_SHEETS_ID no configurado en Render")
        return None

    # Fix: Render sometimes stores \\n instead of real \n in env vars,
    # which breaks the private_key field in the service account JSON.
    creds_json = creds_json.replace('\\n', '\n')

    try:
        creds_data = json.loads(creds_json)
    except json.JSONDecodeError as e:
        print(f"⚠️ Google Sheets: GOOGLE_CREDENTIALS_JSON no es JSON válido: {e}")
        return None

    creds = Credentials.from_service_account_info(creds_data, scopes=SCOPES)
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
