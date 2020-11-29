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
Tuy nhiên ở Crawler ban đầu này em chỉ sử dụng một list url rồi tạo vong lặp để crawl dữ liệu trong các url đã được định sẵn đó.
### Lấy dữ liệu giá thành sản phẩm và lưu:
Dữ liệu về giá và tên sản phẩm thu được từ mỗi sản phẩm sẽ được lưu trong một list và ghi vào file scv:
```
with open('output_test.scv','w', encoding="utf8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Title','Price Current'])
        for x in url:
            html_tree = html.fromstring(get_html(x))
            for product in html_tree.xpath("//a[@class='product-item']"):
                title = product.xpath(".//div[@class='name']/span/text()")
                price_current = product.xpath(".//div[@class='price-discount__price']/text()")
                writer.writerow([title[0],price_current[0]])
```
### Kết quả thu được:
Crawler chỉ mới sơ khai chạy theo selenium nên còn khá chậm, code vẫn còn chưa hoàn chỉnh để có thể crawl dữ liệu lớn. Và kết quả thu được:
- Số lượng sản phẩm khoảng 500 sản phẩm.
- Thông tin: Tên sản phẩm, giá hiện tại của sản phẩm.

