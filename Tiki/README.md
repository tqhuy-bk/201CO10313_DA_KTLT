# Giới thiệu
Đây là một crawler đơn giản sử dụng Selenium để thu thập dữ liệu giá thành của sản phẩm trên trang thương mại điện tử [Tiki](www.tiki.vn).
# Những việc đã làm và giải thích mã nguồn
### Cách sử dụng Source Code:
Sau khi cài đặt Selenium và tải source về giải nén sau đó chạy trong Command line bằng lệnh:<br>
```python crawl.py```
### Cài đặt Selenium
Trang web tiki cấm bot crawl dữ liệu từ trang này nên nhóm đã sử dụng Selenium giả lập Client để có thể crawl dữ liệu.
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
Có nhiều cách để có thể load nhiều trang sản phẩm, tại trang Tiki các trang sản phẩm đều có ở dạng "https://tiki.vn/tivi-thiet-bi-nghe-nhin/c4221?src=c.4221.hamburger_menu_fly_out_banner&page=1", ở đây chỉ cần thay số ở chổ "page=1" thì có thể load sang trang mới. Tạo vòng lặp để crawl dữ liệu.<br>
Để có thể crawl dữ liệu lớn thì em sử dụng cách trên và tạo vòng lặp for i in range(1,5) để dễ dàng crawl nhiều dữ liệu hơn.
### Lấy dữ liệu giá thành sản phẩm và lưu:
Dữ liệu về sản phẩm được format bằng DataFrame thư viện Pandas.<br>
Các cột thông tin gồm có: Category,Name,Price và Url.<br>
Trong đó, Price được chuẩn hóa thành số nguyên không phải dạng chữ như trên website. Và Category dùng để phân chia sản phẩm thành ba loại đó là: Điện thoại di động, Điện tử và Điện lạnh. Dữ liệu được lưu trữ vào file csv để tiện cho việc phân tích và sử dụng dữ liệu sau này.
```
    url = ['https://tiki.vn/tu-lanh/c2328?page=']
    title = []
    price = []
    url_product = []
    category = []
    for x in url:
        for i in range(1,16):
            html_tree = html.fromstring(get_html(x+str(i)))
            category_url_temp = html_tree.xpath("//div[@class='CategoryViewstyle__Right-bhstkd-1 fYDhGF']//div[@class='title']/h1/text()")[0]
            if(category_url_temp =='Máy lạnh - Máy điều hòa' or category_url_temp =='Máy nước nóng' or category_url_temp=='Tủ lạnh' or category_url_temp=='Tủ đông - Tủ mát'):
                category_url = "Điện lạnh"
            elif(category_url_temp == 'Điện thoại Smartphone' or category_url_temp == 'Máy tính bảng'):
                category_url = "Điện thoại di động"
            else:
                category_url = "Điện tử"
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
    temp.to_csv('output.csv',encoding='utf-8',index = False)
```
### Kết quả thu được:
Do Selenium là giả danh người dùng nên việc crawl không nhanh như những cách crawl khác nên việc crawl không được nhanh. Kết quả thu được trong trang tiki là:
- Khoảng 3500 sản phẩm bao gồm : điện thoại di động, điện tử và điện lạnh.
- Thông tin sản phẩm gồm: category, name, price, url.

