import os
import threading

import requests
from bs4 import BeautifulSoup


def get_links(category, download_limit):
    page = 1
    links = list()

    while len(links) <= download_limit:
        url = f'https://pixabay.com/zh/images/search/{category}/?pagi={page}'
        print(url)
        html = requests.get(url)
        html.encoding = 'utf-8'
        soup = BeautifulSoup(html.text, 'lxml')
        photos = soup.select('div.item img')

        if not photos:
            break

        for photo in photos:
            link = photo.get('src')
            if link == '/static/img/blank.gif':
                link = photo.get('data-lazy')
            if link in links:
                return links
            links.append(link)

        page += 1

    return links


def download_picture(url, path):
    picture = requests.get(url)
    index = url.rfind('.')
    path += url[index:]

    with open(path, 'wb+') as file:
        file.write(picture.content)


def download_pictures_thread(category, links):
    download_number = len(links)
    thread_limit = 100
    quotient, remainder = divmod(download_number, thread_limit)

    for i in range(quotient):
        threads = list()
        for j in range(thread_limit):
            thread_number = i * thread_limit + j
            path = category + os.sep + str(thread_number + 1)
            threads.append(threading.Thread(
                target=download_picture,
                args=(links[thread_number], path)
            ))
            threads[j].start()

        for k in threads:
            k.join()

        percentage = (i + 1) * thread_limit / download_number
        print(f'目前進度: {percentage:.2%}')

    threads = list()
    for j in range(remainder):
        thread_number = quotient * thread_limit + j
        path = category + os.sep + str(thread_number + 1)
        threads.append(threading.Thread(
            target=download_picture,
            args=(links[thread_number], path)
        ))
        threads[j].start()

    for k in threads:
        k.join()
    print(f'目前進度: 100.00 %')
