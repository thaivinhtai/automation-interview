#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module contains IMAP functions for convenience.
"""

from typing import Union

from imaplib import IMAP4, IMAP4_SSL
from email import message_from_bytes
from email.message import Message


def get_mail_client(imap_mail_server: str, imap_port: int,
                    email_address: str, email_password: str) -> IMAP4:
    """Get mail client.

    Login to the email.

    Parameters
    ----------
    imap_mail_server : str
        The IMAP server
    imap_port : int
        The Port to connect to
    email_address : str
        The email address
    email_password : str
        The email password

    Returns
    -------
    IMAP4
    """
    mail_object = IMAP4_SSL(host=imap_mail_server, port=imap_port)
    mail_object.login(user=email_address, password=email_password)
    return mail_object


def get_email_ids(mail_object: IMAP4, label: str = 'INBOX',
                  criteria: str = 'ALL', max_mails_to_look: int = 10) -> list:
    """Get list email id.

    Parameters
    ----------
    mail_object : IMAP4
        The email object after login.
    label : str
        Email label. Default = "INBOX"
    criteria : str
        The search criteria. Default = "ALL"
    max_mails_to_look : int
        The maximum number of elements in the list

    Returns
    -------
    list
        List of email id.
    """
    mail_object.select(label)
    type_, data_ = mail_object.search(None, criteria)
    mail_ids = data_[0]
    id_list_ = mail_ids.split()
    # revers so that latest are at front
    id_list_.reverse()
    id_list_ = id_list_[: min(len(id_list_), max_mails_to_look)]
    return id_list_


def get_email_message(email_object: IMAP4,
                      email_id: Union[int, str, bytes]) -> Message:
    """Get email message

    Parameters
    ----------
    email_object : IMAP4
    email_id : Union[int, str, bytes]
        Email id.

    Returns
    -------
    Message
        the Message object
    """
    email_id = str(int(email_id))
    type_, data_ = email_object.fetch(email_id, '(RFC822)')
    for response_part in data_:
        if isinstance(response_part, tuple):
            return message_from_bytes(response_part[1])


def search_by_subject(email_object: IMAP4,
                      email_ids_list: Union[list, iter],
                      subject_substring: str) -> Message:
    """Search email by its subject.

    Parameters
    ----------
    email_object : IMAP4
    email_ids_list : list
        List email id
    subject_substring : str
        String to search

    Returns
    -------
    Message
    """
    for email_id in email_ids_list:
        msg = get_email_message(email_object=email_object, email_id=email_id)
        if "Subject" not in msg.keys():
            continue
        subject = msg.get("Subject", "")
        if subject_substring.lower() in subject.lower():
            print(subject)
            return msg


def get_mail_info(message_object: Message) -> dict:
    """Get email info.

    This function returns:
    {
        "From": <sender>,
        "To": <receiver>,
        "Subject": <subject>
        "Content": email content in string format
    }

    Parameters
    ----------
    message_object : Message
        The message object

    Returns
    -------
    dict
    """

    email_info = {
        "From": message_object.get("From", ""),
        "To": message_object.get("To", ""),
        "Subject": message_object.get("Subject", ""),
        "Content": ""
    }

    if not message_object.is_multipart():
        content_type = message_object.get_content_type()
        # get the email body
        content = message_object.get_payload(decode=True).decode()
        if content_type == "text/plain":
            email_info["Content"] = content
            return email_info

    # iterate over email parts
    for part in message_object.walk():
        # extract content type of email
        content_type = part.get_content_type()
        content_disposition = str(part.get("Content-Disposition"))

        try:
            email_info["Content"] = part.get_payload(decode=True).decode()
        except AttributeError:
            pass

        if content_type == "text/plain" \
                and "attachment" not in content_disposition:
            return email_info


if __name__ == "__main__":
    mail_ = get_mail_client(imap_mail_server="imap.gmail.com", imap_port=993,
                            email_address="",
                            email_password="")
    id_list = get_email_ids(mail_)
    ms = search_by_subject(email_object=mail_, email_ids_list=id_list,
                           subject_substring="Assigment - 569")
    print(get_mail_info(ms))
