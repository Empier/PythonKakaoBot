# -*- coding: utf-8 -*-

from locoresponse import LocoResponse


class LocoCreateResponse(LocoResponse):
    def chat_id(self):
        print self._data["errMsg"].encode('utf-8')
        return self._data["chatId"]
