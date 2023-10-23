from http.client import IncompleteRead
import os
import pytube as pt
import subprocess
from tqdm import tqdm

#проверяем, есть ли в директории программы папка "Загруженное", если нет, создаем
#также проверяем names.txt
if os.path.isdir('Загруженное'):
    pass
else:
    os.mkdir('Загруженное')
PATH = 'Загруженное'
file = open('names.txt', 'r')

print ("Начало загрузки")

#функция конвертирует скачаный видос в mp4, pytube, вроде скачивает в каком-то мутном формате, который никто не открывает
#для конвертации используем ffmpeg - штука, встроенная в винду (и в мак, и в линь), которая умеет все конвертировать, открывать, редактировать и все такое
#ffmpeg юзаем через subproceess. Он, по сути, открывает новый терминал в винде и вписывает туда запуск ffmpeg
# с try except костыль лютый. Если конвертация не проходит, запускает функцию еще раз. ОЧЕНЬ ВЕРОЯТНО, ЧТО ВСЕ ЗАВИСНЕТ), хз как фиксить, писать надо было быстро
# итератор не итератор, а прост счетчик попыток конвертирования
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

# для каждой строки в файле запускаем по очереди pytube, для каждой ссылки, это свой объект (yt)
for line in lines:
    yt = pt.YouTube(line.strip())
    print(f"Строка принята - {line}")
    n=0
    # снова костыль, который может легко войти в инфинит луп, можно попробовать пофиксить)
    # в бесконечном цикле пытается постоянно обратиться к ютубу за файлом для скачивания, после чего, pytube делает всю магию и присылает файлик
    # если ошибок подключения не вылезает, и все выполняется, выполняется else
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

    # получаем видео из куска потока, который присылает pytube, скачиваем его через свойства объекта(тоже функция pytube)
    vid = stream.get_highest_resolution()
    print("Начало загрузки")
    vid.download(PATH)
    print("Завершение загрузки")

file.close()
print("\tУспешно")