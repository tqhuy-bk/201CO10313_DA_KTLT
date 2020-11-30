from lxml import html
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup 
import csv

listurl=["https://dienmaycholon.vn/loa-thanh-soundbar",
"https://dienmaycholon.vn/tivi-led",
"https://dienmaycholon.vn/dan-may",
"https://dienmaycholon.vn/loa-thanh-soundbar",
"https://dienmaycholon.vn/cassette",
"https://dienmaycholon.vn/dau-karaoke",
"https://dienmaycholon.vn/amply",
"https://dienmaycholon.vn/micro",
"https://dienmaycholon.vn/phu-kien-dien-tu",
"https://dienmaycholon.vn/loa-keo",
"https://dienmaycholon.vn/loa-bluetooth-thong-minh"
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
            for product in html_tree.xpath("//div[@class='pro_infomation']"):
                #title1=product.xpath("././/div[@class='_1NoI8_ _1JBBa']/text()")
                title = product.xpath(".//h3[@class='nameproduct']/text()")
                #if title == title1:
                #    title = product.xpath("././/div[@class='_1NoI8_ _16BAGk']/text()")
                price_current = product.xpath(".//strong[@class='price_sale line_throught']/text()")
                price_original = product.xpath("././/span[@class='price_market']/text()")
                writer.writerow([title,price_current,price_original])

    

    