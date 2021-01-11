# ! /usr/bin/env python
# -*- coding: utf-8 -*-

import random


def logs(s):
    with open('logs.txt', 'a+', encoding='utf8') as df:
        df.write(s + '\n')


def send(bot_api, chat_id, message='', attachment=[]):
    bot_api.messages.send(
        random_id=random.getrandbits(32),
        chat_id=chat_id,
        message=message,
        attachment=attachment
    )