from flask import request, abort, Blueprint, url_for, session, render_template, jsonify, redirect, json
from datetime import datetime, timedelta
import flask
from app.module.post_exchange_module import PostExchange
import requests
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

LINE_CLIENT_ID = "2006696301"
LINE_CLIENT_SECRET = "3e56786ceb2cbfb2c1f7bb581d314802"
LINE_REDIRECT_URI = "https://4b84-58-136-253-186.ngrok-free.app/callback-login"
LINE_ACCESS_TOKEN = "WaYSIv7uIgRWmwW0GEOJRbzhXHEVd3hG4MoVP9bsYImKRY/fJwj9Huwf41c1eTCnGVvkZcKSz7UD1FdXAuc9vniv6ZDFcvnO14Cb3dImIO6OHCFMHE/D67E43kyzExutIIvkyU/KlbyVcZrsFeKV/gdB04t89/1O/w1cDnyilFU="
LINE_AUTH_URL = "https://access.line.me/oauth2/v2.1/authorize"
LINE_TOKEN_URL = "https://api.line.me/oauth2/v2.1/token"
LINE_PROFILE_URL = "https://api.line.me/v2/profile"

@line_route_bp.route("/login")
def login():
    login_url = (
        f"{LINE_AUTH_URL}?response_type=code"
        f"&client_id={LINE_CLIENT_ID}"
        f"&redirect_uri={LINE_REDIRECT_URI}"
        f"&state=random_state&scope=profile%20openid"
    )
    return redirect(login_url)

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

@line_route_bp.route('/callback-login', methods=['GET'])
def callback_permision():
    code = request.args.get("code")
    state = request.args.get("state")

    if not code:
        return "Authorization failed."
    
    token_data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": LINE_REDIRECT_URI,
        "client_id": LINE_CLIENT_ID,
        "client_secret": LINE_CLIENT_SECRET,
    }

    response = requests.post(LINE_TOKEN_URL, data=token_data)
    token_response = response.json()

    if "access_token" not in token_response:
        return "Failed to obtain access token."

    access_token = token_response["access_token"]

    # Retrieve user profile
    headers = {"Authorization": f"Bearer {access_token}"}
    profile_response = requests.get(LINE_PROFILE_URL, headers=headers)
    profile = profile_response.json()

    session["profile"] = profile
    return redirect(url_for("line_route_bp.profile"))

@line_route_bp.route("/profile")
def profile():
    if "profile" not in session:
        return redirect(url_for("home"))

    profile = session["profile"]
    message = "login สำเร็จ"

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {LINE_ACCESS_TOKEN}'
    }
    payload = {
        "to": profile['userId'],
        "messages": [
            {
                "type": "text",
                "text": message
            }
        ]
    }
    
    url = 'https://api.line.me/v2/bot/message/push'
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    
    return redirect('line://chats')

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
            elif event.message.text == "login":
                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[TextMessage(text='https://4b84-58-136-253-186.ngrok-free.app/login')]
                    )
                )
            else:
                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[TextMessage(text=f'ผมไม่เข้าใจที่คุณพูด')]
                    )
                )