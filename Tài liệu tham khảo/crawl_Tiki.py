from lxml import html
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup 
import csv

def get_html(url):
    scroll_to_bottom = True
    browser = webdriver.Chrome()
    browser.maximize_window()
    browser.get(url)
    if scroll_to_bottom:
        last = None
        for v in range(500):
            for k in range(5):
                browser.find_element_by_xpath('//html').send_keys(Keys.DOWN)
            if last is not None and last == browser.execute_script('return window.pageYOffset;'):
                break
            last = browser.execute_script('return window.pageYOffset;')
    html_source = browser.page_source
    browser.quit()
    return html_source

if __name__ == '__main__':
    url = 'https://tiki.vn/deal-hot?src=header_label&_lc=Vk4wMzQwMjAwMDM%253D&tab=now&page=1'
    
    html_tree = html.fromstring(get_html(url))

    with open('output.scv','w', encoding="utf8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Title','Price Current','Price Original'])
        for product in html_tree.xpath("//a[@class='Item__Wrapper-m1oy8w-0 gJJtEe']"):
            title = product.xpath("./div[@class='title']/text()")
            price_current = product.xpath("./p[@class='price']/text()")
            price_original = product.xpath(".//span[@class='original deal']/text()")
            writer.writerow([title,price_current,price_original])

    

    