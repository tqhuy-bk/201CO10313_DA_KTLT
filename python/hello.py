from lxml import html
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup 
import csv

listurl=[
"https://shopee.vn/%C4%90i%E1%BB%87n-tho%E1%BA%A1i-cat.84.1979",
"https://shopee.vn/%C4%90i%E1%BB%87n-tho%E1%BA%A1i-cat.84.1979?page=0&sortBy=ctime",
"https://shopee.vn/M%C3%A1y-t%C3%ADnh-b%E1%BA%A3ng-cat.84.14026",
"https://shopee.vn/M%C3%A1y-t%C3%ADnh-b%E1%BA%A3ng-cat.84.14026?page=0&sortBy=ctime",
"https://shopee.vn/Pin-s%E1%BA%A1c-d%E1%BB%B1-ph%C3%B2ng-cat.84.2817",
"https://shopee.vn/Pin-s%E1%BA%A1c-d%E1%BB%B1-ph%C3%B2ng-cat.84.2817?page=0&sortBy=ctime",
"https://shopee.vn/Laptop-cat.13030.13065",
"https://shopee.vn/Laptop-cat.13030.13065?page=0&sortBy=ctime",
"https://shopee.vn/Thi%E1%BA%BFt-B%E1%BB%8B-M%E1%BA%A1ng-cat.13030.13079",
"https://shopee.vn/Thi%E1%BA%BFt-B%E1%BB%8B-M%E1%BA%A1ng-cat.13030.13079?page=0&sortBy=ctime",
"https://shopee.vn/Linh-Ki%E1%BB%87n-M%C3%A1y-T%C3%ADnh-cat.13030.13069",
"https://shopee.vn/Linh-Ki%E1%BB%87n-M%C3%A1y-T%C3%ADnh-cat.13030.13069?page=0&sortBy=ctime",
"https://shopee.vn/M%C3%A1y-%E1%BA%A3nh-M%C3%A1y-quay-phim-cat.13033",
"https://shopee.vn/M%C3%A1y-%E1%BA%A3nh-M%C3%A1y-quay-phim-cat.13033?page=0&sortBy=ctime"]

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
            for product in html_tree.xpath("//div[@class='_1gkBDw']"):
                title1=product.xpath("././/div[@class='_1NoI8_ _1JBBa']/text()")
                title = product.xpath("././/div[@class='_1NoI8_ _1JBBaM']/text()")
                if title == title1:
                    title = product.xpath("././/div[@class='_1NoI8_ _16BAGk']/text()")
                price_current = product.xpath("./././/span[@class='_341bF0']/text()")
                price_original = product.xpath("././/div[@class='_1w9jLI QbH7Ig U90Nhh']/text()")
                writer.writerow([title,price_current,price_original])

    

    