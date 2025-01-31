from flask import Blueprint
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from model import GetDataGoogleModel

SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/spreadsheets.readonly']

READ_SPREADSHEET_ID = "1Q3w-UW3jlXMKMgNaFjdrLVV2PPAuWf-DJ9dZjxuX81A"
READ_RANGE_NAME = "ชีท1!A1:F7"

class PostExchange():
    def get_post_exchange_by_user_id(self, user_id):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    
        service = build("sheets", "v4", credentials=creds)
        sheet = service.spreadsheets()
        result = (
            sheet.values()
            .get(spreadsheetId=READ_SPREADSHEET_ID, range=READ_RANGE_NAME)
            .execute()
        )
        values = result.get("values", [])

        date_list = values[0]
        data_px = []
        for index, value in enumerate(values, start=0):
            if index == 0: 
                continue
            id = value[0]
            total_amount = value[5]
        
            for index, item in enumerate(value, start=0):
                if index == 0 or index == len(value) - 1 or item == '':
                    continue
                
                amount = item 
                date = date_list[index]
                data_px.append(GetDataGoogleModel().to_dict(id, date, amount, total_amount))
        
        gg = list(filter(lambda x: x.id == user_id, data_px))
        
        return f'รายงานยอด px\nประจำวันที่ {gg[0].date}\nยอด {gg[0].amount} บาท'

    def create_user_post_exchange(self):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    
        spreadsheet_id = "1Q3w-UW3jlXMKMgNaFjdrLVV2PPAuWf-DJ9dZjxuX81A"
        range_name = "users!A4:C6"
        value_input_option = "USER_ENTERED"
        
        service = build("sheets", "v4", credentials=creds)
        sheet = service.spreadsheets()
        values = [
            ["Name", "Age", "City"],
            ["John", 30, "New York"],
            ["Jane", 25, "Los Angeles"],
        ]

        body = {"values": values}
        result = (
            service.spreadsheets()
            .values()
            .update(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption=value_input_option,
                body=body,
            ).execute()
        )
        return f"create user post exchange"