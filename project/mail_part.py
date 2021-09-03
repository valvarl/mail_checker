# ! /usr/bin/env python
# -*- coding: utf-8 -*-

import imaplib
import random
import socket
import time
from datetime import datetime

import easyimap
import base64
import re

from project.access_data import mail_login, mail_password, sleep_timeout
from project.vk_part import send_message


replies = ['Нагнулся в душе за мылом, а сзади слышу...',
           'Слаще этой новости чафира еще не варили.',
           'Леди и джентельмены, в цирке снова представление!',
           'Все клоуны уехали, а сообщение осталось.',
           'Вы присылаете хороших новостей? Красивое...',
           'От сумы и от тюрьмы не зарекайся. Особенно во время сессии.',
           'Всем добра и позитива. Кто куда, а я за пивом.',
           'Кто не курит и не пьет, рано или поздно начнет после такого.',
           'Им не заставить нас учиться по субботам!',
           'Школа несчастья есть самая лучшая школа. Знали?',
           'Качество сна, к сожалению, не зависит от числа подушек.']


signature = r'________________________________\r\n\r\nЭто электронное сообщение и любые документы, приложенные к нему, содержат конфиденциальную информацию и предназначены исключительно для использования работниками НИУ ВШЭ, физическим или юридическим лицом, которому они адресованы. Уведомляем Вас о том, что, если это сообщение не предназначено Вам, использование, копирование, распространение информации, содержащейся в настоящем сообщении, а также осуществление любых действий на основе этой информации, не допускается. Если Вы считаете, что Вы получили это электронное сообщение по ошибке, пожалуйста, свяжитесь с отправителем и незамедлительно удалите электронное сообщение и любые вложения с компьютера. Заранее благодарим.\r\n\r\nThis e-mail and any attachments to it contain confidential information intended only for the use of the HSE University staff, the individual or entity who they are addressed to. We inform you that if you are not an intended recipient of this e-mail, the use, copying, distribution of the information contained in this message, as well as the conduction of any action based on this information is not allowed. If you believe that you have received this email in error, please contact the sender and immediately delete the email and any attachments from your computer. Thank you in advance.'
signature2 = r'----------------------------------------------------------------------\nЭто электронное сообщение и любые документы, приложенные к нему, содержат конфиденциальную информацию и предназначены исключительно для использования работниками НИУ ВШЭ, физическим или юридическим лицом, которому они адресованы. Уведомляем Вас о том, что, если это сообщение не предназначено Вам, использование, копирование, распространение информации, содержащейся в настоящем сообщении, а также осуществление любых действий на основе этой информации, не допускается. Если Вы считаете, что Вы получили это электронное сообщение по ошибке, пожалуйста, свяжитесь с отправителем и незамедлительно удалите электронное сообщение и любые вложения с компьютера. Заранее благодарим.\nThis e-mail and any attachments to it contain confidential information intended only for the use of the HSE University staff, the individual or entity who they are addressed to. We inform you that if you are not an intended recipient of this e-mail, the use, copying, distribution of the information contained in this message, as well as the conduction of any action based on this information is not allowed. If you believe that you have received this email in error, please contact the sender and immediately delete the email and any attachments from your computer. Thank you in advance. \xa0\n----------------------------------------------------------------------'


def decode_filename(file_name: str):
    file_name_copy = file_name
    try:
        encoding = re.match(r'=\?\S*\?B\?', file_name).group(0)[2:-3]
        file_name = re.sub(r'=\?\S*\?B\?', '', file_name)
        d = base64.b64decode(file_name)
        return d.decode(encoding)
    except Exception:
        return file_name_copy


def get_unseen_mails(imapper):
    mails = []
    for mail in imapper.unseen(limit=5):
        from_addr = mail.from_addr[:mail.from_addr.index('<')] + ' ' + mail.from_addr[mail.from_addr.index('<'):]
        title = ' на тему «%s».' % mail.title if mail.title else ''
        attachments = []
        regex = r'((_(_|\r|\n)*?)?(От|From).*?(Тема|Subject).*?(\r|\n)*?\n)'
        text0 = re.sub(regex, '\n》═══════~◈~═══════《\n', mail.body, flags=re.S)
        text = re.sub(signature2, '', re.sub(signature, '', text0)).strip() + '\n\n══════ஜ▲ஜ══════'
        # print([text])
        for attachment in mail.attachments:
            attachments.append((decode_filename(attachment[0]), attachment[1], attachment[2]))
        mails.append((''.join(
            [
                random.choice(replies),
                '\n\n@%s, пишет %s%s\n\n' % (
                    'all' if (datetime.utcnow().hour + 3) % 24 >= 6 else 'online',
                    from_addr,
                    title)
            ]
        ), text,
                      attachments))
    # print(mails)
    send_message(mails)


def mail_receiver():
    while True:
        # print('auth')
        imapper = easyimap.connect('imap.mail.ru', mail_login, mail_password)
        # print('ready')
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
        # print('sleep')
        time.sleep(sleep_timeout)  # 30