from urllib.parse import unquote

import requests
from bs4 import BeautifulSoup
import os
from selenium import webdriver
import time

from selenium.webdriver.common.by import By


def get_cookie():
    # Khởi tạo trình duyệt Firefox với Selenium
    driver = webdriver.Firefox()

    # Mở trang web và đăng nhập
    driver.get("http://elib.vku.udn.vn/password-login")
    time.sleep(2)
    username_input = driver.find_element(By.ID,"tlogin_email")
    password_input = driver.find_element(By.ID,"tlogin_password")
    submit_button = driver.find_element(By.NAME, "login_submit")


    username_input.send_keys("anhdn.23itb@vku.udn.vn")
    password_input.send_keys("&3P,)qv*@*A.")
    submit_button.click()

    # Lấy cookie sau khi đã đăng nhập thành công
    cookies = driver.get_cookies()

    # Đóng trình duyệt sau khi đã lấy được cookie
    driver.quit()

    # Xử lý cookie để sử dụng với thư viện requests
    cookie_dict = {cookie['name']: cookie['value'] for cookie in cookies}
    return cookie_dict;


def download_pdf(url, directory, cookies):  # Thêm tham số cookies vào hàm
    # Tạo thư mục nếu nó không tồn tại
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Tải nội dung của trang web với cookie được cung cấp (nếu có)
    response = requests.get(url, cookies=cookies)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Tìm tất cả các liên kết đến các tệp PDF trên trang web
    pdf_links = soup.find_all('a', href=lambda href: (href and href.endswith('.pdf')))

    for link in pdf_links:
        pdf_url = "http://elib.vku.udn.vn" + link['href']
        # Lấy tên tệp từ URL
        filename = os.path.join(directory, os.path.basename(unquote(pdf_url)))
        # Tải xuống tệp PDF
        with open(filename, 'wb') as f:
            f.write(requests.get(pdf_url, cookies=cookies).content)  # Sử dụng cookies ở đây
        print(f"Tệp {filename} đã được tải xuống thành công.")

if __name__ == "__main__":
    # Nhập URL của trang web từ người dùng
    url = input("Nhập URL của trang web: ")
    # Thư mục lưu trữ
    save_directory = input("Nhập tên folder muốn lưu: ")
    #save_directory = "downloaded_pdfs"
    # Tải xuống tệp PDF từ URL đã cung cấp
    cookie = get_cookie()
    download_pdf(url, save_directory, cookie)
    print("="*20 + "\nTải xuống hoàn tất!")
    a = input()

