#coding:utf-8

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest


class NewVistorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_td_in_tr(self, exp_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(exp_text, [row.text for row in rows])

    def test4start_a_todolist(self):
        #T想开发一个todo-list,这是首页
        self.browser.get('http://localhost:8000')

        #检查网页标题和头部是否都包含Todo
        self.assertIn('Todo', self.browser.title) 
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Todo', header_text)

        #应用邀请她输入一个待办事项
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        #T输入了“学习django”
        inputbox.send_keys('learn django')

        #T按回车键后，页面更新，待办事项表格中新增“1：学习django”
        inputbox.send_keys(Keys.ENTER)
        self.check_td_in_tr("1: learn django")

        #页面中仍有文本框，并可以继续输入
        #T输入了“实践使用selenium”
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('learn selenium')
        inputbox.send_keys(Keys.ENTER)

        #页面再次更新，显示了上述两个事项  
        self.check_td_in_tr("1: learn django")
        self.check_td_in_tr("2: learn selenium")

        #T要确定该网站是否保存他的清单
        #网站生成了一个URL,并配有相关说明

        #他访问了生成的URL，显示了之前填入的待办事项

        #他很满意，关闭了浏览器
        self.browser.quit()

if __name__ == '__main__':
    unittest.main(warnings='ignore')
    