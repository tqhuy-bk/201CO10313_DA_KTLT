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
    url = ['https://www.lazada.vn/dien-thoai-di-dong/?spm=a2o4n.searchlistcategory.cate_1.1.6ba2bdd5Mxpfhj','https://www.lazada.vn/do-gia-dung-lon/?spm=a2o4n.home.cate_3.3.19056afeiKdxzX','https://www.lazada.vn/tv-video-am-thanh-thiet-bi-deo-cong-nghe/?spm=a2o4n.searchlistcategory.cate_3.1.27a2545cpgrRBx']
    with open('output_test.scv','w', encoding="utf8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Title','Price Current','Price Original'])
        for x in url:

            html_tree = html.fromstring(get_html(x))

    
            for product in html_tree.xpath("//div[@class='c2prKC']"):
                title = product.xpath(".//div[@class='c16H9d']/a/text()")
                price_current = product.xpath(".//span[@class='c13VH6']/text()")
                price_original = product.xpath(".//span[@class='c1-B2V']/del[@class='c13VH6']/text()")
                writer.writerow([title,price_current,price_original])
    

    

    