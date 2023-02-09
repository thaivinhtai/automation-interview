#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

"""

from test_data.common_variables import DEFAULT_APP_USER_TO_SEND_MESSAGE, \
    DEFAULT_APP_MESSAGE
from random import randint

from .based import BasedPage


class ChatScreen(BasedPage):
    def __init__(self):
        super().__init__()
        self.new_chat_button = 'id=com.vsee.vsee.beta:id/action_add'
        self.demo_friend = 'xpath=//*[@text="{}"]'
        self.done_button = 'id=com.vsee.vsee.beta:id/action_done'
        self.chat_box = 'id=com.vsee.vsee.beta:id/chatEditText'
        self.send_button = 'id=com.vsee.vsee.beta:id/chatSendBut'
        self.random_num = str(randint(0, 1000))

    def start_new_chat(self, email: str = DEFAULT_APP_USER_TO_SEND_MESSAGE,
                       chat_content: str = DEFAULT_APP_MESSAGE):
        self.driver.logger.info(f"Start new chat with {email}")
        self._click_on_locator(self.new_chat_button)
        self._click_on_locator(
            self.demo_friend.format(DEFAULT_APP_USER_TO_SEND_MESSAGE))
        self._click_on_locator(self.done_button)
        self._send_string_to_locator(self.chat_box,
                                     chat_content + self.random_num)
        self._click_on_locator(self.send_button)

    def check_if_message_is_sent(self,
                                 message: str = DEFAULT_APP_MESSAGE) -> bool:
        self.driver.logger.info("Check the recent message.")
        result = self.driver.wait_explicit(
            condition="visibility_of_element_located",
            locator=f'xpath=//*[@text="{message + self.random_num}"]'
        )
        if not result:
            self.driver.take_screenshot()
            return False
        return True
