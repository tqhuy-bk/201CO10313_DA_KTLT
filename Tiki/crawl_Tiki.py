from lxml import html
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
 
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
    url = ['https://tiki.vn/dien-thoai-may-tinh-bang/c1789?src=c.1789.hamburger_menu_fly_out_banner','https://tiki.vn/tivi-thiet-bi-nghe-nhin/c4221?src=c.4221.hamburger_menu_fly_out_banner']
    with open('output.scv','w', encoding="utf8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Title','Price Current','Price Original'])
        for x in url:
            html_tree = html.fromstring(get_html(x))

            
            for product in html_tree.xpath("//a[@class='product-item']"):
                title = product.xpath(".//div[@class='name']/span/text()")
                price_current = product.xpath(".//div[@class='price-discount__price']/text()")
                price_original = product.xpath(".//div[@class='price-discount__discount']/text()") 
                writer.writerow([title,price_current,price_original])

    

    
