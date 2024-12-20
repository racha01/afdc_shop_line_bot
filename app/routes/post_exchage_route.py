from flask import Blueprint
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from model import GetDataGoogleModel
from ..module.post_exchange_module import PostExchange
# from module.post_exchange_module import PostExchange

SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/spreadsheets.readonly']


SAMPLE_SPREADSHEET_ID = "1Q3w-UW3jlXMKMgNaFjdrLVV2PPAuWf-DJ9dZjxuX81A"
SAMPLE_RANGE_NAME = "ชีท1!A1:F7"

post_exchange_bp = Blueprint('post_exchange_bp', __name__)
post_exchange = PostExchange()
@post_exchange_bp.get('/api/post_exchange/<user_id>')
def get_post_exchange(user_id):
    # post_exchange_module = PostExchange
    # gg = post_exchange_module.get_post_exchange_by_user_id(user_id)
    return 'rachanon'

@post_exchange_bp.post('/api/post_exchange')
def create_post_exchange():
    post_exchange.create_user_post_exchange()
    
    return f'รายงานยอด px\nประจำวันที่'
    
    