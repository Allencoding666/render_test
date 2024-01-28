from telegram.ext.filters import MessageFilter


class FilterMsgTest(MessageFilter):
    def filter(self, message):
        return "哈哈" in message.text
