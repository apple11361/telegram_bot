import sys
from io import BytesIO

import telegram
from flask import Flask, request, send_file

from fsm import SportDataMachine


API_TOKEN = '394928478:AAEA7EZ_F7Olghg6Wbdc-LuMsv4VCjXXi18'
WEBHOOK_URL = 'https://56790d34.ngrok.io/hook'


app = Flask(__name__)
bot = telegram.Bot(token=API_TOKEN)

machine = SportDataMachine(
    states=[
        'where',
        'US',
        'US_query',
        'JP',
        'JP_query',
        'TW',
        'TW_query'
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
            'dest': 'US_query',
            'conditions': 'is_going_to_US_query'
        },
        {
            'trigger': 'go_back_US',
            'source': 'US_query',
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
            'dest': 'JP_query',
            'conditions': 'is_going_to_JP_query'
        },
        {
            'trigger': 'go_back_JP',
            'source': 'JP_query',
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
            'dest': 'TW_query',
            'conditions': 'is_going_to_TW_query'
        },
        {
            'trigger': 'go_back_TW',
            'source': 'TW_query',
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

@app.route('/show-fsm', methods=['GET'])
def show_fsm():
    byte_io = BytesIO()
    machine.graph.draw(byte_io, prog='dot', format='png')
    byte_io.seek(0)
    return send_file(byte_io, attachment_filename='fsm.png', mimetype='image/png')

if __name__=="__main__":
    _set_webhook()
    app.run()

