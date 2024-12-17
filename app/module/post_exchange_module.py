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
        
        gg = list(filter(lambda x: x.id == user_id and x.date == '5 ธ.ค. 67', data_px))
        
        return f'รายงานยอด px\nประจำวันที่ {gg[0].date}\nยอด {gg[0].amount} บาท'

    def create_user_post_exchange(self):
        return f"create user post exchange"