#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

"""

from .based import BasedPage


class FooterMenu(BasedPage):
    def __init__(self):
        super().__init__()
        self.chat = 'xpath=//*[@content-desc="Chats"]'

    def navigate_to_chat_screen(self):
        self.driver.logger.info("Navigate to the Chat Screen.")
        self._click_on_locator(self.chat)
