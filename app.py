from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import requests, json


import errno
import os
import sys, random
import tempfile

from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, VideoMessage, DatetimePickerAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, SpacerComponent, IconComponent, ButtonComponent,
    SeparatorComponent,
)

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('BJZ1tzDFXT7bvqpdP2ACTYaFKykHzVw5ZuWgrLYMkEkC+tKdm7EG0iTaWMeGlYjH0lSmFpamGvngpf03db9f3rsyRwQIDqBIKXH8NlJsmceYVhKLsLCkdJu5w8XRORr2hiRilc3tP9NjvZr6pj88DAdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('9579953429d30455b3e5854c7f415a71')
#===========[ NOTE SAVER ]=======================
notes = {}

# Post Request
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(JoinEvent)
def handle_join(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='Joined this ' + event.source.type + '))

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text #simplify for receove message
    sender = event.source.user_id #get user_id
    gid = event.source.sender_id #get group_id
    roomid = event.source.room_id #get room id
#=====[ LEAVE GROUP OR ROOM ]==========[ ARSYBAI ]======================
    if text.lower() == 'bye':
        if isinstance(event.source, SourceGroup):
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text='Halo'))
            line_bot_api.leave_group(gid)
        elif isinstance(event.source, SourceRoom):
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text='Leaving group'))
            line_bot_api.leave_room(roomid)
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="Bot can't leave from 1:1 chat"))

#=====[ TEMPLATE MESSAGE ]=============[ ARSYBAI ]======================
    elif text.lower() == '/template':
        buttons_template = TemplateSendMessage(
            alt_text='template',
            template=ButtonsTemplate(
                title='[ TEMPLATE MSG ]',
                text= 'Tap the Button',
                actions=[
                    MessageTemplateAction(
                        label='Culum 1',
                        text='/arsybai'
                    ),
                    MessageTemplateAction(
                        label='CULUM 2',
                        text='/arsybai'
                    ),
                    MessageTemplateAction(
                        label='CULUM 3',
                        text='/arsybai'
                    )
                ]
            )
        )

        line_bot_api.reply_message(event.reply_token, buttons_template)
#=====[ CAROUSEL MESSAGE ]==========[ ARSYBAI ]======================
    elif text.lower() == '/carousel':
        message = TemplateSendMessage(
            alt_text='OTHER MENU',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        title='CAROUSEL 1',
                        text='This Carousel URI action',
                        actions=[
                            URITemplateAction(
                                label='>carousel 1<',
                                uri='https://line.me/ti/p/~arsy22bai'
                            )
                        ]
                    ),
                    CarouselColumn(
                        title='ABAI-API',
                        text='API documentation',
                        actions=[
                            URITemplateAction(
                                label='>Visit<',
                                uri='https://arsybaiapi.herokuapp.com'
                            )
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    elif text.lower() == 'image':
        message = ImageSendMessage(
        original_content_url='https://example.com/original.jpg',
        preview_image_url='https://example.com/preview.jpg'
        )
        line_bot_api.reply_message(event.reply_token, message)
#=====[ FLEX MESSAGE ]==========[ ARSYBAI ]======================
    elif text.lower() == 'flex':
        bubble = BubbleContainer(
            direction='ltr',
            hero=ImageComponent(
                url='https://example.com/cafe.jpg',
                size='full',
                aspect_ratio='20:13',
                aspect_mode='cover',
                action=URIAction(uri='http://example.com', label='label')
            ),
            body=BoxComponent(
                layout='vertical',
                contents=[
                    # title
                    TextComponent(text='Brown Cafe', weight='bold', size='xl'),
                    # review
                    BoxComponent(
                        layout='baseline',
                        margin='md',
                        contents=[
                            IconComponent(size='sm', url='https://example.com/gold_star.png'),
                            IconComponent(size='sm', url='https://example.com/grey_star.png'),
                            IconComponent(size='sm', url='https://example.com/gold_star.png'),
                            IconComponent(size='sm', url='https://example.com/gold_star.png'),
                            IconComponent(size='sm', url='https://example.com/grey_star.png'),
                            TextComponent(text='4.0', size='sm', color='#999999', margin='md',
                                          flex=0)
                        ]
                    ),
                    # info
                    BoxComponent(
                        layout='vertical',
                        margin='lg',
                        spacing='sm',
                        contents=[
                            BoxComponent(
                                layout='baseline',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='Place',
                                        color='#aaaaaa',
                                        size='sm',
                                        flex=1
                                    ),
                                    TextComponent(
                                        text='Shinjuku, Tokyo',
                                        wrap=True,
                                        color='#666666',
                                        size='sm',
                                        flex=5
                                    )
                                ],
                            ),
                            BoxComponent(
                                layout='baseline',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='Time',
                                        color='#aaaaaa',
                                        size='sm',
                                        flex=1
                                    ),
                                    TextComponent(
                                        text="10:00 - 23:00",
                                        wrap=True,
                                        color='#666666',
                                        size='sm',
                                        flex=5,
                                    ),
                                ],
                            ),
                        ],
                    )
                ],
            ),
            footer=BoxComponent(
                layout='vertical',
                spacing='sm',
                contents=[
                    # separator
                    SeparatorComponent(),
                    # websiteAction
                    ButtonComponent(
                        style='Primary',
                        height='sm',
                        action=URIAction(label='WEBSITE', uri="https://example.com")
                    )
                ]
            ),
        )
        message = FlexSendMessage(alt_text="hello", contents=bubble)
        line_bot_api.reply_message(
            event.reply_token,
            message
        )
#=======================================================================================================================
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
