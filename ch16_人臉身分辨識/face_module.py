import sqlite3
import time
from datetime import datetime

import chat_bot_module
import cv2
import requests

BASE_URL = ''
KEY = ''
gid = ''
pid = ''
headers_stream = {}
headers_json = {}
headers = {}


def face_init(b, k):
    global BASE_URL, KEY, headers_stream, headers_json, headers
    BASE_URL = b
    KEY = k
    headers_stream = {'Ocp-Apim-Subscription-Key': KEY,
                      'Content-Type': 'application/octet-stream'}
    headers_json = {'Ocp-Apim-Subscription-Key': KEY,
                    'Content-Type': 'application/json'}
    headers = {'Ocp-Apim-Subscription-Key': KEY}


def face_use(g, p):
    global gid, pid
    gid = g
    pid = p


def face_add(image):
    is_encode, image_encode = cv2.imencode('.jpg', image)
    if is_encode:
        print('編碼失敗')
        return None
    image_bytes = image_encode.tobytes()

    face_url = f'{BASE_URL}/persongroups/{gid}/persons/{pid}/persistedFaces'
    response = requests.post(face_url,
                             headers=headers_stream,
                             data=image_bytes)
    if response.status_code == requests.codes.ok:
        print('新增臉部成功')
    else:
        print('新增臉部失敗:', response.text)


def face_detect(image):
    detect_url = f'{BASE_URL}/detect?returnFaceId=true'
    is_encode, image_encode = cv2.imencode('.jpg', image)
    if is_encode:
        print('編碼失敗')
        return None
    image_bytes = image_encode.tobytes()

    response = requests.post(detect_url,
                             headers=headers_stream,
                             data=image_bytes)
    if response.status_code == requests.codes.ok:
        face = response.json()
        if face:
            face_id = face[0]['faceId']
            return face_id
        else:
            print("照片中沒有偵測到人臉")


def face_identify(face_id):
    identify_url = f'{BASE_URL}/identify'
    body = str({'personGroupId': gid,
                'faceIds': [face_id]})
    response = requests.post(identify_url,
                             headers=headers_json,
                             data=body)
    if response.status_code == requests.codes.ok:
        person = response.json()
        if person[0]['candidates']:
            person_id = person[0]['candidates'][0]['personId']
            print(person_id)
            return person_id
        else:
            return None


def face_who(image):
    face_id = face_detect(image)
    person_id = face_identify(face_id)

    if person_id:
        persons = person_list(gid)
        for person in persons:
            if person_id == person['personId']:
                name = person['name']
                print(f'歡迎: {name}')
                chat_bot_module.bot_speak_re(f'歡迎: {name}')
                db_save('mydb.sqlite', person['name'])
                db_check('mydb.sqlite')
    else:
        print('查無相符身分')
        chat_bot_module.bot_speak('查無相符身分', 'zh-tw')


def person_list(gid):
    person_url = f'{BASE_URL}/persongroups/{gid}/persons'
    response = requests.get(person_url,
                            headers=headers)
    if response.status_code == requests.codes.ok:
        print('查詢人員完成')
        return response.json()
    else:
        print("查詢人員失敗:", response.json)


def db_save(db, name):
    connect = sqlite3.connect(db)
    sql = 'CREATE TABLE IF NOT EXISTS my_table ("name" TEXT, "punch_time" TEXT)'
    connect.execute(sql)
    save_time = str(datetime.now().strftime('%Y-%m-%d %H.%M.%S'))
    sql = f'INSERT INTO my_table VALUES ("{name}", "{save_time}")'
    connect.execute(sql)
    connect.commit()
    connect.close()


def db_check(db):
    try:
        connect = sqlite3.connect(db)
        connect.row_factory = sqlite3.Row
        sql = 'SELECT * FROM my_table'
        cursor = connect.execute(sql)
        dataset = cursor.fetchall()
        key1, key2 = dataset[0].keys()
        print(f'{key1}\t{key2}')
        print('----\t----')
        for name, save_time in dataset:
            print(f'{name}\t{save_time}')
    except:
        print('讀取資料庫錯誤')
    finally:
        connect.close()


def face_shot(action_type):
    is_count = False
    face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    capture = cv2.VideoCapture(0)
    while capture.isOpened():
        is_success, image = capture.read()
        if not is_success:
            print('讀取影像失敗')
            continue

        image_copy = image.copy()
        faces = face_detector.detectMultiScale(
            image,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(200, 200))

        if len(faces) == 1:
            if not is_count:
                t1 = time.time()
                is_count = True
            counter = 5 - int(time.time() - t1)

            for x, y, width, height in faces:
                cv2.rectangle(
                    image_copy, (x, y), (x + width, y + height),
                    (0, 255, 255), 2)
                cv2.putText(
                    image_copy, str(counter),
                    (x + int(width / 2), y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 255, 255), 2)

            if counter == 0:
                is_count = False
                filename = datetime.now().strftime('%Y-%m-%d %H.%M.%S')
                cv2.imwrite(filename + '.jpg', image)

                if action_type == 'add':
                    face_add(image)
                elif action_type == 'who':
                    face_who(image)

        else:
            is_count = False

        cv2.imshow('Frame', image_copy)
        k = cv2.waitKey(1)
        if k in (ord('q'), ord('Q')):
            print('退出系統')
            cv2.destroyAllWindows()
            capture.release()
            break
    else:
        print('開啟攝影機失敗')
