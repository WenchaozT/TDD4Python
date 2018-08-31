from selenium import webdriver

browser = webdriver.Chrome()
browser.get('http://localhost:8000')
# browser.get('https://www.baidu.com')

assert 'Django' in browser.title