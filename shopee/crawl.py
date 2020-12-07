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
    url = ['https://shopee.vn/%C4%90i%E1%BB%87n-tho%E1%BA%A1i-cat.84.1979?page=',
    'https://shopee.vn/M%C3%A1y-t%C3%ADnh-b%E1%BA%A3ng-cat.84.14026?page=',
    'https://shopee.vn/Pin-s%E1%BA%A1c-d%E1%BB%B1-ph%C3%B2ng-cat.84.2817?page=',
    'https://shopee.vn/Thi%E1%BA%BFt-b%E1%BB%8B-%C3%A2m-thanh-cat.2365.2371?page=',
    'https://shopee.vn/Th%E1%BA%BB-nh%E1%BB%9B-cat.13033.13038?page=',
    'https://shopee.vn/M%C3%A1y-%E1%BA%A3nh-DSLR-cat.13033.13042?page=',
    'https://shopee.vn/M%C3%A1y-%E1%BA%A3nh-kh%C3%B4ng-g%C6%B0%C6%A1ng-l%E1%BA%ADt-cat.13033.13044?page='
    'https://shopee.vn/M%C3%A1y-quay-phim-cat.13033.13052?page=',
    'https://shopee.vn/Qu%E1%BA%A1t-M%C3%A1y-n%C3%B3ng-l%E1%BA%A1nh-cat.2353.2356?page='
    'https://shopee.vn/Thi%E1%BA%BFt-b%E1%BB%8B-ch%C4%83m-s%C3%B3c-qu%E1%BA%A7n-%C3%A1o-cat.2353.9906?page=',
    'https://shopee.vn/M%C3%A1y-h%C3%BAt-b%E1%BB%A5i-Thi%E1%BA%BFt-b%E1%BB%8B-l%C3%A0m-s%E1%BA%A1ch-cat.2353.2358?page=',
    'https://shopee.vn/%C4%90%E1%BB%93-gia-d%E1%BB%A5ng-l%E1%BB%9Bn-cat.2353.2805?page=',
    'https://shopee.vn/Th%E1%BA%BB-nh%E1%BB%9B-cat.13033.13038?page=',
    'https://shopee.vn/Tai-nghe-cat.2365.2370?page=',
    'https://shopee.vn/Thi%E1%BA%BFt-b%E1%BB%8B-%C4%91eo-th%C3%B4ng-minh-cat.2365.13147?page=',
    'https://shopee.vn/Android-Tivi-Box-cat.2365.13145?page=',
    'https://shopee.vn/Tivi-cat.2365.13143?page=',
    'https://shopee.vn/Ph%E1%BB%A5-ki%E1%BB%87n-Thi%E1%BA%BFt-b%E1%BB%8B-game-cat.2365.13898?page='
    ]
    title = []
    price = []
    url_product = []
    category = []
    for x in url:
        for i in range(1,2):
            html_tree = html.fromstring(get_html(x+str(i)))
            category_url_temp = html_tree.xpath("//div[@class='shopee-category-list__category']//a/text()")[0]
            if(category_url_temp =='Máy lạnh - Máy điều hòa' or category_url_temp =='Máy nước nóng' or category_url_temp=='Tủ lạnh' or category_url_temp=='Tủ đông - Tủ mát'):
                category_url = "Điện lạnh"
            elif(category_url_temp == 'Điện Thoại & Phụ Kiện' or category_url_temp == 'Máy tính bảng'):
                category_url = "Điện thoại di động"
            else:
                category_url = "Điện tử"
            for product in html_tree.xpath("//div[@class='col-xs-2-4 shopee-search-item-result__item']"):
                title_temp = product.xpath(".//div[@class='O6wiAW']/div[@class='_1NoI8_ _1JBBaM']/text()")
                if(len(title_temp)==0):
                    title.append(product.xpath(".//div[@class='O6wiAW']/div[@class='_1NoI8_ _16BAGk']/text()")[0])
                else:
                    title.append(title_temp[0]) 
                price_current = product.xpath(".//div[@class='_2lBkmX']//span[@class='_341bF0']/text()")
                format_price = (int)(price_current[0].replace(".",""))
                price.append(format_price)
                url_product_one = 'https://shopee.vn' + product.xpath(".//a/@href")[0]
                url_product.append(url_product_one)
                category.append(category_url)
    data = {'Category':category,'Name':title,'Price':price,'Url':url_product}
    temp = pandas.DataFrame(data)
    temp.to_csv('output.csv',encoding='utf-8',index = False)

    