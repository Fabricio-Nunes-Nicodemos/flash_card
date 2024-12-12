import pandas
import random
from tkinter import *

BACKGROUND_COLOR = "#B1DDC6"
FONT_NAME = "Ariel"
current_card = {}
to_learn = {}


try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(card_background, image=card_front_png)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    global current_card
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background, image=card_back_png)


def is_know():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


# Window
window = Tk()
window.title("Flash Card")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, func=flip_card)


# Card image
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_png = PhotoImage(file="images/card_front.png")
card_back_png = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_png)
card_title = canvas.create_text(400, 150, fill="black", font=(FONT_NAME, 40, "italic"))
card_word = canvas.create_text(400, 263, fill="black", font=(FONT_NAME, 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)


# Wrong button
cross_image = PhotoImage(file="images/wrong.png")
unknow_btn = Button(image=cross_image, highlightthickness=0, command=next_card)
unknow_btn.grid(column=0, row=1)


# Right button
check_image = PhotoImage(file="images/right.png")
known_btn = Button(image=check_image, highlightthickness=0, command=is_know)
known_btn.grid(column=1, row=1)


next_card()


window.mainloop()