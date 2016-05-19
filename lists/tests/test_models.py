#-*- coding:utf-8 -*-
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.core.urlresolvers import resolve
from django.test import TestCase
from lists.views import home_page
from django.http import HttpRequest
from lists.models import Item, List

from django.core.exceptions import ValidationError


class ItemModelTest(TestCase):
    
    def test_default_text(self):
        item = Item()
        self.assertEqual(item.text, '')

    def test_item_is_related_to_list(self):
        list_ = List.objects.create()
        item = Item()
        item.list = list_
        item.save()
        self.assertIn(item, list_.item_set.all())

    def test_cannot_save_empty_list_items(self):
        list_ = List.objects.create()
        item = Item(list = list_, text="")
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()
            
    def test_duplicate_items_are_invalid(self):
        list_ = List.objects.create()
        Item.objects.create(list=list_, text="bal")
        with self.assertRaises(ValidationError):
            item =  Item(list=list_, text="bal")
            item.full_clean()

    def test_duplicate_items_belong_to_different_list(self):
        list_ = List.objects.create()
        list2_ = List.objects.create()
        Item.objects.create(list=list_, text="bal")
        item = Item(list=list2_, text="bal")
        item.full_clean()

    def test_list_ordering(self):
        list1 = List.objects.create()
        item1 = Item(list=list1, text="item1")
        item2 = Item(list=list1, text="item2")
        item3 = Item(list=list1, text="item3")
        item1.save()
        item2.save()
        item3.save()

        self.assertEqual(list(Item.objects.all()), [item1, item2, item3])


class ListModelTest(TestCase):

    def test_get_absolute_url(self):
        list_=List.objects.create()
        self.assertEqual(list_.get_absolute_url(), '/lists/%d/' %(list_.id))

