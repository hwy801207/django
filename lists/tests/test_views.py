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

from django.template.loader import render_to_string


class HomePageTest(TestCase):

    def test_root_url_resolve_to_home_page(self):
        found = resolve("/")
        self.assertEqual(found.func, home_page)

    def test_home_page_return_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        self.assertTrue(response.content.startswith(b'<html>'))
        self.assertIn(b'<title>To-Do lists</title>', response.content)
        self.assertTrue(response.content.strip().endswith(b'</html>'))

    def test_home_page_content_compare(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')
        #必须解码
        #self.assertEqual(expected_html, response.content.decode())



class ListViewTest(TestCase):
    

    def test_displays_all_items(self):
        list_ = List.objects.create()
        Item.objects.create(text="itemey 1", list=list_)
        Item.objects.create(text="itemey 2", list=list_)

        other_list = List.objects.create()
        Item.objects.create(text="other list itemey 1", list=other_list)
        Item.objects.create(text="other list itemey 2", list=other_list)


        response = self.client.get('/lists/%d/' %(other_list.id,))

        self.assertContains(response, 'itemey 1') 
        self.assertContains(response, 'itemey 2') 
        self.assertContains(response, 'other list itemey 1') 
        self.assertContains(response, 'other list itemey 2') 

    def test_use_list_template(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/%d/' %(list_.id))
        self.assertTemplateUsed(response, 'list.html')

class NewListTest(TestCase):

    def test_saving_a_post_request(self):
        self.client.post(
                '/lists/new', data = {'item_text': 'A new list item'}
                )


        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_invalid_list_items_arent_saved(self):
        self.client.post('/lists/new', data={'item_text', ""})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)


class NewItemTest(TestCase):
    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        
        self.client.post(
                         '/lists/%d/add_item' %(correct_list.id),
                         data={'item_text': 'A new item for an existing list'}
                         )
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)
        
    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        
        response = self.client.post(
                                    '/lists/%d/add_item' % (correct_list.id),
                                    data = {'item_text': 'A new item for an existing list'}
                                    )
        self.assertRedirects(response, '/lists/%d/' % (correct_list.id,))
    
    def test_passes_correct_list_to_template(self): 
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get('/lists/%d/' %(correct_list.id))
        self.assertEqual(response.context['list'], correct_list)