from tkinter import *
from tkinter import ttk
from pytube import YouTube
from tkinter.messagebox import showinfo, showerror
import threading
import os

def download_audio():
    mp3_link = url_entry.get()
    if mp3_link == '':
        showerror(title='Erro', message='Por favor coloque a MP3 URL')
    else:
        try:
            def on_progress(stream, chunk, bytes_remaining):
                total_size = stream.filesize
                def get_formatted_size(total_size, factor=1024, suffix='B'):
                    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
                        if total_size < factor:
                            return f"{total_size:.2f}{unit}{suffix}"
                        total_size /= factor
                    return f"{total_size:.2f}Y{suffix}"

                formatted_size = get_formatted_size(total_size)
                bytes_downloaded = total_size - bytes_remaining
                percentage_completed = round(bytes_downloaded / total_size * 100)
                progress_bar['value'] = percentage_completed
                progress_label.config(text=str(percentage_completed) + '%, File size:' + formatted_size)
                window.update()
                
            audio = YouTube(mp3_link, on_progress_callback=on_progress)     
            output = audio.streams.get_audio_only().download()
            base, ext = os.path.splitext(output)
            new_file = os.path.expanduser("~/Desktop/") + audio.title + '.mp3'
            os.rename(output, new_file)
            showinfo(title='Download Complete', message='Seu MP3 se encontra na "área de trabalho".')
            progress_label.config(text='')
            progress_bar['value'] = 0           
        except:
            showerror(title='Download Error', message='Um erro aconteceu enquanto tentava ' \
                    'baixar seu MP3\nO que pode ter acontecido: ' \
                    '\n->link invalido\n->Esse arquivo já existe na área de trabalho\n')
            progress_label.config(text='')
            progress_bar['value'] = 0
        
def downloadThread():
    t1 = threading.Thread(target=download_audio)
    t1.start()   

window = Tk()
window.title('MP3 Downloader')
window.geometry('500x250+430+180')
window.resizable(height=FALSE, width=FALSE)

canvas = Canvas(window, width=500, height=250)
canvas.pack()

"""Styles for the widgets"""
label_style = ttk.Style()
label_style.configure('TLabel', foreground='#000000', font=('OCR A Extended', 15))

entry_style = ttk.Style()
entry_style.configure('TEntry', font=('Dotum', 15))

button_style = ttk.Style()
button_style.configure('TButton', foreground='#000000', font='DotumChe')

mp3_label = ttk.Label(window, text='Youtube MP3 Downloader', style='TLabel', foreground="#fff", background="#f00")
canvas.create_window(260, 50, window=mp3_label)

url_label = ttk.Label(window, text='Enter MP3 URL:', style='TLabel', font=(15))
url_entry = ttk.Entry(window, width=72, style='TEntry')

canvas.create_window(90, 90, window=url_label)
canvas.create_window(250, 110, window=url_entry)

progress_label = Label(window, text='')
canvas.create_window(240, 130, window=progress_label)

progress_bar = ttk.Progressbar(window, orient=HORIZONTAL, length=440, mode='determinate')
canvas.create_window(250, 160, window=progress_bar)

download_button = ttk.Button(window, text='Download MP3', style='TButton', command=downloadThread)
canvas.create_window(240, 190, window=download_button)

creditos = ttk.Label(window, text="criador: Marcelo de Oliveira Pugan", font=(6))
canvas.create_window(360, 240, window=creditos)

window.mainloop()
