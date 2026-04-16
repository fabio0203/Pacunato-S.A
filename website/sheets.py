import gspread
import json
import os
from google.oauth2.service_account import Credentials

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


def _fix_json_control_chars(s):
    """
    Render sometimes stores literal newlines inside JSON string values
    (e.g. in private_key). This converts them back to \\n escape sequences
    so json.loads() can parse the JSON correctly.
    """
    result = []
    in_string = False
    escape_next = False
    for char in s:
        if escape_next:
            result.append(char)
            escape_next = False
        elif char == '\\':
            result.append(char)
            escape_next = True
        elif char == '"':
            in_string = not in_string
            result.append(char)
        elif in_string and char == '\n':
            result.append('\\n')
        elif in_string and char == '\r':
            result.append('\\r')
        else:
            result.append(char)
    return ''.join(result)


def get_sheet(tab_name):
    creds_json = os.environ.get('GOOGLE_CREDENTIALS_JSON', '').strip()
    sheet_id = os.environ.get('GOOGLE_SHEETS_ID', '').strip()

    if not creds_json:
        print(f"Google Sheets: GOOGLE_CREDENTIALS_JSON no configurado (longitud raw: {len(os.environ.get('GOOGLE_CREDENTIALS_JSON', ''))})")
        return None
    if not sheet_id:
        print(f"Google Sheets: GOOGLE_SHEETS_ID no configurado (longitud raw: {len(os.environ.get('GOOGLE_SHEETS_ID', ''))})")
        return None
    print(f"Google Sheets: creds_json longitud={len(creds_json)}, primeros 20 chars: {creds_json[:20]}")

    try:
        creds_data = json.loads(creds_json)
    except json.JSONDecodeError:
        # Render stored literal newlines inside string values — fix and retry
        try:
            creds_data = json.loads(_fix_json_control_chars(creds_json))
            print("Google Sheets: JSON corregido (newlines literales en private_key)")
        except json.JSONDecodeError as e:
            print(f"Google Sheets: GOOGLE_CREDENTIALS_JSON no es JSON valido: {e}")
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
            print(f"Google Sheets OK: fila en '{tab_name}'")
    except Exception as e:
        print(f"Google Sheets error ({tab_name}): {str(e)}")
