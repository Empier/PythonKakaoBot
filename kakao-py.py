#!/usr/bin/python
# -*- coding: utf-8 -*-

import getpass
import gevent
import sys
import login
import traceback
import signal
from botdol import *



def main():
    email = "-"
    uuid = "8d528440-07E0-0000-0000-000000000000"

    password = "-"

    sess = login.try_login(email, password, uuid)
    if sess is None:
        return

    gevent.signal(signal.SIGTERM, sess.set_run_event)
    gevent.signal(signal.SIGQUIT, sess.set_run_event)
    gevent.signal(signal.SIGKILL, sess.set_run_event)

    try:
        sess.register_bot(Botdol())
        sess.run()
        sess.join()
    except:
        import traceback
        print "---- main loop ----"
        print traceback.format_exc()
        print "-------------------"
    finally:
        sess.close()

if __name__ == "__main__":
    #if len(sys.argv) < 3:
    #    usage(sys.argv)
    #    sys.exit(1)

    main()
