import math
import random
import time
from tkinter import *
from tkinter import messagebox


timer = 60  # Must be a multiple of 60
words = ['other', 'new', 'good', 'high', 'old', 'great', 'big', 'american', 'small', 'large', 'national', 'young',
         'different', 'black', 'long', 'little', 'important', 'political', 'bad', 'white', 'real', 'best', 'right',
         'social', 'only', 'public', 'sure', 'low', 'early', 'able', 'human', 'local', 'late', 'hard', 'major',
         'better', 'economic', 'strong', 'possible', 'whole', 'free', 'military', 'true', 'federal', 'international',
         'full', 'special', 'easy', 'clear', 'recent', 'certain', 'personal', 'open', 'red', 'difficult', 'available',
         'likely', 'short', 'single', 'medical', 'current', 'wrong', 'private', 'past', 'foreign', 'fine', 'common',
         'poor', 'natural', 'significant', 'similar', 'hot', 'dead', 'central', 'happy', 'serious', 'ready', 'simple',
         'left', 'physical', 'general', 'environmental', 'financial', 'blue', 'democratic', 'dark', 'various', 'entire',
         'close', 'legal', 'religious', 'cold', 'final', 'main', 'green', 'nice', 'huge', 'popular', 'traditional']
title = "Typing Speed Test"
description = f"Have you ever wondered how fast you can type? Now you have the opportunity to find out!" \
              f" \n\nThe test lasts {timer} seconds. Press the space bar after each word. " \
              f"Once the test is complete, you'll receive your typing speed in characters and words per minute." \
              f"\n\nCheck how much of a keyboard master you are! Good luck!"
font_name = 'Arial'
font_size = 15
index = 0
timer_started = False
correct_words = []
incorrect_words = []


def create_labels_with_words():
    """Creates 10 word labels and arranges them in two rows. Returns a list of created labels."""
    random_words = random.sample(words, 10)
    list_of_labels = []
    for word in random_words:
        text_label = Label(text_frame, text=word, font=(font_name, font_size))
        list_of_labels.append(text_label)

    for i in range(0, 10, 5):
        for j in range(5):
            list_of_labels[i + j].grid(row=i, column=j, padx=5, pady=2)
    return list_of_labels


def next_word():
    """Highlights the current word and moves words in the application."""
    global index
    typing_entry.delete(0, END)
    labels[index].configure(bg="SystemButtonFace")
    index += 1
    labels[index].configure(bg="darkolivegreen1")

    if index == 5:
        old_words = [labels[index + n].cget('text') for n in range(5)]
        new_words = random.sample(words, 5)
        next_set_of_words = old_words + new_words
        for n in range(10):
            labels[n].configure(text=next_set_of_words[n], fg='black', bg="SystemButtonFace")
            index = 0
        labels[index].configure(bg="darkolivegreen1")


def word_check(*args):
    """Checks if the text entered in the Entry field matches the current word."""
    current_word = labels[index].cget('text')
    entered_text = entry_var.get()
    if entered_text != "" and entered_text[-1] == ' ':  # Prevents from typing only spaces
        entered_text = entered_text.strip()
        if entered_text == current_word:
            labels[index].configure(fg='green')
            correct_words.append(entered_text)
            next_word()
        elif len(entered_text) >= len(current_word):
            labels[index].configure(fg='red')
            incorrect_words.append(current_word)
            next_word()
        else:
            labels[index].configure(fg='black')


def keyboard_typed(event):
    """Handles the keys pressed on the keyboard and starts the timer."""
    global timer_started
    if event.char == '\x7f':  # User clicked Ctrl + Backspace
        typing_entry.delete(0, END)

    if not timer_started:
        timer_started = True
        starting_time = time.time() + timer
        time_label.after(1000, count_down, starting_time)

    if event.keysym == 'Return':
        restart_test()
        messagebox.showinfo(title="Enter clicked", message="Use Spaces instead of Enters. It's faster that way.\n\n"
                                                           "Start again.")


