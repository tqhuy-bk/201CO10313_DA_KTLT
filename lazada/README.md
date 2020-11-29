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
Dữ liệu về giá và tên sản phẩm thu được từ mỗi sản phẩm sẽ được lưu trong một list và ghi vào file scv:
```
with open('output_test.scv','w', encoding="utf8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Title','Price Current','Price Original'])
        for x in url:
            html_tree = html.fromstring(get_html(x))
            for product in html_tree.xpath("//div[@class='c2prKC']"):
                title = product.xpath(".//div[@class='c16H9d']/a/text()")
                price_current = product.xpath(".//span[@class='c13VH6']/text()")
                price_original = product.xpath(".//span[@class='c1-B2V']/del[@class='c13VH6']/text()")
                if len(price_original) == 0:
                    writer.writerow([title[0],price_current[0],None])
                else:
                    writer.writerow([title[0],price_current[0],price_original[0]])
```
### Kết quả thu được:
Crawler chỉ mới sơ khai chạy theo selenium nên còn khá chậm, code vẫn còn chưa hoàn chỉnh để có thể crawl dữ liệu lớn. Và kết quả thu được:
- Số lượng sản phẩm khoảng 500 sản phẩm.
- Thông tin: Tên sản phẩm, giá hiện tại của sản phẩm và giá trước khi khuyến mãi của sản phẩm.

