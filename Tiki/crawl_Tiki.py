from lxml import html
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas
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
    url = ['https://tiki.vn/tivi-thiet-bi-nghe-nhin/c4221?src=c.4221.hamburger_menu_fly_out_banner&page=2']
    title = []
    price = []
    url_product = []
    category = []
    for x in url:
        html_tree = html.fromstring(get_html(x))
        category_url = html_tree.xpath("//div[@class='CategoryViewstyle__Right-bhstkd-1 fYDhGF']//div[@class='title']/h1/text()")[0]
        for product in html_tree.xpath("//a[@class='product-item']"):
            title_temp = product.xpath(".//div[@class='name']/span/text()")
            title.append(title_temp[0]) 
            price_current = product.xpath(".//div[@class='price-discount__price']/text()")
            format_price = (int)(price_current[0][:-2].replace(".",""))
            price.append(format_price)
            url_product_one = 'https://tiki.vn' + product.xpath("@href")[0]
            url_product.append(url_product_one)
            category.append(category_url)
    data = {'Category':category,'Name':title,'Price':price,'Url':url_product}
    temp = pandas.DataFrame(data)
    temp.to_csv('out_put.txt')

    
