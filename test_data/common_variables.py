#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module stores the test data.
"""

from pathlib import Path


_CURRENT_DIR = str(Path(__file__).parent.absolute())

GMAIL_LOGIN_URL = "https://mail.google.com"
IMAP_HOST = "imap.gmail.com"
IMAP_PORT = 993

GITHUB_ORG = "SeleniumHQ"
DEFAULT_APP_USER_TO_SEND_MESSAGE = "demo@vsee.com"
DEFAULT_APP_MESSAGE = "Hello App!"
APP_DOWNLOAD_URL = "https://tinyurl.com/ydeumnh9"


class SenderEmail:
    username = "sender.interview@gmail.com"
    password = "Interview#12345678x@X"


class __Receiver:
    __credential_file = open(f"{_CURRENT_DIR}/receiver_credential").readlines()
    credentials = {
        credential.strip("\n").split("=")[0]:
            credential.strip("\n").split("=")[-1]
        for credential in __credential_file
    }

    @property
    def username(self):
        return self.credentials.get("username")

    @property
    def password(self):
        return self.credentials.get("password")


Receiver = __Receiver()


class MailContent:
    subject = "[Interview] Assignment - {}"
    content = "Hello, this is the email content. {}"


if __name__ == "__main__":
    print(Receiver.username)
    print(Receiver.password)
