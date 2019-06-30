# coding:utf-8

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase
# import unittest


# class NewVistorTest(unittest.TestCase):
class NewVistorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def checkRowInTable(self, exp_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(exp_text, [row.text for row in rows])

    def test4start_a_todolist(self):
        # T想开发一个todo-list,这是首页
        self.browser.get(self.live_server_url)
        # self.browser.get("http://localhost:8000")

        # 检查网页标题和头部是否都包含Todo
        self.assertIn('Todo', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Todo', header_text)

        # 应用邀请她输入一个待办事项
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # T输入了“学习django”
        inputbox.send_keys('learn django')

        # T按回车键后，页面更新，待办事项表格中新增“1：学习django”
        inputbox.send_keys(Keys.ENTER)
        wenchaozURL = self.browser.current_url
        self.assertRegex(wenchaozURL, '/todolists/.+')
        self.checkRowInTable("1: learn django")

        # 页面中仍有文本框，并可以继续输入
        # T输入了“实践使用selenium”
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('learn selenium')
        inputbox.send_keys(Keys.ENTER)

        # 页面再次更新，显示了上述两个事项
        self.checkRowInTable("1: learn django")
        self.checkRowInTable("2: learn selenium")

        # T要确定该网站是否保存他的清单
        # 网站生成了一个URL,并配有相关说明

        # 他访问了生成的URL，显示了之前填入的待办事项

        # 他很满意，关闭了浏览器
        # 避免cookies泄露个人信息
        self.browser.quit()
        print('wenchaoz close windows.')

        # 另一用户creep访问了网站,看不到wenchaoz创建的清单
        self.browser = webdriver.Chrome()
        self.browser.get(self.live_server_url)
        pageText = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Learn django', pageText)
        self.assertNotIn('Learn selenium', pageText)

        # creep输入了“学习django”
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('creep')

        # creep按回车键后，页面更新
        inputbox.send_keys(Keys.ENTER)

        # creep获得了属于他的URL
        creepURL = self.browser.current_url
        self.assertRegex(creepURL, '/todolists/.+')
        self.assertNotEqual(wenchaozURL, creepURL)

        # 只有creep的清单，没有wenchaoz的
        pageText = self.browser.find_element_by_tag_name('body').text
        self.assertIn('creep', pageText)
        self.assertNotIn('Learn django', pageText)
        self.assertNotIn('Learn selenium', pageText)

        # self.fail('Finish the test~')


    def test_layout_and_styling(self):
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=5
        )

        inputbox.send_keys('test\n')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=5
        )
        