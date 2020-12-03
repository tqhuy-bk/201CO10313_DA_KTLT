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
    url = ['https://www.lazada.vn/laptop/?page=3&spm=a2o4n.home.cate_1.3.4b576afeRhRFkd']
    title = []
    price = []
    url_product = []
    category = []
    for x in url:
        html_tree = html.fromstring(get_html(x))
        category_url = html_tree.xpath("//div[@class='ant-col-20 ant-col-push-4 c1z9Ut']/div[@class='cUQuRr']/h1/text()")[0]
        for product in html_tree.xpath("//div[@class='c2prKC']"):
            title_temp = product.xpath(".//div[@class='c16H9d']/a/text()")
            title.append(title_temp[0])
            price_current = product.xpath(".//span[@class='c13VH6']/text()")
            format_price = (int)(price_current[0][:-2].replace(".",""))
            price.append(format_price)
            url_product_one = 'https://' + (product.xpath(".//div[@class='c16H9d']/a/@href")[0])[6:]
            url_product.append(url_product_one)
            category.append(category_url)
    data = {'Category':category,'Name':title,'Price':price,'Url':url_product}
    temp = pandas.DataFrame(data)
    temp.to_csv('out_put.txt')            
    

    

    
