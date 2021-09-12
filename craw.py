import requests
from bs4 import BeautifulSoup
import re

# Resques data thông qua link
link_base = "https://www.lbar.com/index.php?src=directory&view=rets_flex_active_agents&srctype=rets_flex_active_agents_lister&xsearch_id=rets_flex_active_agents_alpha&xsearch=dummy&query=name.starts.{0}&pos=0,{1},{1}&xsearch_id=rets_flex_active_agents_alpha&xsearch=dummy"

base_domain = "https://www.lbar.com/"

# Lượng data tối đa - giả sử cho tối đa 1 triệu dòng / mục A..Z
maximum_row = 1000000

# Tạo List các request theo các ký tự từ a..z
# Ký tự cuối cùng sẽ là từ a..z trong mã ASCII
list_link =[]
for letter in range(97, 123):
    list_link.append(link_base.format(chr(letter), maximum_row))

# Duyệt qua từng link một
fake_chrome_header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'}

# Mở file ghi ở chế độ ghi đề
# Lưu ý nếu thao tác craw vừa rồi bị ngắt quãng thì cần backup lại kết quả đó
file_name = "result_craw.csv"
file_result = open(file_name, "w")
# Ghi tiêu đề cột vào file csv ở đầu đầu tiên
header_result = "picture_profile,link_profile,name,description,company,address,phone_contact,email_contact,\n"
file_result.write(header_result)

for i in range (len(list_link)):
    print(f"craw Agent by Lastname - letter: ", chr(97+i).title())
    # Phân tích cú pháp và bóc tách data
    link = list_link[i]
    response = requests.get(link, headers=fake_chrome_header)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Trong bài tập này, chỉ có 1 table duy nhất
    # tự tìm hiểm thêm thứ bậc các lớp của HTML
    # data_table = soup.find_all("table")
    # data_tbody = data_table[0].find("tbody")
    data_tr = soup.find_all("tr")
    
    # Duyệt qua từng dòng dữ liệu trong nhóm A
    # Loại bỏ dòng đầu tiên (dòng tiêu đề bảng)
    for row in data_tr[1:]:
        data_td_list = row.find_all("td")
        # Thứ tự trong các td
        # agentPhoto >> agentName >> Address >> Contact
        link_profile = data_td_list[0].find_all("a")[0].get("href")
        link_p = base_domain + link_profile
        
        picture_profile = data_td_list[0].find_all("img")
        
        name = data_td_list[1].text
        names = name.split("\n")
        names.remove("")
        name1 = names[0].strip()
        name2 = names[1].strip()
        
        addr = data_td_list[2].text.replace(",", "-")
        addrs = addr.split("\n")
        addrs.remove("")
        company = addrs[0].strip().replace("\n", "").strip()
        address = addrs[1].strip().replace("\n", "").strip().lstrip()
        
        try:
            email_contact = data_td_list[3].find_all("a")[0].text.strip()
        except:
            email_contact = ""
        try:
            phone_contact = data_td_list[3].text.strip().replace(email_contact, "").rstrip()
        except:
            phone_contact = ""

        str1 = f"{link_p},{name1},{name2},{company},{address},{phone_contact},{email_contact},{picture_profile},\n"

        # Lưu kết quả ra file .csv
        file_result.write(str1)
        print(f"\t- {name1.title()}.")

# Đóng file kết quả lại
file_result.close()
print(f"Done, all results had written in {file_name}.")