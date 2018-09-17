import re

from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase
from django.urls import resolve

from todolists.models import Item
from todolists.views import home_page


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string(
            'todolists/home.html',
        )
        # clear the csrf hidden 清除homepage由于csrf导致的渲染后变化
        csrf_regex = r'<input[^>]+csrfmiddlewaretoken[^>]+>'
        self.assertEqual(
            re.sub(csrf_regex, '', response.content.decode()),
            re.sub(csrf_regex, '', expected_html)
        )

    def test_home_page_save_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'test item'

        home_page(request)

        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Item.objects.first().text, request.POST['item_text'])

    def test_home_page_redirects_after_POST(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'test item'

        response = home_page(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/todolists/worldshare')

    def test_home_page_only_saves_items_necessary(self):
        request = HttpRequest()
        home_page(request)
        self.assertEqual(Item.objects.count(), 0)

        request.method = 'POST'
        request.POST['item_text'] = 'learn'
        home_page(request)
        # response = home_page(request)
        # print(response.content.decode())
        self.assertEqual(Item.objects.count(), 1)


class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'The second item'
        second_item.save()

        saved_items = Item.objects.all()
        # print(saved_items[0].text)
        self.assertEqual(saved_items.count(), 2)
        self.assertEqual([saved_items[0], saved_items[1]],
                         [first_item, second_item])


class ListViewTest(TestCase):

    def test_uses_todolist_template(self):
        response = self.client.get('/todolists/worldshare/')
        self.assertTemplateUsed(response, 'todolists/todolists.html')

    def test_displays_all_items(self):
        Item.objects.create(text='item 1')
        Item.objects.create(text='item 2')

        response = self.client.get('/todolists/worldshare/')

        self.assertContains(response, 'item 1')
        self.assertContains(response, 'item 2')
