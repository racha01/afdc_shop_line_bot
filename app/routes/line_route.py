from flask import request, abort, Blueprint, url_for, session
from datetime import datetime, timedelta
import flask
from app.module.post_exchange_module import PostExchange
from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)

line_route_bp = Blueprint('line_route_bp', __name__)
app = flask.Flask(__name__)
app.config.from_object('config.LineConfig')

handler = WebhookHandler(app.config['WEBHOOK_HEADER'])
configuration = Configuration(access_token=app.config['ACCESS_TOKEN'])

@line_route_bp.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    current_time = datetime.utcnow()

    message_time = datetime.utcfromtimestamp(event.timestamp / 1000.0)
    
    if current_time - message_time < timedelta(seconds=10):
     
      with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            if(event.message.text == 'เช็คยอด'):
                post_exchange_module = PostExchange()
                message = post_exchange_module.get_post_exchange_by_user_id(event.source.user_id)
                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[TextMessage(text=message)]
                    )
                )
            else:
                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[TextMessage(text=f'ผมไม่เข้าใจที่คุณพูด')]
                    )
                )