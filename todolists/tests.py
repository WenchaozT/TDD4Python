from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase
from django.urls import resolve
import re

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
        #clear the csrf hidden 清除由于csrf导致的渲染后变化
        csrf_regex = r'<input[^>]+csrfmiddlewaretoken[^>]+>'
        self.assertEqual(
            re.sub(csrf_regex, '', response.content.decode()), 
            re.sub(csrf_regex, '', expected_html)
        )

    def test_home_page_save_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'test item'

        response = home_page(request)
        self.assertIn('test item', response.content.decode())
        expected_html = render_to_string(
            "todolists/home.html",
            {'new_item_text': 'test item'}
        )
        #clear the csrf hidden 清除由于csrf导致的渲染后变化
        csrf_regex = r'<input[^>]+csrfmiddlewaretoken[^>]+>'
        self.assertEqual(
            re.sub(csrf_regex, '', response.content.decode()), 
            re.sub(csrf_regex, '', expected_html)
        )
