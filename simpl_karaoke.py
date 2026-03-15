# ---------------------------------------------------
# ІМПОРТИ БІБЛІОТЕК
# ---------------------------------------------------

# Імпорт елементів customtkinter для створення GUI
# Імпортуй: CTk (вікно), CTkButton (кнопка), CTkLabel (текст), CTkCanvas (канва)
from customtkinter import CTk, CTkButton, CTkLabel,CTkCanvas

# Бібліотека для запису та відтворення звуку
import sounddevice as sd

# Імпорт функцій для читання та запису wav файлів
from scipy.io import wavfile

# Бібліотека для роботи з числовими масивами (аудіо)
import numpy as np

# Імпорт функції randint для генерації випадкових чисел
from random import randint


# ---------------------------------------------------
# ШЛЯХИ ДО ФАЙЛІВ
# ---------------------------------------------------

# Шлях до мінусовки
minus_path = "DREVO.wav"

# Шлях до файлу запису
record_path = "DREVO-record.wav"


# ---------------------------------------------------
# ГОЛОВНЕ ВІКНО ПРОГРАМИ
# ---------------------------------------------------

# Створи клас App який успадковує CTk
class App(Ctk):

    # ---------------------------------------------------
    # КОНСТРУКТОР КЛАСУ
    # ---------------------------------------------------

    def __init__(self):
        super().__init__()

        # Виклич конструктор батьківського класу CTk
        # встанови колір фону "#310A31"
        

        # Встанови розмір вікна 600x500
        self.geometry("600x600")

        # Встанови назву вікна "Simple Karaoke"
        self.title("Simple Karaoke")

        # Створи властивість recording
        # вона показує чи зараз іде запис
        self.recording=False

        # Створи властивість playing
        # вона показує чи зараз відтворюється звук
        self.playing = False

        # Виклич метод створення анімації звуку
        self.anime()


        # ---------------------------------------------------
        # ЗАГОЛОВОК
        # ---------------------------------------------------

        # Створи Label
        # текст "Simple Karaoke"
        # колір "#BF9BC6"
        # шрифт Arial розмір 40
        lbl = CTkLabel(self,text="Simple Karaoke",color="#BF9BC6",font = ("Arial",40))

        # Розмісти label у вікні (pack)
        lbl.pack()


        # ---------------------------------------------------
        # КНОПКА ЗАПИСУ
        # ---------------------------------------------------

        # Створи кнопку запису
        # текст "Start"
        # ширина 200
        # висота 100
        # радіус кутів 50
        # кольори "#C52EA7" "#BC8CB7"
        # команда — виклик методу do_record
        self.btn_record = CTkButton(self,text = "Start",width = 200,hight= 100,radius=50,fg_color = "#C52EA7",text_color="#BC8CB7",
                                        command=self.do_record )


        # Додай обробку правої кнопки миші
        # подія "<Button-3>"
        # виклик методу stop_all
        self.btn_record.bind("<Button-3>")


        # Відобрази кнопку у вікні
        self.btn_record.pack()


        # ---------------------------------------------------
        # ІНФОРМАЦІЙНИЙ ТЕКСТ
        # ---------------------------------------------------

        # Створи Label
        # текст "Start record + minus"
        # колір "#DABBD5"
        # розмір 16
        self.lbl_info = CTkLabel(text ="Start record + minus",color = "DABBD5",size = 16) 

        # Розмісти label у вікні
        self.lbl_info.pack()


        # ---------------------------------------------------
        # ДОДАТКОВИЙ ТЕКСТ
        # ---------------------------------------------------

        # Створи label
        # текст "Left click stop all"
        # колір "#DABBD5"
        # розмір 16
        lbl2 = CTkLabel(text = "Left click stop all",color = "DABBD5",size = 16)

        # Відобрази label
        lbl2.pack()



    # ---------------------------------------------------
    # МЕТОД ЗАПИСУ
    # ---------------------------------------------------

    def do_record(self):

        # Якщо запис НЕ йде
        # перевір властивість recording
        if not self.recording:

            # Зупини всі звуки
            sd.stop()

            # Зміни властивість playing на False
            self.playing = False

            # Увімкни запис
            # зміни recording на True
            self.recording = True

            # Зміни текст кнопки на "Stop"
            self.btn_record.configure(text = "Stop")

            # Зміни текст інформаційного label
            # "Recording... Press Stop when done"
            self.lbl_info.configure(text = "Recording... Press Stop when done")


            # ---------------------------------------------------
            # 1. ЧИТАННЯ WAV ФАЙЛУ
            # ---------------------------------------------------

            # Використай wavfile.read()
            # збережи sample rate у self.fs
            # збережи аудіо масив у self.minus
            self.fs,self.minus = wavfile.read(minus_path)


            # ---------------------------------------------------
            # 2. ЗМЕНШЕННЯ ГУЧНОСТІ
            # ---------------------------------------------------

            # self.minus — масив амплітуд
            # помнож на 0.4 щоб зменшити гучність
            # використай astype(self.minus.dtype)
            minus_play = (self.minus * 0.4).astype(self.minus.dtype)


            # ---------------------------------------------------
            # 3. PLAYREC
            # ---------------------------------------------------

            # Використай sd.playrec()
            # аргументи:
            # data — мінусовка
            # samplerate — self.fs
            # channels — 1 (моно)

            # результат запису збережи у self.recording_file
            self.recording_file = sd.player(data = minus_play,samplaret = self.fs,
                                            channels = 1)


        else:

            # ------------------------------------
            # STOP RECORD
            # ------------------------------------

            # Зупини запис sd.stop()
            sd.stop()

            # Зміни recording на False
            self.recording = False

            # Зміни текст кнопки на "Start"
            self.btn_record.configure(text = "Start")
            # Зміни текст label на "Processing and saving..."
            self.lbl_info.configure(text="Processing and saving...")
            # Виклич метод save_file()
            self.save_file()



    # ---------------------------------------------------
    # ЗБЕРЕЖЕННЯ ФАЙЛУ
    # ---------------------------------------------------

    def save_file(self):

        # Переведи запис мікрофона у float
        mic = self.recording_file.astype(np.float32)

        # Візьми мінусовку тієї ж довжини
        minus_cut = self.minus[:len(mic)].astype(np.float32)


        # ---------------------------------------------------
        # ЗМІШУВАННЯ
        # ---------------------------------------------------

        # Додай голос до мінусовки
        mixed = minus_cut + mic

        # Нормалізуй звук
        # щоб амплітуда не перевищувала максимум
        mixed /= np.max(np.abs(mixed))


        # ---------------------------------------------------
        # ЗБЕРЕЖЕННЯ WAV
        # ---------------------------------------------------

        # Використай wavfile.write()
        # аргументи:
        # шлях файлу
        # sample rate
        # звук переведений у int16

        wavfile.write(record_path,self.fs,mixed)


        # ---------------------------------------------------
        # ВІДТВОРЕННЯ
        # ---------------------------------------------------

        # Відтвори результат sd.play()
        sd.play(mixed,self.fs)

        # Встанови playing = True
        self.playing = True



    # ---------------------------------------------------
    # ГЕНЕРАЦІЯ ВИПАДКОВОГО КОЛЬОРУ
    # ---------------------------------------------------

    def random_color(self):

        # Згенеруй RGB значення від 150 до 255
        r = randint(150, 255)
        g = randint(150, 255)
        b = randint(150, 255)

        # Поверни HEX колір
        return f'#{r:02X}{g:02X}{b:02X}'



    # ---------------------------------------------------
    # СТВОРЕННЯ СТОВПЧИКІВ
    # ---------------------------------------------------

    def creat_anime_sound(self):

        # Створи Canvas
        # розмір 890x440
        # фон "#310A31"
        self.canva = CTkCanvas(width = 890,hight = 440,dg= "#310A31") 

        # Розмісти Canvas у координатах (0, 300)
        self.pack(0,300)


        # Створи список стовпчиків
        self.stolp = []


        # Початкова позиція X
        x1 = 10

        # Ширина стовпчика
        w = 60


        # Створи 15 стовпчиків у циклі
        for i in range(15):

            # Випадкова висота 20–400
            h = randint(20,400)

            # Отримай випадковий колір
            color = self.random_color()

            # Розрахуй координату y1
            # 440 - висота стовпчика
            y1 = 440 - h

            # Створи прямокутник
            # аргументи:
            # x1, y1
            # x1 + w
            # 440
            # fill=color
            st = self.canva.creat_regtangle(x1,y1,x1 +w,440,fill = color)

            # Додай стовпчик у список
            self.stolp.append(st)

            # Зміни x1
            # додай ширину стовпчика + 5
            x1 += w+5


        # Запусти анімацію
        self.anime()



    # ---------------------------------------------------
    # АНІМАЦІЯ
    # ---------------------------------------------------

    def anime(self):

        # Якщо іде запис або відтворення
        if self.recording or self.playing:

            # Початкові значення
            x1 = 10
            w = 60

            # Перебери всі стовпчики
            for st in self.stolp:
                # Нова висота
                h = randint(20,400)

                # Новий колір
                color = self.random.color()

                # Нова координата y
                y1 = 440-h


                # Зміни координати стовпчика
                # метод canvas.coords()
                self.canva.coords(st,x1,y1,x1+w,440)


                # Зміни колір
                # метод canvas.itemconfig()
                self.canva.itemconfig(st,fiil = color)

                # Зміни x1
                x1 += w +5


        # Повтор виклику через 150 мс
        self.after(150, self.anime)



    # ---------------------------------------------------
    # ПОВНА ЗУПИНКА
    # ---------------------------------------------------

    def stop_all(self, e):

        # Зупини звук
        sd.stop

        # Встанови playing = False
        self.playing = False

        # Встанови recording = False
        self.recording = False

        # Зміни текст кнопки
        self.btn_record.configure(text = "start")

        # Зміни текст label
        self.lbl_info.configure(text = "Start record or playing")



# ---------------------------------------------------
# ЗАПУСК ПРОГРАМИ
# ---------------------------------------------------

App().mainloop()