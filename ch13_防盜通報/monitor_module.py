import smtplib
from email.mime.image import MIMEImage

import cv2
from twilio.rest import Client  # https://github.com/twilio/twilio-python


def get_mime_image(subject, from_, to, image):
    is_encode, image_encode = cv2.imencode('.jpg', image)
    if not is_encode:
        print('編碼失敗')
        return None
    image_bytes = image_encode.tobytes()

    mime_image = MIMEImage(image_bytes)
    mime_image['Content-type'] = 'application/octet-stream'
    mime_image['Content-Disposition'] = 'attachment; filename="picture.jpg"'
    mime_image['Subject'] = subject
    mime_image['From'] = from_
    mime_image['To'] = to

    return mime_image.as_string()


def send_gmail(gmail_address, gmail_password, to_address, message):
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp_gmail:
        print(smtp_gmail.ehlo())
        print(smtp_gmail.starttls())
        print(smtp_gmail.login(gmail_address, gmail_password))
        status = smtp_gmail.sendmail(gmail_address, to_address, message)
        if not status:
            print('寄信成功')
        else:
            print('寄信失敗', status)


def send_sms(text, sid, token, us_phone, tw_phone):
    client = Client(sid, token)
    sms = client.messages.create(from_=us_phone,
                                 to=tw_phone,
                                 body=text)
    print('簡訊發送時間: ', sms.date_created)
