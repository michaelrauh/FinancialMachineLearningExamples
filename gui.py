from tkinter import *
master = Tk()

class user:
    pass

user.q0 = DoubleVar()
user.q1 = DoubleVar()
user.q2 = DoubleVar()
user.q3 = DoubleVar()
user.q4 = DoubleVar()

user.q0.set(1)
user.q1.set(1)
user.q2.set(1)
user.q3.set(1)
user.q4.set(1)

x = StringVar()
x.set("foo")

def callback():
    x.set("bar")

def inc(x):
    x.set(x.get() + .1)

def dec(x):
    x.set(x.get() - .1)

examplebutton = Button(master, text = "What's up?", command = callback)
examplelabel = Label(master, textvariable=x)

title = Label (master, text = "High Profiler", font = "Helvetica 36 bold")
q0_label = Label (master, text = "min", font = "Helvetica 16")
q1_label = Label (master, text = "25%", font = "Helvetica 16")
q2_label = Label (master, text = "median", font = "Helvetica 16")
q3_label = Label (master, text = "75%", font = "Helvetica 16")
q4_label = Label (master, text = "max", font = "Helvetica 16")

q0_inc_button = Button(master, text = "^", command = inc(user.q0))
q1_inc_button = Button(master, text = "^", command = inc(user.q1))
q2_inc_button = Button(master, text = "^", command = inc(user.q2))
q3_inc_button = Button(master, text = "^", command = inc(user.q3))
q4_inc_button = Button(master, text = "^", command = inc(user.q4))

q0_dec_button = Button(master, text = "v", command = dec(user.q0))
q1_dec_button = Button(master, text = "v", command = dec(user.q1))
q2_dec_button = Button(master, text = "v", command = dec(user.q2))
q3_dec_button = Button(master, text = "v", command = dec(user.q3))
q4_dec_button = Button(master, text = "v", command = dec(user.q4))

title.grid(row=0,column=0,columnspan=5)

q0_label.grid(row = 1, column = 0)
q1_label.grid(row = 1, column = 1)
q2_label.grid(row = 1, column = 2)
q3_label.grid(row = 1, column = 3)
q4_label.grid(row = 1, column = 4)

q0_inc_button.grid(row = 2, column = 0)
q1_inc_button.grid(row = 2, column = 1)
q2_inc_button.grid(row = 2, column = 2)
q3_inc_button.grid(row = 2, column = 3)
q4_inc_button.grid(row = 2, column = 4)

q0_dec_button.grid(row = 4, column = 0)
q1_dec_button.grid(row = 4, column = 1)
q2_dec_button.grid(row = 4, column = 2)
q3_dec_button.grid(row = 4, column = 3)
q4_dec_button.grid(row = 4, column = 4)

mainloop()
