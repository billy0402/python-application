import auto_car_module
import cv2
import numpy as np

capture = cv2.VideoCapture('road.mp4')
if capture.isOpened():
    while True:
        is_success, image = capture.read()
        if is_success:
            edge = auto_car_module.get_edge(image)  # 邊緣偵測
            roi = auto_car_module.get_roi(edge)  # 取得 ROI
            lines = cv2.HoughLinesP(image=roi,  # Hough 轉換
                                    rho=3,
                                    theta=np.pi / 180,
                                    threshold=30,
                                    minLineLength=50,
                                    maxLineGap=40)
            average_lines = auto_car_module.get_average_lines(lines)  # 取得左右 2 條平均線方程式
            if average_lines is not None:
                lines = auto_car_module.get_sub_lines(image, average_lines)  # 取得要畫出的左右 2 條線段
                image = auto_car_module.draw_lines(image, lines)  # 畫出線段
            cv2.imshow('Frame', image)
        keyboard = cv2.waitKey(1)
        if keyboard in (ord('q'), ord('Q')):
            print('退出系統')
            cv2.destroyAllWindows()
            capture.release()
            break
else:
    print('開啟攝影機失敗')
