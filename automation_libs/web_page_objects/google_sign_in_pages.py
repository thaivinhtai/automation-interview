#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

"""

from selenium.webdriver.common.keys import Keys
from time import sleep
from test_data.common_variables import GMAIL_LOGIN_URL, SenderEmail

from .based import BasedPage


class GoogleSignInPage(BasedPage):
    def __init__(self):
        super().__init__()
        self.email_or_phone_number_field = 'xpath=//input[@type="email"]'
        self.next_button = 'xpath=//div[@id="identifierNext"]/div/button'
        self.password_field = 'xpath=//input[@type="password"]'
        self.login_button = 'xpath=//button[@name="login"]'

    def access_gmail_url(self):
        self.driver.logger.info("Access Gmail login URL.")
        self.driver.go_to_url(GMAIL_LOGIN_URL)

    def sign_in_gmail(self, email: str = SenderEmail.username,
                      password: str = SenderEmail.password):
        self.driver.logger.info("Enter Gmail.")
        self._send_string_to_locator(
                locator=self.email_or_phone_number_field, str_to_be_sent=email
            )
        self.driver.logger.info("Press Enter.")
        self.driver.get_element(
            self.email_or_phone_number_field).send_keys(Keys.RETURN)
        self.driver.logger.info("Enter Password.")
        for try_times in range(5):
            if self.driver.wait_explicit(
                    condition="visibility_of_element_located",
                    locator=self.password_field):
                break
            sleep(1)
        password_field_element = self.driver.get_element(self.password_field)
        self.driver.driver.execute_script("arguments[0].click();",
                                          password_field_element)
        self._send_string_to_locator(
                locator=self.password_field, str_to_be_sent=password
            )
        self.driver.logger.info("Press Enter.")
        self.driver.get_element(self.password_field).send_keys(Keys.RETURN)
