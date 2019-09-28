import re
import time

import cv2
import requests

BASE_URL = 'https://westcentralus.api.cognitive.microsoft.com/vision/v2.0'
recognize_url = f'{BASE_URL}/recognizeText?mode=Printed'
KEY = '7fff44ff719f4c6eb1a027d19426ebf2'
headers = {'Ocp-Apim-Subscription-Key': KEY}
headers_stream = {'Ocp-Apim-Subscription-Key': KEY,
                  'Content-Type': 'application/octet-stream'}


def get_license(image):
    print('status: Start')
    is_encode, image_encode = cv2.imencode('.jpg', image)
    if not is_encode:
        return '編碼失敗'

    image_bytes = image_encode.tobytes()
    recognize_response = requests.post(recognize_url,
                                       headers=headers_stream,
                                       data=image_bytes)
    if recognize_response.status_code != requests.codes.accepted:
        print(recognize_response.json())
        return '請求失敗'

    result_url = recognize_response.headers['Operation-Location']
    result_response = requests.get(result_url, headers=headers)
    while result_response.status_code == requests.codes.ok and result_response.json()['status'] != 'Succeeded':
        result_response = requests.get(result_url, headers=headers)
        time.sleep(0.5)
        print('status: ', result_response.json()['status'])
    lines = result_response.json()['recognitionResult']['lines']

    for line in lines:
        text = line['text']
        license_plate = re.match(r'^[\w]{2,4}[-. ][\w]{2,4}$', text).group()
        if license_plate:
            return license_plate
    else:
        return '無法辨識'
