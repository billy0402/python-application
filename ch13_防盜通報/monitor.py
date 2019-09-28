import cv2
import monitor_module

gmail_address = 'YOUR EMAIL ADDRESS'
gmail_password = 'YOUR EMAIL PASSWORD'
to_address = ['FIRST TO EMAIL', 'SECOND TO EMAIL']

sid = 'YOUR ACCOUNT SID'
token = 'YOUR AUTH TOKEN'
us_phone = 'YOUR US PHONE'
tw_phone = 'YOUR TW PHONE'

capture = cv2.VideoCapture(0)
image_pre = None
skip = 1  # 設定不比對的次數，由於前影像是空的，略過一次比對
while capture.isOpened():
    is_success, image = capture.read()
    if is_success:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # 灰階處理
        image_now = cv2.GaussianBlur(gray, (13, 13), 5)  # 高斯模糊
        if skip > 0:
            skip -= 1
        else:
            difference = cv2.absdiff(image_now, image_pre)  # 此影格與前影格的差異值
            ret, thresh = cv2.threshold(difference, 25, 255,  # 門檻值
                                        cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(thresh,  # 找到輪廓
                                           cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_SIMPLE)
            if contours:
                print('偵測到移動')
                cv2.drawContours(image, contours, -1, (255, 255, 255), 2)
                message = monitor_module.get_mime_image('小偷入侵', '鷹眼防盜監視器', '警察局', image)
                if message:
                    monitor_module.send_gmail(gmail_address, gmail_password, to_address, message)
                    monitor_module.send_sms('小偷入侵', sid, token, us_phone, tw_phone)
                skip = 200  # 0.05(waitKey) * 200 = 10秒，暫停不比對
            else:
                print('靜止畫面')
        cv2.imshow('frame', image)
        image_pre = image_now.copy()

    keyboard = cv2.waitKey(50)
    if keyboard in (ord('q'), ord('Q')):
        print('退出系統')
        cv2.destroyAllWindows()
        capture.release()
        break
