from .base import FunctionalTest
from selenium.webdriver.support.ui import WebDriverWait
import time


TEST_EMAIL = 'cctv@mockmyid.com'

class LoginTest(FunctionalTest):


    def switch_to_new_window(self, text_in_title):
        retries = 60
        while retries > 0:
            for handle in self.browser.window_handles:
                self.browser.switch_to_window(handle)
                print(self.browser.title)
                if text_in_title in self.browser.title:
                    return
            retries -= 1
            time.sleep(0.5)
        self.fail("could ont find window")


    def test_login_with_persona(self):
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('id_login').click()

        self.switch_to_new_window('Mozilla Persona')

        self.browser.find_element_by_id('authentication_email').send_keys(TEST_EMAIL)
        self.browser.find_element_by_tag_name('button').click()

        self.switch_to_new_window('To-Do')

        self.wait_to_be_logged_in(mail=TEST_EMAIL)

        self.browser.refresh()
        self.wait_to_be_logged_in(mail=TEST_EMAIL)

        self.browser.find_element_by_id('id_logout').click()
        self.wait_to_be_logged_out(mail=TEST_EMAIL)

        self.browser.refresh()
        self.wait_to_be_logged_out(mail=TEST_EMAIL)

