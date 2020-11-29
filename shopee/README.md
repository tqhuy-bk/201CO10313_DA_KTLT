Cách sử dụng Source Code:
Sau khi cài đặt Selenium và tải source về giải nén sau đó chạy trong Command line bằng lệnh:
python crawl.py

Cài đặt Selenium
Trang web Shopee cấm bot crawl dữ liệu từ trang này nên nhóm đã sử dụng Selenium giả lập Client để có thể crawl dữ liệu. Em cài đặt Selenium, sau đó tải thêm chromedriver.exe để có thể điều khiển được Chrome. Đoạn code bên dưới sử dụng Selenium để mô phỏng người dùng duyệt Web. Tự động croll trang web, đồng thời trả về source html chứa dữ liệu cần crawl.

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
Link sản phẩm
Có nhiều cách để có thể load nhiều trang sản phẩm, tại trang Shopee các trang sản phẩm đều có ở dạng "https://shopee.vn/%C4%90i%E1%BB%87n-tho%E1%BA%A1i-cat.84.1979", ở mỗi sản phẩm ta chỉ cần copy link website thì có thể load sang trang mới. Tạo vòng lặp để crawl dữ liệu.
Tuy nhiên ở Crawler ban đầu này chỉ sử dụng một list url rồi tạo vong lặp để crawl dữ liệu trong các url đã được định sẵn đó.

Lấy dữ liệu giá thành sản phẩm và lưu:
Dữ liệu về giá và tên sản phẩm thu được từ mỗi sản phẩm sẽ được lưu trong một list và ghi vào file scv:

with open('output.scv','w', encoding="utf8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Title','Price Current','Price Original'])
        for i in listurl:
            url = i
            html_tree = html.fromstring(get_html(url))
            for product in html_tree.xpath("//div[@class='_1gkBDw']"):
                title1=product.xpath("././/div[@class='_1NoI8_ _1JBBa']/text()") // tại vì 1 một số tiêu đề của các sản phần khác nhau có 2 loại tên class nên em cố tình tạo ra "title1" rỗng để so sánh ở dưới.
                title = product.xpath("././/div[@class='_1NoI8_ _1JBBaM']/text()")
                if title == title1:
                    title = product.xpath("././/div[@class='_1NoI8_ _16BAGk']/text()")
                price_current = product.xpath("./././/span[@class='_341bF0']/text()")
                price_original = product.xpath("././/div[@class='_1w9jLI QbH7Ig U90Nhh']/text()")
                writer.writerow([title,price_current,price_original])
Kết quả thu được:
Crawler chỉ mới sơ khai chạy theo selenium nên còn khá chậm, code vẫn còn chưa hoàn chỉnh để có thể crawl dữ liệu lớn. Và kết quả thu được:
Thông tin: Tên sản phẩm, giá hiện tại của sản phẩm.Chú ý đến đường truyền mạng vì nếu mạng chậm code sẽ chạy hơi lâu.