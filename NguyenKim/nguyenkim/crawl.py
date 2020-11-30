from lxml import html
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup 
import csv

listurl=["https://www.nguyenkim.com/tu-lanh/?sort_by=position&sort_order=desc",
"https://www.nguyenkim.com/tivi-man-hinh-lcd/",
"https://www.nguyenkim.com/may-giat/",
"https://www.nguyenkim.com/dien-thoai-di-dong/",
"https://www.nguyenkim.com/may-tinh-xach-tay/",
"https://www.nguyenkim.com/may-lanh/",
"https://www.nguyenkim.com/may-anh/"
]

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
    
    
    

    with open('output.scv','w', encoding="utf8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Title','Price Current','Price Original'])
        for i in listurl:
            url = i
            html_tree = html.fromstring(get_html(url))
            for product in html_tree.xpath("//div[@class='nk-product-desc']"):
                title = product.xpath("./p/span/text()")
                price_current1 = product.xpath("./div/div/div/p/span/span/text()")
                price_current = product.xpath("./div/div/div/p/span/text()")
                if price_current==price_current1:price_current = product.xpath("./div/div/div/p/text()")
                price_original = product.xpath("./div/div/p/span/text()")
                writer.writerow([title,price_current,price_original])

    

    