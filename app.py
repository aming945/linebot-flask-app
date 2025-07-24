from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, QuickReply, QuickReplyButton, MessageAction
from linebot.models import TemplateSendMessage, ButtonsTemplate, PostbackAction, PostbackEvent,FlexSendMessage

app = Flask(__name__)



line_bot_api = LineBotApi('goBLuHUNvyvNlynFI+Xc/jgM/n8L/60A0X23kx+n5QM6Hp6IpDWyu5w6qP/hs6T6uawY6KX3Ijo915mGgPrDh3X35BUbBL8V7Fu55gJkA5/c86rN1hM6y4WrXlL/lLAQqNe+lK8BcAvQUfCW2WPSswdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('0accce30a3ead3b05e956b69b96fda08')

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers.get('X-Line-Signature')
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_msg = event.message.text

    if user_msg == "健保":
        buttons_template = TemplateSendMessage(
        alt_text='您想詢問哪種健保問題？',
        template=ButtonsTemplate(
            title='您想詢問哪種健保問題？',
            text='請選擇：',
            actions=[
                MessageAction(label='xin thẻ bảo hiểm', text='xin thẻ bảo hiểm y tế'),
                MessageAction(label='健保費用', text='健保費用'),
                MessageAction(label='健保卡忘記帶', text='健保卡忘記帶'),
                MessageAction(label='健保退費', text='健保退費'),
            ]
        )
    )
        line_bot_api.reply_message(event.reply_token, buttons_template)

    elif user_msg == "課程":
        flex_message = FlexSendMessage(
            alt_text='您想詢問哪種課程問題？',
            contents={
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "text", "text": "請選擇課程相關問題", "weight": "bold", "size": "md", "margin": "md"},
                        {"type": "button", "style": "white", "action": {"type": "message", "label": "課程報名", "text": "課程報名"}},
                        {"type": "button", "style": "primary", "action": {"type": "message", "label": "課程費用", "text": "課程費用"}},
                        {"type": "button", "style": "primary", "action": {"type": "message", "label": "課程時程", "text": "課程時程"}},
                        {"type": "button", "style": "primary", "action": {"type": "message", "label": "課程證明", "text": "課程證明"}}
                    ]
                }
            }
        )
        line_bot_api.reply_message(event.reply_token, flex_message)

# 處理使用者點擊 postback 按鈕
@handler.add(PostbackEvent)
def handle_postback(event):
    data = event.postback.data

    if data == '加入健保':
        reply_text = "加入健保"
    elif data == '健保費用':
        reply_text = "健保費用"
    elif data == '健保卡忘記帶':
        reply_text = "健保卡忘記帶"
    elif data == '健保退費':
        reply_text = "健保退費"
    else:
        reply_text = "您選擇了：" + data

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )


if __name__ == "__main__":
    app.run(debug=True)