import cv2

image = cv2.imread('turn_right.jpg')

# https://docs.opencv.org/2.4/doc/user_guide/ug_traincascade.html
# https://github.com/sauhaardac/Haar-Training
detector = cv2.CascadeClassifier('haar_turnR.xml')
signs = detector.detectMultiScale(image,
                                  scaleFactor=1.1,
                                  minNeighbors=2,
                                  minSize=(30, 30))
if signs is not None:
    for x, y, w, h in signs:
        cv2.rectangle(image,
                      (x, y), (x + w, y + h),
                      (0, 0, 255), 2)
else:
    print('沒有偵測到右轉標誌')

cv2.imshow('Frame', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
