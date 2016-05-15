#!/usr/bin/env python3

from selenium import webdriver
import unittest
from unittest import skip
import sys
from selenium.webdriver.common.keys import Keys
#from django.test import LiveServerTestCase
from .base import FunctionalTest

class ItemValidationTest(FunctionalTest):

    @skip
    def test_can_not_add_empty_list_item(self):
        self.fail("write me")

