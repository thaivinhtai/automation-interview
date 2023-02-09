*** Settings ***
Resource  ../../automation_libs/robot_bdd_keywords/gmail_bdd_keywords.robot


*** Test Cases ***
Verify sending an email from the Gmail and reading using IMAP

    Given The sender logs in to the gmail account
    When The sender sends an email with the default content to the receiver
    Then The receiver should receive the email with correct content
