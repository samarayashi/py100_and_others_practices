from tkinter import Tk, Canvas, Label, Entry, Button, Toplevel, PhotoImage
from tkinter import messagebox
from random import choice
from csv import DictReader, DictWriter
from os import path
import time

BACKGROUND_COLOR = "#B1DDC6"
SUB_BG = '#e8d3d1'
voc_list = []
unknown_list = []
current_voc = {}
flip_timer = None
source_file_name = ""


def load_data(csv_name: str):
    # make sure has source file, if have xx_to_learn.csv read it first
    if path.exists(f'./words_resource/{csv_name}_to_learn.csv'):
        with open(f'./words_resource/{csv_name}_to_learn.csv', newline='', encoding='utf-8') as csvfile:
            reader = DictReader(csvfile)
            for row in reader:
                voc_list.append(row)
    elif path.exists(f'./words_resource/{csv_name}.csv'):
        with open(f'./words_resource/{csv_name}.csv', newline='', encoding='utf-8') as csvfile:
            reader = DictReader(csvfile)
            for row in reader:
                voc_list.append(row)
    else:
        messagebox.showinfo(title='No csv file', message=f"Can't find the {csv_name}.csv in words_resource")

    # collect source file information, then call timer and next_card() first time
    if voc_list:
        global source_file_name, flip_timer
        source_file_name = csv_name
        sub_window.destroy()
        window.deiconify()
        flip_timer = window.after(3000, flip_card)
        next_card()


def next_card(known: bool = False):
    global current_voc, flip_timer
    # remove known word, keep a record of unknown word
    if known:
        voc_list.remove(current_voc)
    else:
        unknown_list.append(current_voc)
    window.after_cancel(flip_timer)
    current_voc = choice(voc_list)
    voc_jp = current_voc['jp']
    canvas.itemconfig(card_image, image=card_front)
    canvas.itemconfig(word_text, text=voc_jp, fill='black', font=('Ariel', 50, 'bold'))
    flip_timer = window.after(3000, flip_card)


def flip_card():
    canvas.itemconfig(card_image, image=card_back)
    voc_en = current_voc['en']
    canvas.itemconfig(word_text, text=voc_en, fill='white', font=('Ariel', 40, 'bold'))


def write_unknown_words():
    record_date = time.strftime("%Y%m%d", time.localtime())
    record_time = time.strftime("%I:%M:%S %p", time.localtime())

    # write unknown words into text file
    with open(f'./learning_record/unknown_words_{record_date}.txt', 'a', newline='', encoding='utf-8') as record_file:
        if record_file.tell() != 0:
            record_file.write('\n\n')
        record_file.write(f'Practice time:{record_time}\tResource: ./jp2csv/{source_file_name}\n')
        record_file.write(f'-------------unknown words list follow-----------------\n')
        global unknown_list
        unknown_list = list(filter(None, unknown_list))
        for seq, voc in enumerate(unknown_list, start=1):
            voc_jp = voc['jp']
            voc_en = voc['en'].replace('\n', '\n\t')
            record_file.write(f"{seq}. {voc_jp}: \n\t{voc_en}")
            record_file.write('\n')

    # write xx_to_learn.csv to get current voc_list which has already excluded known word
    with open(f'./words_resource/{source_file_name}_to_learn.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['jp', 'en']
        writer = DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(voc_list)
    window.destroy()


def destroy_all():
    sub_window.destroy()
    window.destroy()


# -------------UI--------------------- #
window = Tk()
window.withdraw()

# ---------show sub window get file name and words source first---------
sub_window = Toplevel(window)
sub_window.title("Choose word collection")
sub_window.config(padx=30, pady=30, bg=SUB_BG)
sub_canvas = Canvas(sub_window, width=500, height=204)
sub_canvas.config(bg=SUB_BG, highlightthickness=0)
jp_logo = PhotoImage(file="./images/JLPT.png")
sub_canvas.create_image(250, 102, image=jp_logo)
sub_canvas.grid(row=0, column=0, columnspan=5)


# config n1~n5 level button
class LevelButton(Button):
    def __init__(self, master, level: str):
        super().__init__(master, text=level, highlightthickness=0, command=lambda: load_data(f'jp_{level.lower()}'),
                         font=("Courier", 15, "bold"), width=4)


# button
n1_button = LevelButton(sub_window, level='N1')
n1_button.grid(row=1, column=0, pady=10)
n2_button = LevelButton(sub_window, level='N2')
n2_button.grid(row=1, column=1)
n3_button = LevelButton(sub_window, level='N3')
n3_button.grid(row=1, column=2)
n4_button = LevelButton(sub_window, level='N4')
n4_button.grid(row=1, column=3)
n5_button = LevelButton(sub_window, level='N5')
n5_button.grid(row=1, column=4)

source_commit_button = Button(sub_window, text="commit", highlightthickness=0,
                              command=lambda: load_data(other_source_entry.get()))
source_commit_button.grid(row=2, column=4)

# label
other_source_label = Label(sub_window, text='Other source file:', bg=SUB_BG, font=("Courier", 10, 'bold'))
other_source_label.grid(row=2, column=0, columnspan=2)

# entry
other_source_entry = Entry(sub_window, width=30)
other_source_entry.grid(row=2, column=2, columnspan=2)
other_source_entry.bind('<Return>', lambda file: load_data(other_source_entry.get()))

# make sure destroy all window(main and sub)
sub_window.protocol("WM_DELETE_WINDOW", destroy_all)

# --------------main windows to show flash card---------------
# canvas
window.title("Flash Card")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
canvas = Canvas(width=800, height=526)
card_front = PhotoImage(file="./images/card_front.png")
card_back = PhotoImage(file='./images/card_back.png')
card_image = canvas.create_image(400, 263, image=card_front)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=1)
word_text = canvas.create_text(400, 263, text='', width=780)
canvas.grid(row=0, column=0, columnspan=2)

# button
check_image = PhotoImage(file="./images/right.png")
known_button = Button(image=check_image, highlightthickness=0, command=lambda: next_card(True))
known_button.grid(row=1, column=0)
cross_image = PhotoImage(file="./images/wrong.png")
unknown_button = Button(image=cross_image, highlightthickness=0, command=lambda: next_card(False))
unknown_button.grid(row=1, column=1)

# when main window close, write unknown words file
window.protocol("WM_DELETE_WINDOW", write_unknown_words)

window.mainloop()
