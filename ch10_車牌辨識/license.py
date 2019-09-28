import cv2  # https://github.com/opencv/opencv/tree/master/samples/python
import license_module

capture = cv2.VideoCapture(0)
if capture.isOpened():
    while True:
        is_success, image = capture.read()
        if is_success:
            cv2.imshow('Frame', image)
        else:
            print('無法讀取影像')
            break

        keyboard = cv2.waitKey(100)
        if keyboard in (ord('s'), ord('S')):
            cv2.imwrite('snapshot.jpg', image)
            text = license_module.get_license(image)
            print('車牌辨識結果: ', text)

        if keyboard in (ord('q'), ord('Q')):
            print('退出系統')
            cv2.destroyAllWindows()
            capture.release()
            break
else:
    print('開啟攝影機失敗')
