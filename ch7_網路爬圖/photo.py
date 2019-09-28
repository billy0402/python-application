import os

import photo_module

while True:
    category = input('請輸入要下載的圖片類型: ')
    download_limit = int(input('請輸入要下載的數量: '))
    links = photo_module.get_links(category, download_limit)

    if not links:
        print('找不到圖片，請換關鍵字再試試看')
    else:
        print(f'找到的相關圖片有 {len(links)} 張')
        break

if not os.path.exists(category):
    os.makedirs(category)

print('開始下載...')

photo_module.download_pictures_thread(category, links)

print('下載完畢')
