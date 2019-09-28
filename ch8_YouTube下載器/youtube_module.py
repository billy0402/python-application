import re
import subprocess
import threading
import tkinter

import requests
from bs4 import BeautifulSoup
from pytube import YouTube  # https://github.com/nficano/pytube


def get_urls(url):
    urls = list()
    if '&list' not in url:
        return urls

    response = requests.get(url)
    if response.status_code != requests.codes.ok:
        print('請求失敗')
        return urls

    soup = BeautifulSoup(response.text, 'lxml')
    links = soup.find_all('a')
    base_url = 'https://www.youtube.com/'

    for link in links:
        href = link.get('href')
        url = base_url + href
        if '&index=' in url and url not in urls:
            urls.append(url)

    return urls


# https://github.com/soimort/you-get
def you_get_info(url):
    process = subprocess.Popen(f'you-get -i {url}',
                               shell=True,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    result = process.communicate()
    result_str = str(result[0], 'utf-8')
    if 'title:' not in result_str:
        return None, None

    title = result_str[result_str.find('title:') + 6: result_str.find('streams')].strip()
    itag = result_str[result_str.find('itag:') + 5: result_str.find('container')].strip()
    if len(itag) > 8:  # 如果 itag0 內容有 ESC 資料 (例: b'\x1b[7m137\x1b[0m')
        itag = itag[4:-4]  # 去除、前後4個 ESC 字元
    return title, itag


def you_get_download(url, itag=None):
    cmd = 'you-get '
    if itag:
        cmd += f'--itag={itag} '
    process = subprocess.Popen(cmd + url,
                               shell=True,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.wait()
    return process.returncode  # 0 = OK


lock = threading.Lock()


def set_list_box(list_box, position, status, info):
    lock.acquire()

    if position < 0:  # 新增項目
        position = list_box.size()
        list_box.insert(tkinter.END, f'{status} {position + 1:02d} {info}')
    else:  # 更新項目
        list_box.delete(position)
        list_box.insert(position, f'{status} {position + 1:02d} {info}')

    lock.release()

    return position


def start_download(url, list_box):
    position = set_list_box(list_box, -1, '◌ 讀取中...', url)
    title, best = you_get_info(url)

    if not title:
        try:
            youtube = YouTube(url)
            title = youtube.title
        except:
            pass

    if not title:
        set_list_box(list_box, position, '✖ 影片無法讀取 (設為私人影片、已刪除或網址錯誤)', url)
        return None
    else:
        set_list_box(list_box, position, '○ 下載中...', title)

    if best:
        print('use you-get')
        you_get_download(url)
    else:
        print('use pytube')
        youtube.streams.first().download()

    set_list_box(list_box, position, '● 影片下載完成', title)


def multi_download(urls, list_box):
    thread_limit = 20
    urls.sort(key=lambda x: int(re.search(r'index=(\d+)', x).group(1)))
    for url in urls:
        while threading.activeCount() >= thread_limit:
            pass
        threading.Thread(target=start_download,
                         args=(url, list_box)).start()
