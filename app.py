import sys
from io import BytesIO

import telegram
from flask import Flask, request, send_file

from fsm import SportDataMachine


API_TOKEN = '394928478:AAEA7EZ_F7Olghg6Wbdc-LuMsv4VCjXXi18'
WEBHOOK_URL = 'https://e77a58d1.ngrok.io/hook'


app = Flask(__name__)
bot = telegram.Bot(token=API_TOKEN)

machine = SportDataMachine(
    states=[
        'where',
        'US',
        'NYY',
        'TEX',
        'JP',
        'FIGHTER',
        'HAWK',
        'TW',
        'BROTHER',
        'MONKEY'
    ],
    transitions=[
        {
            'trigger': 'advance',
            'source': 'where',
            'dest': 'where',
            'conditions': 'where_to_where'
        },
        {
            'trigger': 'advance',
            'source': 'where',
            'dest': 'US',
            'conditions': 'is_going_to_US'
        },
        {
            'trigger': 'advance',
            'source': 'where',
            'dest': 'JP',
            'conditions': 'is_going_to_JP'
        },
        {
            'trigger': 'advance',
            'source': 'where',
            'dest': 'TW',
            'conditions': 'is_going_to_TW'
        },
        {
            'trigger': 'advance',
            'source': 'US',
            'dest': 'US',
            'conditions': 'US_to_US'
        },
        {
            'trigger': 'advance',
            'source': 'US',
            'dest': 'NYY',
            'conditions': 'is_going_to_NYY'
        },
        {
            'trigger': 'advance',
            'source': 'US',
            'dest': 'TEX',
            'conditions': 'is_going_to_TEX'
        },
        {
            'trigger': 'go_back_US',
            'source': [
                'NYY',
                'TEX'
            ],
            'dest': 'US'
        },
        {
            'trigger': 'advance',
            'source': 'JP',
            'dest': 'JP',
            'conditions': 'JP_to_JP'
        },
        {
            'trigger': 'advance',
            'source': 'JP',
            'dest': 'FIGHTER',
            'conditions': 'is_going_to_FIGHTER'
        },
        {
            'trigger': 'advance',
            'source': 'JP',
            'dest': 'HAWK',
            'conditions': 'is_going_to_HAWK'
        },
        {
            'trigger': 'go_back_JP',
            'source': [
                'FIGHTER',
                'HAWK'
            ],
            'dest': 'JP'
        },
        {
            'trigger': 'advance',
            'source': 'TW',
            'dest': 'TW',
            'conditions': 'TW_to_TW'
        },
        {
            'trigger': 'advance',
            'source': 'TW',
            'dest': 'BROTHER',
            'conditions': 'is_going_to_BROTHER'
        },
        {
            'trigger': 'advance',
            'source': 'TW',
            'dest': 'MONKEY',
            'conditions': 'is_going_to_MONKEY'
        },
        {
            'trigger': 'go_back_TW',
            'source': [
                'BROTHER',
                'MONKEY'
            ],
            'dest': 'TW'
        },
        {
            'trigger': 'advance',
            'source': [
                'US',
                'JP',
                'TW'
            ],
            'dest': 'where',
            'conditions': 'is_going_to_where'
        }
    ],
    initial='where',
    auto_transitions=False,
    show_conditions=True,
)


def _set_webhook():
    status = bot.set_webhook(WEBHOOK_URL)
    if not status:
        print('Webhook setup failed')
        sys.exit(1)
    else:
        print('Your webhook URL has been set to "{}"'.format(WEBHOOK_URL))


@app.route('/hook', methods=['POST'])
def webhook_handler():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    machine.advance(update)
    return 'ok'


if __name__=="__main__":
    _set_webhook()
    app.run()

