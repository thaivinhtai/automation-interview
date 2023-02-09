*** Settings ***
Library  automation_libs.web_page_objects.google_sign_in_pages.GoogleSignInPage
Library  automation_libs.web_page_objects.gmail_page.GmailPage
Library  ../imap_testing_lib.py
Documentation  This module contains BDD keywords for Gmail-related test cases.


*** Keywords ***
The sender logs in to the gmail account
    [Documentation]  Log in to Gmail using the default account.

    access_gmail_url
    sign_in_gmail


The sender sends an email with the default content to the receiver
    [Documentation]  Send an email with the default content and a random number
    ...     to the receiver.

    ${return_number}        send mail
    set global variable         ${THE_RANDOM_NUMBER}        ${return_number}
    sleep   10  # Wait for the email to be sent


The receiver should receive the email with correct content
    [Documentation]     Using IMAP to get the email content and compare with
    ...     the sender one via the random number as a global var.

    ${RECEIVED_EMAIL_INFO}  get email info by subject       ${THE_RANDOM_NUMBER}
    ${RESULT}       compare emails from sender and receiver   ${RECEIVED_EMAIL_INFO}
    ...     ${THE_RANDOM_NUMBER}
    should be true      ${RESULT}       The email of sender and receiver are not match.
