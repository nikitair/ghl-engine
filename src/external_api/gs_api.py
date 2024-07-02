import os
import json
from dotenv import load_dotenv
from config.logging_config import logger
from dataclasses import dataclass
import gspread
from google.oauth2.service_account import Credentials
from config import ROOT_DIR

load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
CREDS = Credentials.from_service_account_file(f"{ROOT_DIR}/.gs_credentials.json", scopes=SCOPES)
GSHEET_ID = os.getenv("GSHEET_ID", "")
WORKSHEET_NAME = os.getenv("WORKSHEET_NAME", "")


@dataclass
class GoogleSheetsAPI:
    sheet_id: str = GSHEET_ID
    worksheet_name: str = WORKSHEET_NAME
    client = gspread.authorize(CREDS)
    sheet = client.open_by_key(sheet_id)
    
    def read_all_data(self) -> list[dict]:
        logger.info(f"GS API: Read all data from (ws: {self.worksheet_name}; s_id: {self.sheet_id}")
        worksheet = self.sheet.worksheet(self.worksheet_name)
        data = worksheet.get_all_records()
        logger.debug(f"GS API: Found data - ({data})")
        return data
