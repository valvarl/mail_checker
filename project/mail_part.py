# ! /usr/bin/env python
# -*- coding: utf-8 -*-

import imaplib
import random
import socket
import time

import easyimap

from project.access_data import mail_login, mail_password, sleep_timeout
from project.vk_part import send_message

replies = ['Птичка принесла на хвосте сигареты - нет! Новое сообщение!',
           'Кое-кто хочет сыграть с нами в игру. А вот и правила, которые я нашел на почте.',
           'Поступила новая непроверенная информация.',
           'Подержите мое пиво, у меня сногсшибательная новость!',
           'Я так ждал этого сообщения...',
           'Никогда не было и вот опять.']


def get_unseen_mails(imapper):
    mails = []
    for mail in imapper.unseen(limit=5):
        from_addr = mail.from_addr[:mail.from_addr.index('<')] + ' ' + mail.from_addr[mail.from_addr.index('<'):]
        title = ' на тему «%s».' % mail.title if mail.title else ''
        mails.append((''.join([random.choice(replies), '\n\n@all, пишет %s%s\n\n' % (from_addr, title)]),
                      mail.body, mail.attachments))
    print(mails)
    send_message(mails)


def mail_receiver():
    while True:
        print('auth')
        imapper = easyimap.connect('imap.mail.ru', mail_login, mail_password)
        print('ready')
        try:
            get_unseen_mails(imapper)
        except imaplib.IMAP4.abort:
            # print('timeout')
            continue
        except socket.gaierror:
            # print('socket_error')
            time.sleep(sleep_timeout)
            continue
        imapper.quit()
        print('sleep')
        time.sleep(sleep_timeout)  # 30
