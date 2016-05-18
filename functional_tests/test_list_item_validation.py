#!/usr/bin/env python3

from selenium import webdriver
import unittest
from unittest import skip
import sys
from selenium.webdriver.common.keys import Keys
#from django.test import LiveServerTestCase
from .base import FunctionalTest

class ItemValidationTest(FunctionalTest):

    def test_can_not_add_empty_list_item(self):
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('\n')

        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You can't have an empty list item")

        self.get_item_input_box().send_keys('Buy milk')
        self.check_for_row_in_list_table('1: Buy milk')

        self.get_item_input_box().send_keys('\n')

        self.check_for_row_in_list_table('1: Buy milk')
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You can't have an empty list item")
        
        self.get_item_input_box().send_keys('Make tea')
        self.check_for_row_in_list_table('1: Buy milk')
        self.check_for_row_in_list_table('2: Make tea')






       
