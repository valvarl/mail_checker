# ! /usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

from project.access_data import group_token, group_id, chat_id
from project.utils import send

extension = {'application/vnd.ms-excel': 'xls',
             'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': 'xlsx',
             'application/msword': 'doc',
             'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'docx',
             'application/vnd.ms-powerpoint': 'ppt',
             'application/vnd.openxmlformats-officedocument.presentationml.presentation': 'pptx',
             'application/pdf': 'pdf',
             'image/jpeg': 'jpg',
             'image/png': 'png'}

# def main():
#     replies = ['1', '2', '3']
#     bot_session = vk_api.VkApi(token=group_token)
#     bot_api = bot_session.get_api()
#     while True:
#         longpoll = VkBotLongPoll(bot_session, group_id)
#         try:
#             print('wait')
#             for event in longpoll.listen():
#                 print('got event')
#                 if event.type == VkBotEventType.MESSAGE_NEW:
#                     print('message')
#                     if event.from_chat:
#                         bot_api.messages.send(
#                             random_id=random.getrandbits(32),
#                             chat_id=event.chat_id,
#                             message=random.choice(replies)
#                         )
#                         print(event.chat_id)
#         except requests.exceptions.ReadTimeout as timeout:
#             continue


def send_message(mails: list):
    bot_session = vk_api.VkApi(token=group_token)
    bot_api = bot_session.get_api()

    for mail in mails:
        attachment, missed = upload_docs(mail[2])
        full_text = mail[0] + mail[1]
        message = full_text + '\n\n--\n' + '\n'.join(missed) if missed else full_text
        try:
            send(bot_api, chat_id, message, attachment)

        except vk_api.exceptions.ApiError:
            message = mail[0] + 'Письмо слишком большое, посмотрие его на почте.\n'
            send(bot_api, chat_id, message)


def upload_docs(docs: list):
    bot_session = vk_api.VkApi(token=group_token)
    bot_api = bot_session.get_api()

    uploaded_docs, missed_docs = [], []
    for doc in docs:
        try:
            upload_url = bot_api.docs.getMessagesUploadServer(peer_id=2000000000 + chat_id)['upload_url']
            print(upload_url)

            request = requests.post(upload_url, files={'file': doc})
            print(request.json())
            if 'error' in request.json().keys() and request.json()['error'] == 'no extension found':
                title = 'attached' + str(len(uploaded_docs) + len(missed_docs)) + '.' + extension[doc[2]]
                request = requests.post(upload_url, files={'file': (title, doc[1], doc[2])}).json()
                request['title'] = title
                print('r', request)

            save_doc = bot_api.docs.save(file=request['file'], title=doc[0])
            print(save_doc)

            doc_attach = 'doc' + str(save_doc['doc']['owner_id']) + '_' + str(save_doc['doc']['id'])
            if len(uploaded_docs) < 10:
                uploaded_docs.append(doc_attach)
            else:
                missed_docs.append(save_doc['doc']['title'] + ': ' + save_doc['doc']['url'])
            print(uploaded_docs)

        except Exception:
            missed_docs.append(doc[0])
            print(missed_docs)
            continue

    return uploaded_docs, missed_docs


# if __name__ == '__main__':
#     main()
