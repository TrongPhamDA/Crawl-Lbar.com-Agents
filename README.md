# crawl-Lbar.com-Agents
 Video hướng dẫn gốc: youtube.com/watch?v=NUF_Av4mJgM
 Thực hiện biên soạn lại code: Trọng, Phạm - (84) 0349816784

 Website cần crawl: https://www.lbar.com/agents/
 (menu: CONSUMERS > Find a REALTER)

 Sử dụng trình duyệt Chrome để tìm hiểu cấu trúc HTML của web
 F12 > Network

 Trang web này request thẳng ra url chứ không request qua API

 Sử dụng library: beautifulsoup4 và requests
 pip install beautifulsoup4
 pip install requests

 Khi gặp lỗi "ModuleNotFoundError: No module named 'requests'" trong môi trường VSCode
 thì kiểm tra Python version của Terminal và IDE
 Terminal: python --version
 IDE: nhìn ở góc dưới bên trái (nếu không đồng nhất thì bấm vào IDE version và chọn lại cho phù hợp)

 Hướng dẫn sử dụng beautifulsoup4
 https://www.crummy.com/software/BeautifulSoup/bs4/doc

 from bs4 import BeautifulSoup
soup = BeautifulSoup(html_doc, 'html.parser')

------------

Website có thể phát hiện request đang làm bởi bot
nên search "add header request python like chrome"

Provide a User-Agent header:

import requests
url = 'http://www.ichangtou.com/#company:data_000008.html'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'}

response = requests.get(url, headers=headers)
print(response.content)

----
Trong từng dòng dữ liệu sẽ có cấu trúc các cột dữ liệu:
    Hình ảnh
    Tên
    Địa chỉ
    Liên hệ
Tìm hiểu cấu truc HTML cùng với method find_all() để tìm thông tin tương ứng.

-----
Xử lý các string thì cần đến:
    strip() tương tự trim()
    lstrip() và rstrip() để loại các dấu tab
    replace("\n", "") để loại bỏ các dấu xuống dòng
    split("\n") để tách 1 string thành các string với delimiter là dấu \n

---
Sau khi đã crawl xong:
cần làm thao tác làm sạch bước cuối với các trình soạn thảo dễ dùng hơn, cụ thể là Excel - Power Query
- làm sạch đường dẫn ảnh profile, chỉ giữ lại link ảnh (file .jpg)
- nếu data nào ko có ảnh thì để trống, không để khung ảnh giữ chổ (file .gif)
- làm sạch (Transform > Trim, hoặc Capitalize, hoặc Upper case) các cột chữ (Tên, Địa chỉ, Công ty)
và cuối cùng là xuất trở về dạng csv để gửi cho client cho gọn gàng.