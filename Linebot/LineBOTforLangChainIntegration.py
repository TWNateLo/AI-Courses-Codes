import openai
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from flask import Flask, request

from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage
import json

app = Flask(__name__)

@app.route("/", methods=['POST'])
def linebot():
    body = request.get_data(as_text=True)
    json_data = json.loads(body)
    print(json_data)
    #try:
    line_bot_api = LineBotApi('channel access token')
    handler = WebhookHandler('channel secret')
    signature = request.headers['X-Line-Signature']
    handler.handle(body, signature)
    tk = json_data['events'][0]['replyToken']
    msg = json_data['events'][0]['message']['text']
    print(msg)
    # fetch the first 5 characters and normalize them to lower case
    ai_msg = msg[:6].lower()
    reply_msg = ''
    # if the first 5 characters are hi ai:
    if ai_msg == 'hi ai:':
        print('query detected')
        chat = ChatOpenAI(model="gpt-3.5-turbo", api_key="openai api key")
        messages = [
            SystemMessage(content="You're a helpful AI assistant connected to LineBOT called 'Law Genius'"),
            HumanMessage(content= str(msg[6:])),
        ]
        reply_msg = chat.invoke(messages).content
    else:
        reply_msg = msg
    text_message = TextSendMessage(text=reply_msg)
    line_bot_api.reply_message(tk,text_message)

if __name__ == "__main__":
    app.run()