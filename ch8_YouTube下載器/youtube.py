import threading
import tkinter
from tkinter import messagebox

import youtube_module


def button_click():
    url = youtube_url.get().strip()

    if not url:
        messagebox.showerror('錯誤', '請輸入網址')
        return None

    urls = youtube_module.get_urls(url)
    if urls and messagebox.askyesno('確認方塊',
                                    '是否下載清單內所有影片?\n是(Y) = 清單影片\n否(N) = 單一影片'):
        threading.Thread(target=youtube_module.multi_download,
                         args=(urls, list_box)).start()
    else:
        threading.Thread(target=youtube_module.start_download,
                         args=(url, list_box)).start()


# 主視窗
window = tkinter.Tk()
window.geometry('640x480')
window.title('YouTube下載器')
font = ('蘋方體', 12)

# 輸入網址區塊
input_frame = tkinter.Frame(window, bg='red', width=640, heigh=120)
input_frame.pack()

label = tkinter.Label(input_frame, text='請輸入 YouTube 影片網址',
                      bg='red', fg='white', font=font)
label.place(relx=0.5, rely=0.25, anchor='center')

youtube_url = tkinter.StringVar()
entry = tkinter.Entry(input_frame, textvariable=youtube_url, width=40)
entry.place(relx=0.5, rely=0.5, anchor='center')

button = tkinter.Button(input_frame, text='下載影片', command=button_click,
                        bg='#FFD700', fg='black', font=font)
button.place(relx=0.85, rely=0.5, anchor='center')

# 下載清單區塊
download_frame = tkinter.Frame(window, width=640, heigh=360)
download_frame.pack()

label = tkinter.Label(download_frame, text='下載狀態',
                      fg='black', font=font)
label.place(relx=0.5, rely=0.1, anchor='center')

list_box = tkinter.Listbox(download_frame, width=65, height=15)
list_box.place(relx=0.5, rely=0.5, anchor='center')

scroll_bar = tkinter.Scrollbar(download_frame)
scroll_bar.place(relx=0.945, rely=0.5, relheight=0.7, anchor='center')

list_box.config(yscrollcommand=scroll_bar.set)
scroll_bar.config(command=list_box.yview)

window.mainloop()
