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
    url = ['https://dienmaycholon.vn/dien-thoai-di-dong-samsung']
    title = []
    price = []
    url_product = []
    category = []
    for x in url:
        html_tree = html.fromstring(get_html(x))
        category_url_temp = html_tree.xpath("//div[@class='first_cate']/h1/text()")[0]
        if(category_url_temp =='Máy Lạnh' or category_url_temp =='Tủ Lạnh' or category_url_temp=='Tủ Đông'):
            category_url = "Điện lạnh"
        elif(category_url_temp == 'Điện Thoại Di Động' or category_url_temp=='Điện Thoại Di Động Nokia Chính Hãng'):
            category_url = "Điện thoại di động"
        else:
            category_url = "Điện tử"
        for product in html_tree.xpath("//div[@class='item_product']"):
            title_temp = product.xpath(".//h3[@class='nameproduct']/text()")
            title.append(title_temp[0][1:-1])
            price_current = product.xpath(".//strong[@class='price_sale line_throught']/text()")
            format_price = (int)(price_current[0][1:].replace(".",""))
            price.append(format_price)
            url_product_one = 'https://dienmaycholon.vn' + (product.xpath(".//div[@class='pro_infomation']/a/@href")[0])[6:]
            url_product.append(url_product_one)
            category.append(category_url)
    data = {'Category':category,'Name':title,'Price':price,'Url':url_product}
    temp = pandas.DataFrame(data)
    temp.to_csv('output.csv',encoding='utf-8',index = False)