def count_down(start_time):
    """It works by updating the timer every second and displaying the test result."""
    if timer_started:
        current_time = time.time()
        difference = round(start_time - current_time)
        time_label.configure(text=f"Time left: {difference}")
        if difference > 0:
            time_label.after(1000, count_down, start_time)
        else:
            cpm, wpm, accuracy = calculate_score()
            message = f"Correct CPM: {cpm}  WPM: {wpm}  Accuracy: {accuracy}%"
            messagebox.showinfo(title="Your score", message=message)
            score_label.configure(text=message)
            restart_test()


def calculate_score():
    """Calculates and returns characters per minute, words per minute and accuracy."""
    one_minute = timer / 60
    characters_in_correct_words = sum([len(word) for word in correct_words])
    cpm = round(characters_in_correct_words / one_minute)
    wpm = math.floor(cpm / 5)

    number_of_correct_words = len(correct_words)
    number_of_all_words = len(correct_words) + len(incorrect_words)
    if number_of_all_words == 0:
        accuracy = 0
    else:
        accuracy = round(number_of_correct_words / number_of_all_words * 100, 2)

    return cpm, wpm, accuracy


def restart_test():
    """Restores all test variables to their initial values"""
    global index, timer_started, correct_words, incorrect_words, labels
    time_label.configure(text=f"Time left: {timer}")
    index = 0
    timer_started = False
    correct_words = []
    incorrect_words = []

    for label in labels:
        label.destroy()
    labels = create_labels_with_words()

    labels[index].configure(bg="darkolivegreen1")
    typing_entry.delete(0, END)


root = Tk()
root.title("Typing Speed Test")
root.geometry('700x450')

# ------------ TITLE AND PROGRAM DESCRIPTION ------------ #
title_label = Label(root, text=title, font=(font_name, font_size+10, "bold"))
program_description = Label(root, text=description, wraplength=640, font=(font_name, font_size - 3))
main_frame = Frame(root, highlightthickness=1, highlightcolor='black')

title_label.pack(pady=10)
program_description.pack(padx=20)
main_frame.pack(pady=25)

# ------------ SCORE DISPLAY ------------ #
score_frame = Frame(main_frame)
recent_score_text = Label(score_frame, text='Recent score:', font=(font_name, font_size - 3))
score_label = Label(score_frame, text="Correct CPM: 0   WPM: 0  Accuracy: 0%", font=(font_name, font_size-3, "bold"))

score_frame.pack(fill='x', expand=True, pady=5)
recent_score_text.pack(side=LEFT, padx=5)
score_label.pack(side=RIGHT, padx=5)

# ------------ TIME AND RESTART BUTTON DISPLAY ------------ #
time_and_reset_frame = Frame(main_frame, highlightthickness=1, highlightbackground='black')
time_label = Label(time_and_reset_frame, text=f"Time left: {timer}", font=(font_name, font_size-3))
restart_btn = Button(time_and_reset_frame, text='Restart', command=restart_test, font=(font_name, font_size-3))

time_and_reset_frame.pack(expand=True, fill='x', ipady=5)
time_label.pack(side=LEFT, padx=20)
restart_btn.pack(side=RIGHT, padx=20)

# ------------ WORDS AND ENTRY FIELD ------------ #

text_frame = Frame(main_frame)
entry_frame = Frame(main_frame)

labels = create_labels_with_words()

labels[index].configure(bg="darkolivegreen1")
entry_var = StringVar()
entry_var.trace_add('write', word_check)
typing_entry = Entry(entry_frame, textvariable=entry_var, font=(font_name, font_size),
                     highlightthickness=1, highlightbackground='black')

text_frame.pack(pady=10)
entry_frame.pack(pady=5)
typing_entry.pack()
typing_entry.focus()

typing_entry.bind("<Key>", keyboard_typed)
root.mainloop()
