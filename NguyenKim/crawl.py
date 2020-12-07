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
    url = ['https://www.nguyenkim.com/dien-thoai-di-dong/page-']
    title = []
    price = []
    url_product = []
    category = []
    for x in url:
        for i in range(1,3):
            html_tree = html.fromstring(get_html(x+str(i)))
            category_url_temp = html_tree.xpath("//div[@class='categories_info']/h2/text()")[0]
            if(category_url_temp =='Máy lạnh - Máy điều hòa' or category_url_temp =='Máy nước nóng' or category_url_temp=='Tủ lạnh' or category_url_temp=='Tủ đông - Tủ mát'):
                category_url = "Điện lạnh"
            elif(category_url_temp == 'Điện Thoại' or category_url_temp == 'Máy tính bảng'):
                category_url = "Điện thoại di động"
            else:
                category_url = "Điện tử"
            for product in html_tree.xpath("//div[@class='item nk-fgp-items nk-new-layout-product-grid']"):
                title_temp = product.xpath(".//div[@class='nk-product-desc']/p/span/text()")
                title.append(title_temp[0]) 
                price_current = product.xpath(".//div[@class='price-now']/p[@class='price-new cate-new']/span/text()")
                format_price = (int)(price_current[0][:-1].replace(".",""))
                price.append(format_price)
                url_product_one =  product.xpath("./a[@class='nk-link-product']/@href")[0]
                url_product.append(url_product_one)
                category.append(category_url)
    data = {'Category':category,'Name':title,'Price':price,'Url':url_product}
    temp = pandas.DataFrame(data)
    temp.to_csv('output.csv',encoding='utf-8',index = False)