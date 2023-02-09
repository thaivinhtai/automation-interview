#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

"""

from test_data.common_variables import SenderEmail

from .based import BasedPage


class LoginScreen(BasedPage):
    def __init__(self):
        super().__init__()
        self.email_field = 'id=com.vsee.vsee.beta:id/loginEmailEdit'
        self.password_field = 'id=com.vsee.vsee.beta:id/loginPasswordEdit'
        self.sign_in_button = 'id=com.vsee.vsee.beta:id/loginSignInBut'

    def sign_in(self, username: str = SenderEmail.username,
                password: str = SenderEmail.password):
        if not self.driver.driver:
            self.driver.set_driver()
        self.driver.logger.info("Sign In to the app.")
        self._send_string_to_locator(self.email_field, username)
        self._send_string_to_locator(self.password_field, password)
        self._click_on_locator(self.sign_in_button)
