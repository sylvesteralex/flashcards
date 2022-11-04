import tkinter as tk
import random
import pandas as pd


# Static and variables
BACKGROUND_COLOR = "#B1DDC6"
WIDTH, HEIGHT = 900, 626
FONT_NAME = "Arial"
to_learn = {}
random_word_index = None

# main window
window = tk.Tk()
window.title("Flash cards")
window.minsize(WIDTH, HEIGHT)
window.config(padx=WIDTH/10, pady=HEIGHT/10, background=BACKGROUND_COLOR)

# import images
card_front_img = tk.PhotoImage(file="./images/card_front.png")
card_back_img = tk.PhotoImage(file="./images/card_back.png")
right_img = tk.PhotoImage(file="./images/right.png")
wrong_img = tk.PhotoImage(file="./images/wrong.png")

# create canvas
flashcard = tk.Canvas(width=800, height=526)
front = flashcard.create_image(400, 266, image=card_front_img)
flashcard.config(background=BACKGROUND_COLOR, border=0, highlightthickness=0)
card_title = flashcard.create_text(800/2, 526/8, text="Title", font=(FONT_NAME, 30, "italic"))
card_word = flashcard.create_text(800/2, 526/2, text="Word", font=(FONT_NAME, 50, "bold"))
flashcard.grid(column=0, row=0, columnspan=2, pady=(0, HEIGHT/15))

# read csv data
try:
    data_file = pd.read_csv("./data/words_to_learn.csv")
    # df = pd.DataFrame.to_dict(data_file)
except FileNotFoundError:
    orig_data = pd.read_csv("./data/french_words.csv")
    # to_learn = orig_data.to_dict(orient="records")
    to_learn = orig_data.to_dict()
else:
    # to_learn = data_file.to_dict(orient="records")
    to_learn = data_file.to_dict()
finally:
    # print(list(to_learn.keys())[0])
    lang_one = list(to_learn.keys())[0]
    lang_two = list(to_learn.keys())[1]
    list_one = to_learn[lang_one]
    # print(list_one)
    list_two = to_learn[lang_two]


# Show random word on the frontend
def show_random_word():
    # word, translation = pick_word_with_translation()
    global random_word_index

    try:
        random_word_index = random.choice(list(list_one))
        # print(random_word_index)
        word = list_one[random_word_index]
        translation = list_two[random_word_index]
    except IndexError:
        flashcard.itemconfig(card_word, text="There is no words \non the list!", fill="red")
    else:
        flashcard.itemconfig(front, image=card_front_img)
        flashcard.itemconfig(card_word, text=word, fill="black")
        flashcard.itemconfig(card_title, text=lang_one, fill="black")

        def flip_card():
            flashcard.itemconfig(front, image=card_back_img)
            flashcard.itemconfig(card_word, text=translation, fill="white")
            flashcard.itemconfig(card_title, text=lang_two, fill="white")

        window.after(5000, flip_card)


def is_known():
    try:
        to_learn[lang_one].pop(random_word_index)
        to_learn[lang_two].pop(random_word_index)
        new_df = pd.DataFrame(to_learn)
        # new_df.to_csv("./data/words_to_learn.csv", mode='a', index=False, header=False)
        new_df.to_csv("./data/words_to_learn.csv", index=False)
        show_random_word()
    except IndexError:
        flashcard.itemconfig(card_word, text="There is no more words \non the list!", fill="red")


def to_remember():
    new_df = pd.DataFrame(to_learn)
    new_df.to_csv("./data/words_to_learn.csv", index=False)
    show_random_word()


# create buttons
known_word_btn = tk.Button(image=right_img, border=0, highlightthickness=0, command=is_known)
known_word_btn.grid(column=1, row=1)
unknown_word_btn = tk.Button(image=wrong_img, border=0, highlightthickness=0, command=to_remember)
unknown_word_btn.grid(column=0, row=1)


show_random_word()
window.mainloop()
