from datetime import datetime
from time import sleep

import cv2
import numpy as np
import matplotlib.pyplot as plt
# https://github.com/scikit-learn/scikit-learn
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures


def remove_regression(image, border):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # 影像轉灰階
    denoise = cv2.fastNlMeansDenoising(gray, h=30)  # 去除 Noise
    ret, thresh = cv2.threshold(denoise, 127, 255,  # 門檻值轉黑白影像
                                cv2.THRESH_BINARY_INV)
    ori = thresh.copy()
    height, width = thresh.shape
    thresh[:, border:width - border] = 0  # 只留左右 border 寬度邊界的像素
    thresh[height * 3 // 5:height, 0: width // 2] = 0  # 遮掉左下區域
    thresh[height * 1 // 4:height, width // 2: width] = 0  # 遮掉右下區域

    # 機器學習
    border_data = np.where(thresh == 255)  # 取得白點的 x, y 座標
    y_label = border_data[0]  # 1 維, 原始資料的資料標籤(答案)
    samples = y_label.shape[0]  # 共有 samples 個資料
    x = border_data[1].reshape(samples, 1)  # 共有 samples 份的特徵 [[x1], [x2], [x3]…]
    linear_regression = LinearRegression()  # 建立線性迴歸物件
    feature = PolynomialFeatures(degree=2)  # 建立 2 次多項式的特徵物件
    x_input = feature.fit_transform(x)  # 產生二次多項式特徵
    linear_regression.fit(x_input, y_label)  # 建立線性迴歸模型
    # print('二項式係數:', linear_regression.coef_)  # 即 x2、x1
    # print('二項式截距:', linear_regression.intercept_)  # 即 x0

    # 產生迴歸線預測值
    new_x = np.array([i for i in range(width)])  # 製作新的 x 座標特徵
    new_x = new_x.reshape(new_x.shape[0], 1)  # 做成一份一份
    new_x_input = feature.fit_transform(new_x)  # 新的二次項特徵
    new_y = linear_regression.predict(new_x_input)  # 輸入新的輸入資料, 產生預測資料

    # 繪製資料點
    # plt.ylim(bottom=0, top=height)  # 限制 y 軸的範圍 (0～height)
    # plt.scatter(x, height - y_label, color='blue', s=1)  # 繪製原始訓練資料點
    # plt.scatter(new_x, height - new_y, color='red', s=1)  # 繪製預測資料點
    # plt.show()

    # 製造曲線影像
    image_curve = np.zeros_like(ori)  # 產生與原始黑白影像同尺寸的全黑影像
    new_y = new_y.round(0)  # 迴歸線的 y 座標, 去除小數位
    for point in np.column_stack([new_y, new_x]):
        py = int(point[0])  # y 座標位置
        px = int(point[1])  # x 座標位置
        w = 3  # 設定曲線寬度
        image_curve[py - w:py + w, px] = 255  # slice

    difference = cv2.absdiff(ori, image_curve)  # 去除曲線 = 原始影像 - 迴歸線
    denoise = cv2.fastNlMeansDenoising(difference, h=80)  # 強力降噪
    # cv2.imshow('denoise', denoise)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return denoise


# 自動輸入車票資訊
def input_ticket_info(driver):
    driver.find_element_by_id('btn-confirm').click()  # 關閉個人資料使用訊息框
    driver.find_element_by_xpath('//select[@name="selectStartStation"]' +
                                 '//option[@value="2"]').click()  # 起站: 台北
    driver.find_element_by_xpath('//select[@name="selectDestinationStation"]' +
                                 '//option[@value="12"]').click()  # 到站: 左營
    driver.find_element_by_id('trainCon:trainRadioGroup_0').click()  # 標準車廂
    date = driver.find_element_by_id('toTimeInputField')  # 日期欄
    date.clear()  # 先清除內容
    today_date = datetime.now().date().strftime('%Y/%m/%d')
    date.send_keys(today_date)  # 輸入日期
    driver.find_element_by_xpath('//option[@value="530P"]').click()  # 下午5點30
    driver.find_element_by_xpath('//option[@value="1P"]').click()  # 買 1 張學生優惠票


# 自動輸入訂票人資訊
def input_train_and_person(driver):
    driver.find_element_by_name('SubmitButton').click()  # 按【確認車次】鈕
    sleep(1)  # 等待換到下一頁
    driver.find_element_by_id('idNumber').send_keys('F123456789')  # 輸入身分證字號
    driver.find_element_by_id('mobileInputRadio').click()  # 選行動電話單選鈕
    driver.find_element_by_id('mobilePhone').send_keys('0912345678')  # 輸入行動電話
    driver.find_element_by_name('agree').click()  # 按下我已明確了解..高鐵約定事項
    # driver.find_element_by_id("isSubmit").click()  # 按下完成訂位按鈕
