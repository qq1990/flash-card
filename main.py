from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
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
    flash_card.itemconfig(card_title, text="French", fill="black")
    flash_card.itemconfig(card_word, text=current_card["French"], fill="black")
    flash_card.itemconfig(card_background, image=CARD_FRONT)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    flash_card.itemconfig(card_title, text="English", fill="white")
    flash_card.itemconfig(card_word, text=current_card["English"])
    flash_card.itemconfig(card_background, image=CARD_BACK)

def know_card():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()

window = Tk()
window.title("Flash Card")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

RIGHT_SYMBOL = PhotoImage(file="images/right.png")
WRONG_SYMBOL = PhotoImage(file="images/wrong.png")
CARD_BACK = PhotoImage(file="images/card_back.png")
CARD_FRONT = PhotoImage(file="images/card_front.png")

right_button = Button(image=RIGHT_SYMBOL, highlightthickness=0, command=know_card)
wrong_button = Button(image=WRONG_SYMBOL, highlightthickness=0, command=next_card)
flash_card = Canvas(height=526, width=800)
card_background = flash_card.create_image(400, 263, image=CARD_FRONT)
card_title = flash_card.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"))
card_word = flash_card.create_text(400, 263, text="word", font=("Ariel", 60, "bold"))

flash_card.config(bg=BACKGROUND_COLOR, highlightthickness=0)
flash_card.grid(column=0, row=0, columnspan=2)

right_button.grid(column=1, row=1)
wrong_button.grid(column=0, row=1)

next_card()


window.mainloop()