# tk1 - Learning Tk #1
# Very first example of Tk to get an idea how it works
# Copied straight from tutorial
#
# 2018-08-31    PV

import random
import tkinter as tk


class GuessingGame:
    def __init__(self, master):
        self.master = master
        master.title("Guessing Game")

        self.secret_number = random.randint(1, 100)
        self.guess = None
        self.num_guesses = 0

        self.message = "Guess a number from 1 to 100"
        self.label_text = tk.StringVar()
        self.label_text.set(self.message)
        self.label = tk.Label(master, textvariable=self.label_text)

        vcmd = master.register(self.validate) # we have to wrap the command
        self.entry = tk.Entry(master, validate="key", validatecommand=(vcmd, '%P'))

        self.guess_button = tk.Button(master, text="Guess", command=self.guess_number)
        self.reset_button = tk.Button(master, text="Play again", command=self.reset, state=tk.DISABLED)

        self.label.grid(row=0, column=0, columnspan=2, sticky=tk.W+tk.E)
        self.entry.grid(row=1, column=0, columnspan=2, sticky=tk.W+tk.E)
        self.guess_button.grid(row=2, column=0)
        self.reset_button.grid(row=2, column=1)

    def validate(self, new_text):
        if not new_text: # the field is being cleared
            self.guess = None
            return True

        try:
            guess = int(new_text)
            if 1 <= guess <= 100:
                self.guess = guess
                return True
            else:
                return False
        except ValueError:
            return False

    def guess_number(self):
        self.num_guesses += 1

        if self.guess is None:
            self.message = "Guess a number from 1 to 100"

        elif self.guess == self.secret_number:
            suffix = '' if self.num_guesses == 1 else 'es'
            self.message = "Congratulations! You guessed the number after %d guess%s." % (self.num_guesses, suffix)
            self.guess_button.configure(state=tk.DISABLED)
            self.reset_button.configure(state=tk.NORMAL)

        elif self.guess < self.secret_number:
            self.message = "Too low! Guess again!"
        else:
            self.message = "Too high! Guess again!"

        self.label_text.set(self.message)

    def reset(self):
        self.entry.delete(0, tk.END)
        self.secret_number = random.randint(1, 100)
        self.guess = 0
        self.num_guesses = 0

        self.message = "Guess a number from 1 to 100"
        self.label_text.set(self.message)

        self.guess_button.configure(state=tk.NORMAL)
        self.reset_button.configure(state=tk.DISABLED)

root = tk.Tk()
my_gui = GuessingGame(root)
root.mainloop()
