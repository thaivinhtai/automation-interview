#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module contains IMAP functions for testing.
"""

import time

from framework_modules.fundamental_auto_libs.imap_util import \
    get_mail_info, get_email_ids, get_mail_client, search_by_subject

from test_data.common_variables import Receiver, IMAP_HOST, IMAP_PORT, \
    SenderEmail, MailContent


def get_email_info_by_subject(random_number: str) -> dict:
    """Get email info by subject from the default receiver user.

    Parameters
    ----------
    random_number : str
        the random number to add to the default subject.

    Returns
    -------
    dict
        {
            "From": <sender>,
            "To": <receiver>,
            "Subject": <subject>
            "Content": email content in string format
        }
    """
    for try_time in range(3):  # Try 3 times
        email_object = get_mail_client(
            imap_mail_server=IMAP_HOST, imap_port=IMAP_PORT,
            email_address=Receiver.username, email_password=Receiver.password
        )
        list_email_id = get_email_ids(mail_object=email_object)
        message_object = search_by_subject(
            email_object=email_object, email_ids_list=list_email_id,
            subject_substring=MailContent.subject.format(random_number))
        if message_object:
            return get_mail_info(message_object)
        time.sleep(5)  # Wait for the email to arrived


def compare_emails_from_sender_and_receiver(
        received_email_info: dict, random_number: str) -> bool:
    """Compare email from sender and receiver.

    Compare if:
        - Email addresses from sender and receiver are match.
        - Subject == Subject
        - Content == Content

    Parameters
    ----------


    Returns
    -------
    bool
        True if all are match
        False if one of them is incorrect
    """
    if SenderEmail.username not in received_email_info.get("From"):
        return False
    if MailContent.subject.format(random_number) \
            != received_email_info.get("Subject"):
        return False
    if MailContent.content.format(random_number) \
            not in received_email_info.get("Content"):
        return False
    return True
