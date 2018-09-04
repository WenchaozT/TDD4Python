#coding:utf-8

from selenium import webdriver
import unittest


class NewVistorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test4start_a_todolist(self):
        #T想开发一个todo-list,这是首页
        self.browser.get('http://localhost:8000')

        #检查网页标题
        self.assertIn('To-Do', self.browser.title) 
        self.fail('Finish the test!')

        #应用邀请她输入一个待办事项

        #T输入了“学习django”

        #T按回车键后，页面更新，待办事项表格中新增“1：学习django”

        #页面中仍有文本框，并可以继续输入
        #T输入了“实践使用selenium”

        #页面再次更新，显示了上述两个事项

        #T要确定该网站是否保存他的清单
        #网站生成了一个URL,并配有相关说明

        #他访问了生成的URL，显示了之前填入的待办事项

        #他很满意，关闭了浏览器
        browser.quit()

if __name__ == '__main__':
    unittest.main(warnings='ignore')
    