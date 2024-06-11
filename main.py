from tkinter import *
import random
import pandas

BACKGROUND_COLOR = "#B1DDC6"
to_learn = {}

# ---------------------------- RANDOM WORDS ------------------------------- #
try:
    data = pandas.read_csv("data/word_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    data_dict = original_data.to_dict('records')

else:
    data_dict = data.to_dict('records')


def random_words():
    global to_learn, timer
    window.after_cancel(str(timer))
    to_learn = random.choice(data_dict)
    canvas.itemconfig(title, text="French", fill="black")
    canvas.itemconfig(word, text=to_learn["French"], fill="black")
    canvas.itemconfig(canvas_image, image=FrontImage)
    timer = window.after(3000, func=Flip_card)


# ---------------------------- FRONT AND BACK ------------------------------- #
def Flip_card():
    canvas.itemconfig(canvas_image, image=BackImage)
    canvas.itemconfig(title, text="English", fill="white")
    canvas.itemconfig(word, text=to_learn["English"], fill="white")


# ---------------------------- KNOW ALREADY ------------------------------- #
def if_yes():
    data_dict.remove(to_learn)
    known = pandas.DataFrame(data_dict)
    known.to_csv("data/word_to_learn.csv", index=False)
    random_words()


# ---------------------------- UI DESIGN ------------------------------- #
window = Tk()
window.title("Flash Cards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
timer = window.after(3000, func=Flip_card)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)

FrontImage = PhotoImage(file="images/card_front.png")
BackImage = PhotoImage(file="images/card_back.png")

canvas_image = canvas.create_image(400, 263, image=FrontImage)
title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

YesImage = PhotoImage(file="images/right.png")
yes = Button(image=YesImage, highlightthickness=0, bd=0, command=if_yes)
yes.grid(column=1, row=1)

NoImage = PhotoImage(file="images/wrong.png")
no = Button(image=NoImage, highlightthickness=0, bd=0, command=random_words)
no.grid(column=0, row=1)

random_words()

window.mainloop()
