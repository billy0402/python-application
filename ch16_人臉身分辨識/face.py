import face_module

BASE_URL = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0'
KEY = '5ffa5cfdaf804535ab5580caa7c60c60'
gid = 'gp01'
pid = '4b19526e-69a0-4d1a-89f1-285e9cb18c12'

face_module.face_init(BASE_URL, KEY)
face_module.face_use(gid, '')
face_module.face_shot('who')
