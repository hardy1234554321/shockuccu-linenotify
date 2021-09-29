from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('DjPoMIGhXbf9sG+Lh6oZP5dKphhWf+ZfRjwn30r8lj+C2mxtgPgbFaSiUZJ7+ivJ1HaVXdh5gZlbVX2ZRfN0Ts+1K78gfITsRBgMjgp0115JpAhhSHr8NOM4XsO/JB01o6iAE6RJI3N3MMK7SG6CBwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('879651a425febf4b25c259c701af938a')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.push_message(to, TextSendMessage(text='Hello World!'))
    # line_bot_api.reply_message(
    #     event.reply_token,
    #     TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()