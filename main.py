from http.client import IncompleteRead
import os
import pytube as pt
import subprocess
from tqdm import tqdm

if os.path.isdir('Загруженное'):
    pass
else:
    os.mkdir('Загруженное')
PATH = 'Загруженное'
file = open('names.txt', 'r')

print ("Начало загрузки")

def convert (inp, outp):
    print("Попытка конвертирования")
    while tqdm(True):
        i=0
        print(f"попытка конвертирования {i}")
        i+=1
        try:
            command = 'ffmpeg -i ' +  inp + outp
            subprocess.run(command)
        except IncompleteRead:
            convert (inp, outp)
        else:
            print("Конвртирование завершено")
            break
        print("\tfailed")


lines = file.readlines()
print("Чтение файла")
for line in lines:
    yt = pt.YouTube(line.strip())
    print(f"Строка принята - {line}")
    n=0
    while True:
        n+=1
        print("Установка соединения:")
        print(f"\tПопытка {n}")
        try:
            print(f"\tПодключение к {line}")
            stream = yt.streams
        except:
            stream = yt.streams
        else:
            print("\tУспешно")
            break

    vid = stream.get_highest_resolution()
    print("Начало загрузки")
    vid.download(PATH)
    print("Завершение загрузки")

file.close()
print("\tУспешно")