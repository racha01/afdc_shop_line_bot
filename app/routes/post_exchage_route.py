from flask import Blueprint
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from model import GetDataGoogleModel
# from module.post_exchange_module import PostExchange

SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/spreadsheets.readonly']


SAMPLE_SPREADSHEET_ID = "1Q3w-UW3jlXMKMgNaFjdrLVV2PPAuWf-DJ9dZjxuX81A"
SAMPLE_RANGE_NAME = "ชีท1!A1:F7"

post_exchange_bp = Blueprint('post_exchange_bp', __name__)

@post_exchange_bp.get('/api/post_exchange/<user_id>')
def get_post_exchange(user_id):
    # post_exchange_module = PostExchange
    # gg = post_exchange_module.get_post_exchange_by_user_id(user_id)
    return 'rachanon'

@post_exchange_bp.post('/api/post_exchange')
def create_post_exchange():
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    
    spreadsheet_id = "1Q3w-UW3jlXMKMgNaFjdrLVV2PPAuWf-DJ9dZjxuX81A"
    range_name = "users!A1:C3"
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
    # result = (
    #     sheet.values()
    #     .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME)
    #     .execute()
    # )
    # values = result.get("values", [])

    # date_list = values[0]
    # data_px = []
    # for index, value in enumerate(values, start=0):
    #     if index == 0: 
    #         continue
    #     id = value[0]
    #     total_amount = value[5]
    
    #     for index, item in enumerate(value, start=0):
    #         if index == 0 or index == len(value) - 1 or item == '':
    #             continue
            
    #         amount = item 
    #         date = date_list[index]
    #         data_px.append(GetDataGoogleModel().to_dict(id, date, amount, total_amount))
    
    # gg = list(filter(lambda x: x.id == user_id and x.date == '5 ธ.ค. 67', data_px))
    
    return f'รายงานยอด px\nประจำวันที่'
    
    