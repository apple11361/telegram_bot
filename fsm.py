from transitions.extensions import GraphMachine

from parse import get_articles
from parse import get_web_page

import time
import numpy

########################parse web for stats##############################
US_stats = numpy.zeros((30, 3), float)
US_name = []
TW_stats = numpy.zeros((4, 3), float)
TW_name = []

page = get_web_page('https://www.msn.com/zh-tw/sports/mlb/team-stats')
if page:
    current_articles = get_articles(page)
    team = 0
    index = 0
    for post in current_articles:
        if index <3:
            US_stats[team][index] = float(post)
        else:
            US_name.append(post)

        index = (index + 1) % 4
        if index==0:
            team = team + 1

#########################################################################

class SportDataMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model = self,
            **machine_configs
        )

    def where_to_where(self, update):
        text = update.message.text
        return (text!='US' and text!='JP' and text!='TW')

    def is_going_to_US(self, update):
        text = update.message.text
        return text=='US'

    def US_to_US(self, update):
        text = update.message.text
        try:
            return 0 > int(text) or int(text) > 30
        except ValueError:
            return 1

    def is_going_to_US_query(self, update):
        text = update.message.text
        return 1 <= int(text) and int(text) <= 30 

    def is_going_to_JP(self, update):
        text = update.message.text
        return text=='JP'

    def JP_to_JP(self, update):
        text = update.message.text
        try:
            return 0 > int(text) or int(text) > 30
        except ValueError:
            return 1

    def is_going_to_JP_query(self, update):
        text = update.message.text
        return 1 <= int(text) and int(text) <= 30

    def is_going_to_TW(self, update):
        text = update.message.text
        return text=='TW'

    def TW_to_TW(self, update):
        text = update.message.text
        try:
            return 0 > int(text) or int(text) > 4
        except ValueError:
            return 1

    def is_going_to_TW_query(self, update):
        text = update.message.text
        return 1 <= int(text) and int(text) <= 4

    def is_going_to_where(self, update):
        text = update.message.text
        return text=='0'

    def on_enter_where(self, update):
        update.message.reply_text(
            '請選擇想查詢的賽區\n'
            '輸入"US"查詢 MLB\n'
            '輸入"JP"查詢 日本職棒\n'
            '輸入"TW"查詢 中華職棒\n'
        )

    def on_enter_US(self, update):
        i = 1;
        text = ( 
            '歡迎來到MLB\n'
            '你可以輸入數字代號\n'
            '查詢各隊伍統計數據\n'
            '0.重新選擇賽區\n'
        )
        for e in US_name:
            text = text+str(i)+'.'+e+'\n'
            i = i + 1
        update.message.reply_text(text)

    def on_enter_US_query(self, update):
        text = update.message.text
        update.message.reply_text(
            US_name[int(text)-1]+'\n'
            '打擊率： '+str(US_stats[int(text)-1][0])+'\n'
            '上壘率： '+str(US_stats[int(text)-1][1])+'\n'
            '長打率： '+str(US_stats[int(text)-1][2])+'\n'
        )
        self.go_back_US(update)

    def on_enter_JP(self, update):
        update.message.reply_text(
            '歡迎來到日本職棒\n'
            '你可以輸入數字代號\n'
            '查詢各隊伍統計數據\n'
            '0.重新選擇賽區\n'
            '1.火腿\n'
            '2.軟銀\n'
        )

    def on_enter_JP_query(self, update):
        update.message.reply_text(
            '日本火腿鬥士\n'
            '打擊率： .263\n'
            '上壘率： .343\n'
            '長打率： .445\n'
        )
        self.go_back_JP(update)

    def on_enter_TW(self, update):
        update.message.reply_text(
            '歡迎來到中華職棒\n'
            '你可以輸入數字代號\n'
            '查詢各隊伍統計數據\n'
            '0.重新選擇賽區\n'
            '1.兄弟\n'
            '2.桃猿\n'
        )

    def on_enter_TW_query(self, update):
        update.message.reply_text(
            '中信兄弟\n'
            '打擊率： .298\n'
            '上壘率： .369\n'
            '長打率： .493\n'
        )
        self.go_back_TW(update)




