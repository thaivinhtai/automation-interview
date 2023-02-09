*** Settings ***
Library  automation_libs.mobile_screen_object.login_screen.LoginScreen
Library  automation_libs.mobile_screen_object.footer_menu.FooterMenu
Library  automation_libs.mobile_screen_object.chat_screen.ChatScreen
Documentation  This module contains BDD keywords for App-related test cases.


*** Keywords ***
The user logs in to the mobile app
    [Documentation]  Sign in to the mobile app with the default user

    sign in

The user starts a new chat and send a message
    [Documentation]  Start a new chat to the demo user and send default message

    navigate to chat screen
    start new chat

The message should be sent
    [Documentation]  Check sent-message.

    check_if_message_is_sent
