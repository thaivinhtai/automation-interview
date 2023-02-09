#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

"""

from selenium.webdriver.common.keys import Keys
from .based import BasedPage
from typing import Union

from test_data.common_variables import Receiver, MailContent
from random import randint


class GmailPage(BasedPage):
    def __init__(self):
        super().__init__()
        self.new_email_button = 'xpath=//div[@class="z0"]/div'
        self.send_to_address_field = 'xpath=//div[@class="afp"]//input'
        self.subject_field = 'xpath=//input[@name="subjectbox"]'
        self.content_field = 'xpath=//td[@class="Ap"]/div/div[@role="textbox"]'
        self.send_mail_button = 'xpath=//div[@class="dC"]/div[1]'

    def send_mail(self, receivers: Union[str, list] = Receiver.username,
                  subject: str = MailContent.subject,
                  content: str = MailContent.content) -> str:
        """Send email with default subject and content plus a random number.

        Parameters
        ----------
        receivers : [list, str]
            Receiver address or list of receivers' address.
        subject : str
            Email subject
        content : str
            Email content

        Returns
        -------
        str
            A random number in str format for comparing from the receiver side.
        """

        self.driver.logger.info("Send email")
        self._click_on_locator(self.new_email_button)
        list_receiver = []
        if type(receivers) == str:
            list_receiver = [receivers]
        else:
            list_receiver += receivers
        for receiver in list_receiver:
            self.driver.logger.debug(
                f"Input '{receiver}' to the address field.")
            self._send_string_to_locator(self.send_to_address_field, receiver)
            self.driver.get_element(
                self.send_to_address_field
            ).send_keys(Keys.ENTER)
        random_number = str(randint(0, 1000))
        self.driver.logger.debug(f"Input '{subject.format(random_number)}' "
                                 f"to the subject field.")
        self._send_string_to_locator(self.subject_field,
                                     subject.format(random_number))
        self.driver.logger.debug(f"""Input 
        '{content.format(random_number)}' 
        to the content field.""")
        self._click_on_locator(self.content_field)
        self._send_string_to_locator(self.content_field,
                                     content.format(random_number))
        self._click_on_locator(self.send_mail_button)
        return random_number
