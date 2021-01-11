# ! /usr/bin/env python
# -*- coding: utf-8 -*-

import traceback

from project.mail_part import mail_receiver
from project.utils import logs

if __name__ == '__main__':
    while True:
        try:
            mail_receiver()
        except Exception as e:
            logs('Error:\n' + traceback.format_exc())
