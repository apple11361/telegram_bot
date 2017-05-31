from transitions.extensions import GraphMachine



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
        return (text!='0' and text!='1' and text!='2')

    def is_going_to_NYY(self, update):
        text = update.message.text
        return text=='1'
    
    def is_going_to_TEX(self, update):
        text = update.message.text
        return text=='2'

    def is_going_to_JP(self, update):
        text = update.message.text
        return text=='JP'

    def JP_to_JP(self, update):
        text = update.message.text
        return (text!='0' and text!='1' and text!='2')

    def is_going_to_FIGHTER(self, update):
        text = update.message.text
        return text=='1'

    def is_going_to_HAWK(self, update):
        text = update.message.text
        return text=='2'

    def is_going_to_TW(self, update):
        text = update.message.text
        return text=='TW'

    def TW_to_TW(self, update):
        text = update.message.text
        return (text!='0' and text!='1' and text!='2')

    def is_going_to_BROTHER(self, update):
        text = update.message.text
        return text=='1'

    def is_going_to_MONKEY(self, update):
        text = update.message.text
        return text=='2'

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
        update.message.reply_text(
            '歡迎來到MLB\n'
            '你可以輸入數字代號\n'
            '查詢各隊伍統計數據\n'
            '0.重新選擇賽區\n'
            '1.洋基\n'
            '2.遊騎兵\n'
        )

    def on_enter_NYY(self, update):
        update.message.reply_text(
            '紐約洋基\n'
            '打擊率： .263\n'
            '上壘率： .343\n'
            '長打率： .445\n'
        )
        self.go_back_US(update)

    def on_enter_TEX(self, update):
        update.message.reply_text(
            '德州遊騎兵\n'
            '打擊率： .237\n'
            '上壘率： .311\n'
            '長打率： .411\n'
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

    def on_enter_FIGHTER(self, update):
        update.message.reply_text(
            '日本火腿鬥士\n'
            '打擊率： .263\n'
            '上壘率： .343\n'
            '長打率： .445\n'
        )
        self.go_back_JP(update)

    def on_enter_HAWK(self, update):
        update.message.reply_text(
            '軟體銀行鷹\n'
            '打擊率： .237\n'
            '上壘率： .311\n'
            '長打率： .411\n'
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

    def on_enter_BROTHER(self, update):
        update.message.reply_text(
            '中信兄弟\n'
            '打擊率： .298\n'
            '上壘率： .369\n'
            '長打率： .493\n'
        )
        self.go_back_TW(update)

    def on_enter_MONKEY(self, update):
        update.message.reply_text(
            'Lamigo桃猿\n'
            '打擊率： .294\n'
            '上壘率： .357\n'
            '長打率： .463\n'
        )
        self.go_back_TW(update)




