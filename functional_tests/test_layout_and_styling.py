#!/usr/bin/env python3

from selenium import webdriver
import unittest
from unittest import skip
import sys
from selenium.webdriver.common.keys import Keys
#from django.test import LiveServerTestCase
from .base import FunctionalTest

class LayoutAndStylingTest(FunctionalTest):

    def test_layout_and_styling(self):
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024, 768)

        inputbox = self.get_item_input_box()
        self.assertAlmostEqual(
                inputbox.location['x'] + inputbox.size['width']/2,
                512,
                delta = 6
                )
