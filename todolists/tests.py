import re

from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase
from django.urls import resolve

from todolists.models import Item, List
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


class ListAndItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = 'The first list item'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'The second item'
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        self.assertEqual(saved_items[0], first_item)
        self.assertEqual(saved_items[0].list, list_)
        self.assertEqual(saved_items[1], second_item)
        self.assertEqual(saved_items[1].list, list_)


class ListViewTest(TestCase):

    def test_uses_todolist_template(self):
        list_ = List.objects.create()
        response = self.client.get('/todolists/%d/' % (list_.id,))
        self.assertTemplateUsed(response, 'todolists/todolists.html')

    def test_displays_items_for_that_list(self):
        right_list = List.objects.create()
        Item.objects.create(text='item 1', list=right_list)
        Item.objects.create(text='item 2', list=right_list)
        other_list = List.objects.create()
        Item.objects.create(text='other item', list=other_list)

        response = self.client.get('/todolists/%d/' % (right_list.id,))

        self.assertContains(response, 'item 1')
        self.assertContains(response, 'item 2')
        self.assertNotContains(response, 'other item')

    def test_passes_right_list_to_template(self):
        right_list = List.objects.create()
        response = self.client.get('/todolists/%d/' % (right_list.id,))
        self.assertEqual(response.context['list'], right_list)


class NewListTest(TestCase):

    def test_home_page_save_POST_request(self):
        self.client.post(
            '/todolists/new',
            data={
                'item_text': 'A new item'
            }
        )
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Item.objects.first().text, 'A new item')

    def test_home_page_redirects_after_POST(self):
        response = self.client.post(
            '/todolists/new',
            data={
                'item_text': 'A new item'
            }
        )
        new_list = List.objects.first()
        self.assertRedirects(response, '/todolists/%d/' % (new_list.id,))


class NewItemTest(TestCase):
    def test_save_request_to_old_list(self):
        right_list = List.objects.create()
        _new_item_text = 'An new item for old list'

        self.client.post(
            '/todolists/%d/add_item' % (right_list.id,),
            data={'item_text': _new_item_text}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, _new_item_text)
        self.assertEqual(new_item.list, right_list)

    def test_redirects_list_view(self):
        right_list = List.objects.create()
        _new_item_text = 'An new item for old list'

        response = self.client.post(
            '/todolists/%d/add_item' % (right_list.id,),
            data={'item_text': _new_item_text}
        )

        print(response)
        self.assertRedirects(response, '/todolists/%d/' % (right_list.id,))
