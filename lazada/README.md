# Giới thiệu
Đây là một crawler đơn giản sử dụng Selenium để thu thập dữ liệu giá thành của sản phẩm trên trang thương mại điện tử [Lazada](https://www.lazada.vn/).
# Những việc đã làm và giải thích mã nguồn
### Cách sử dụng Source Code:
Sau khi cài đặt Selenium và tải source về giải nén sau đó chạy trong Command line bằng lệnh:<br>
```python crawl.py```
### Cài đặt Selenium
Trang web Lazada cũng cấm bot crawl dữ liệu và dữ liệu được trả về bằng javascript trang nên nhóm đã sử dụng Selenium giả lập Client để có thể crawl dữ liệu.
Em cài đặt [Selenium](https://www.selenium.dev/), sau đó tải thêm  ```chromedriver.exe``` để có thể điều khiển được Chrome.
Đoạn code bên dưới sử dụng Selenium để mô phỏng người dùng duyệt Web. Tự động croll trang web, đồng thời trả về source html chứa dữ liệu cần crawl.
```
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
```
### Link sản phẩm
Có nhiều cách để có thể load nhiều trang sản phẩm, tại trang Lazada các trang sản phẩm đều có ở dạng "https://www.lazada.vn/tv-video-am-thanh-thiet-bi-deo-cong-nghe/?page=4&spm=a2o4n.searchlistcategory.cate_3.1.27a2545cpgrRBx", ở đây chỉ cần thay số ở chổ "page=1" thì có thể load sang trang mới. Tạo vòng lặp để crawl dữ liệu.<br>
Tuy nhiên ở Crawler ban đầu này em chỉ sử dụng một list url rồi tạo vong lặp để crawl dữ liệu trong các url đã được định sẵn đó.
### Lấy dữ liệu giá thành sản phẩm và lưu:
Dữ liệu về sản phẩm được format bằng DataFrame thư viện Pandas.<br>
Các cột thông tin gồm có: Category,Name,Price và Url.<br>
Trong đó, Price được chuẩn hóa thành số nguyên không phải dạng chữ như trên website. Và Category dùng để phân chia sản phẩm thành ba loại đó là: Điện thoại di động, Điện tử và Điện lạnh. Dữ liệu được lưu trữ vào file csv để tiện cho việc phân tích và sử dụng dữ liệu sau này.
```
    title = []
    price = []
    url_product = []
    category = []
    for x in url:
        html_tree = html.fromstring(get_html(x))
        category_url_temp = html_tree.xpath("//div[@class='ant-col-20 ant-col-push-4 c1z9Ut']/div[@class='cUQuRr']/h1/text()")[0]
        if(category_url_temp =='Máy Lạnh' or category_url_temp =='Tủ Lạnh' or category_url_temp=='Tủ Đông'):
            category_url = "Điện lạnh"
        elif(category_url_temp == 'Điện Thoại Di Động' or category_url_temp=='Điện Thoại Di Động Nokia Chính Hãng'):
            category_url = "Điện thoại di động"
        else:
            category_url = "Điện tử"
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
    temp.to_csv('output.csv',encoding='utf-8',index = False) 
```
### Kết quả thu được:
Do Selenium là giả danh người dùng nên việc crawl không nhanh như những cách crawl khác nên việc crawl không được nhanh. Kết quả thu được trong trang Lazada là:
- Khoảng 2000 sản phẩm bao gồm : điện thoại di động, điện tử và điện lạnh.
- Thông tin sản phẩm gồm: category, name, price, url.
