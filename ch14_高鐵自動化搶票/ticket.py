import re
from time import sleep

import cv2
import pytesseract  # https://github.com/madmaze/pytesseract
import ticket_module
from selenium import webdriver

url = 'https://irs.thsrc.com.tw/IMINT/?locale=tw'
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--incognito')
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
driver = webdriver.Chrome('./chromedriver', options=chrome_options)
driver.get(url)
driver.maximize_window()
ticket_module.input_ticket_info(driver)

is_success = False
for try_count in range(20):  # 嘗試破解驗證碼 20 次
    if is_success:
        ticket_module.input_train_and_person(driver)
        break
    print(f'----- 第{try_count + 1}次 -----')

    pass_code_url2 = pass_code_url = driver.find_element_by_id('BookingS1Form_homeCaptcha_passCode') \
        .get_attribute('src')
    re_code_button = driver.find_element_by_id('BookingS1Form_homeCaptcha_reCodeLink') \
        .click()
    # 等待驗證碼更新完成
    while pass_code_url2 == pass_code_url:
        try:
            pass_code_url2 = driver.find_element_by_id('BookingS1Form_homeCaptcha_passCode') \
                .get_attribute('src')
        except:
            pass
        sleep(0.5)

    pass_code_image = driver.find_element_by_id('BookingS1Form_homeCaptcha_passCode')
    # 等待圖檔載入完成
    while pass_code_image.size['width'] < 50 or pass_code_image.size['width'] > 180:
        pass
    pass_code_image.screenshot('pass_code.png')

    wrong = list()
    image = cv2.imread('pass_code.png')
    # 使用範圍 2~15 的 border 寬度進行線性迴歸測試
    for border in range(2, 15):
        result_image = ticket_module.remove_regression(image, border=border)  # 取得去除迴歸線後的影像
        ocr_txt = pytesseract.image_to_string(result_image)  # 對影像進行 OCR 文字辨識
        print('OCR結果:', ocr_txt)
        key = re.sub(r'[^0-9^A-Z]*', '', ocr_txt.upper())
        if len(key) != 4:
            continue

        key = re.sub(r'[0O]', 'Q', key)  # 將 0 或 O 替換為 Q (因驗證碼中不會有0或O)
        if key not in wrong:
            print('輸入驗證碼:', key)
            driver.find_element_by_name('homeCaptcha:securityCode').send_keys(key)
            driver.find_element_by_id('SubmitButton').click()
            sleep(0.5)
            try:
                if driver.find_element_by_class_name('section_title').text:  # 如果有訂位明細元素
                    is_success = True
                    print('驗證成功')
                    break
            except:
                print('驗證失敗')
                wrong.append(key)
                driver.find_element_by_name('homeCaptcha:securityCode').clear()
