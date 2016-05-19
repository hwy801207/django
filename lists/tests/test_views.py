#-*- coding:utf-8 -*-
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.utils.html import escape
from django.template.loader import render_to_string

from unittest import skip

from lists.models import Item, List
from lists.views import home_page
from lists.forms import ItemForm, EMPTY_LIST_ERROR

class HomePageTest(TestCase):

    def test_home_page_renders_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response,'home.html')
        
    def test_home_page_uses_item_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)
        


class NewListTest(TestCase):
        
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
        
    def test_can_save_a_POST_request_to_an_existing_list(self):
#         other_list = List.objects.create()
        correct_list = List.objects.create()
        
        self.client.post(
                         '/lists/%d/' %(correct_list.id),
                         data = { 'text' : 'A new item for an existing list'})
        self.assertEqual(List.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text,'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)
        
    def test_POST_redirectc_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        
        response = self.client.post(
                                    '/lists/%d/' %(correct_list.id,),
                                    data = {'text': 'A new item for an existing list'})
        self.assertRedirects(response, '/lists/%d/'  % (correct_list.id))
        
    def test_validation_errors_end_up_on_lists_page(self):
        list_ = List.objects.create()
        response = self.client.post('/lists/%d/' %(list_.id),
                                    data = {'text': ''}
                                    )
        self.assertEqual(response.status_code, 200 )
        self.assertTemplateUsed(response, 'list.html')
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)
        
        

    
class ListViewTest(TestCase):
    
    def post_invalid_input(self):
        list_ = List.objects.create()
        return self.client.post(
                                '/lists/%d/' %(list_.id,),
                                data = {'text': ''}
                                )

    def test_saving_a_post_request(self):
        self.client.post(
                '/lists/new', data = {'text': 'A new list item'}
                )
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_invalid_list_items_arent_saved(self):
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)
        
    def test_validation_errors_are_sent_back_to_home_page_template(self):
        self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        
        expected_error = escape("You can't have an empty list item")
#         self.assertEqual(expected_error, response.content().decode())
        self.assertContains(response, expected_error)
        
    def test_validation_errors_are_sent_back_to_home_page_template(self):
        response = self.post_invalid_input()
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'list.html')
        
        
    def test_validation_errors_are_shown_on_home_page(self):
        response = self.post_invalid_input()
        self.assertContains(response, escape(EMPTY_LIST_ERROR))
        
    def test_for_invalid_input_passes_form_to_template(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], ItemForm)


    def test_form_save_handles_saving_to_a_list(self):
        list_ = List.objects.create()
        form = ItemForm(data={'text': 'do me'})
        new_item = form.save(for_list = list_)
        self.assertEqual(new_item, Item.objects.first())
        self.assertEqual(new_item.text, "do me")
        self.assertEqual(new_item.list, list_)
       
    @skip
    def test1():
        pass
        
