# -*- coding: utf-8 -*-

import gevent
from gevent.threadpool import ThreadPool
import pickle
import json
import urlparse
import os
import psycopg2
from util.utils import *
from wordquiz import *
from bot.bot import *
from summary import *
from variable import *
from hangang import *
from help import *
from mafiagame import *
from jeonghan import *
from music import *
from share import *
from dday import *
from keywords import *
from coin import *


class Botdol(Bot):
    def __init__(self):
        super(Botdol, self).__init__()
        self._version = 1.0
        self._name = "유미"

        urlparse.uses_netloc.append("postgres")

        self._pgconn = psycopg2.connect(
            database="aaa",
            user="postgres",
            password="1234",
            host="127.0.0.1",
            port="5432"
        )
        #264588139300152 동네남자방
        #219909832146279 개인톡
        #234264607883386 테스트방
        #189386551758081 마약
        #254974539480472 이진근
        with self._pgconn.cursor() as cursor:
            self._init_db(cursor)
            self._variable = Variable.load(cursor)
            self._wordquiz = Wordquiz.load(cursor)
            self._dday = Dday.load(cursor)
            self._keyword = Keyword.load(cursor)

        self._mafiagame = MafiaGame()
        #self._coinanalyzer = CoinAnalyzer()
        #self._pool = ThreadPool(1)
        #self._pool.spawn(self._coinanalyzer.run)

        # 빨래통
        
        self.add_command(189386551758081, HangangCommand("자살"))
        self.add_command(189386551758081, MafiaCommand("ㅁㅍㅇ", self._mafiagame))
        self.add_command(189386551758081, MusicSearchCommand("ㅇㄱ"))
        self.add_command(189386551758081, MusicDownloadCommand("ㅇㄷ"))
        self.add_command(189386551758081, HelpCommand("?", self._commands.get(189386551758081, {})))

        # 개인톡


        # 그 외
        self.add_command(0, MafiaSingleChatCommand("ㅁㅍㅇ", self._mafiagame))
        # help must be added at the last
        self.add_command(0, HelpCommand("?", self._commands.get(0, {})))
        self._bot_timer = gevent.spawn(self._do_timer)

    def _init_db(self, cur):
        cur.execute("""CREATE TABLE IF NOT EXISTS pickled
            (id SERIAL PRIMARY KEY NOT NULL,
             type VARCHAR(12) NOT NULL,
             data TEXT);""")

        self._pgconn.commit()

    def _do_timer(self):
        while True:
            gevent.sleep(60)
            self.save()

    def shutdown(self):
        self._bot_timer.kill()
        self.save()
        self._pgconn.close()

    def save(self):
        with self._pgconn.cursor() as cursor:
            Variable.save(cursor, self._variable.var())
            Wordquiz.save(cursor, self._wordquiz)
            Dday.save(cursor, self._dday.dday())
            Keyword.save(cursor, self._keyword.keyword())
            self._pgconn.commit()

    def on_connect(self, sess):
        sess.send_text("{0} v{1} 구동".format(self._name, self._version), 219909832146279)
        sess.send_chat_on_room(219909832146279)

    def on_shutdown(self, sess):
        sess.send_text("{0} v{1} 종료".format(self._name, self._version), 219909832146279)

    def on_msg(self, sess, msg):
        self.process_command(sess, msg)

        author_nick = msg.author()
        msg = msg.chat_log()
        message = msg.message()
        chat_id = msg.chat_id()
        author = msg.author_id()
        print chat_id
        # none commands
        if chat_id == 264588139300152:
            pass

        else:
            pass
