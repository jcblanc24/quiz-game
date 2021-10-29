import tkinter.ttk
from tkinter import *
from tkinter import messagebox
import sqlite3
import time
import random
from PyDictionary import PyDictionary
from googletrans import Translator, LANGUAGES
import pygame


# -------------------------------------------- The Sign Up Page -------------------------------------------------
def signUpPage():
    root.destroy()
    global sign_up
    sign_up = Tk()

    # The size of the window
    sign_up.geometry('800x600+255+80')
    sign_up.resizable(width=False, height=False)
    sign_up.title('Quiz Game')
    sign_up.iconbitmap('icon.ICO')

    # The variables
    full_name = StringVar()
    username = StringVar()
    password = StringVar()
    country = StringVar()

    # Canvas
    canvas = Canvas(sign_up, width=800, height=740, bg='SkyBlue2')
    canvas.pack()
    frame1 = Frame(canvas, bg='white')
    frame1.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

    # -----The Labels and The Entries
    label_heading = Label(frame1, text='Quiz App SignUp', font=('Calibri', 40), bg='white')
    label_heading.place(relx=0.2, rely=0.1)

    # full name
    label_name = Label(frame1, text='Full Name', fg='black', bg='white')
    label_name.place(relx=0.21, rely=0.4)
    name_entry = Entry(frame1, bg='#d3d3d3', fg='black', textvariable=full_name)
    name_entry.config(width=42)
    name_entry.place(relx=0.31, rely=0.4)

    # username
    label_username = Label(frame1, text='Username', fg='black', bg='white')
    label_username.place(relx=0.21, rely=0.5)
    username_entry = Entry(frame1, bg='#d3d3d3', fg='black', textvariable=username)
    username_entry.config(width=42)
    username_entry.place(relx=0.31, rely=0.5)

    # password
    label_password = Label(frame1, text='Password', fg='black', bg='white')
    label_password.place(relx=0.21, rely=0.6)
    password_entry = Entry(frame1, bg='#d3d3d3', fg='black', textvariable=password, show='*')
    password_entry.config(width=42)
    password_entry.place(relx=0.31, rely=0.6)

    # country
    label_country = Label(frame1, text='Country', fg='black', bg='white')
    label_country.place(relx=0.21, rely=0.7)
    country_entry = Entry(frame1, bg='#d3d3d3', fg='black', textvariable=country)
    country_entry.config(width=42)
    country_entry.place(relx=0.31, rely=0.7)

    def add_user_to_database():
        fullname = name_entry.get()
        uname = username_entry.get()
        pwd = password_entry.get()
        cty = country_entry.get()

        conn = sqlite3.connect('Quiz.db')
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS user(
            full_name Varchar(150),
            user_name Varchar(50),
            password Varchar(100),
            country Varchar(100))""")
        cur.execute("""INSERT INTO user(full_name, user_name, password, country) VALUES(?,?,?,?)""",
                    (fullname, uname, pwd, cty))
        conn.commit()
        cur.execute("""SELECT * FROM user""")
        result = cur.fetchall()
        print(result)
        conn.close()
        loginPage(result)

    def already_have_account():
        conn = sqlite3.connect('Quiz.db')
        cur = conn.cursor()
        conn.commit()
        cur.execute("""SELECT * FROM user """)
        result = cur.fetchall()
        loginPage(result)

    # SignUp Button
    signup_button = Button(frame1, text='SignUp', bg='#d3d3d3', padx=5, pady=5, width=5, command=add_user_to_database)
    signup_button.configure(width=15, height=1, activebackground="#33B5E5", relief=FLAT)
    signup_button.place(relx=0.4, rely=0.8)

    # Already have a account Button
    log_button = Button(frame1, text='Already have an Account?', bg='white', padx=5, pady=5, width=5,
                        command=already_have_account)
    log_button.config(width=18, height=1, activebackground="#33B5E5", relief=FLAT)
    log_button.place(relx=0.38, rely=0.9)

    sign_up.mainloop()


# -------------------------------------------- The Login Page -------------------------------------------------
def loginPage(logdata):
    sign_up.destroy()
    global login
    login = Tk()

    # The size of the window
    login.geometry('800x600+255+80')
    login.resizable(width=False, height=False)
    login.title('Quiz Game')
    login.iconbitmap('icon.ICO')

    # The variables
    username = StringVar()
    password = StringVar()

    # Canvas
    canvas = Canvas(login, width=800, height=740, bg='SkyBlue2')
    canvas.pack()
    frame1 = Frame(canvas, bg='white')
    frame1.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

    # -----The Labels and The Entries
    label_heading = Label(frame1, text='Quiz App Login', font=('Calibri', 40), bg='white')
    label_heading.place(relx=0.2, rely=0.1)

    # username
    label_username = Label(frame1, text='Username', fg='black', bg='white')
    label_username.place(relx=0.21, rely=0.4)
    username_entry = Entry(frame1, bg='#d3d3d3', fg='black', textvariable=username)
    username_entry.config(width=42)
    username_entry.place(relx=0.31, rely=0.4)

    # password
    label_password = Label(frame1, text='Password', fg='black', bg='white')
    label_password.place(relx=0.215, rely=0.5)
    password_entry = Entry(frame1, bg='#d3d3d3', fg='black', textvariable=password, show='*')
    password_entry.config(width=42)
    password_entry.place(relx=0.31, rely=0.5)

    def check():
        for a, b, c, d in logdata:
            if b == username_entry.get() and c == password_entry.get():
                login.destroy()
                main_menu()
                break
        else:
            messagebox.showerror('Error', 'Wrong Username and Password')
            username_entry.delete(0, END)
            password_entry.delete(0, END)

    # Login Button
    log = Button(frame1, text='Login', padx=5, pady=5, width=5)
    log.configure(width=15, height=1, activebackground="#33B5E5", relief=FLAT, command=check)
    log.place(relx=0.4, rely=0.6)

    login.mainloop()


# -------------------------------------------- True or False -------------------------------------------------
def true_or_false():
    global true_false
    true_false = Tk()

    # The size of the window
    true_false.geometry('800x600+255+80')
    true_false.resizable(width=False, height=False)
    true_false.title('Quiz Game')
    true_false.iconbitmap('icon.ICO')

    # Canvas
    canvas = Canvas(true_false, width=800, height=740, bg='SkyBlue2')
    canvas.pack()
    frame1 = Frame(true_false, bg='white')
    frame1.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

    def countDown():
        check = 0
        for k in range(15, 0, -1):

            if k == 1:
                check = -1
            timer.configure(text=k)
            frame1.update()
            time.sleep(1)

        timer.configure(text="Times up!")
        if check == -1:
            return -1
        else:
            return 0

    global score
    score = 0

    question = [
        ["Bollywood is the nickname of Britain's movie industry.", 'False'],
        ["Death Valley is the lowest, hottest, and driest area of North America.", 'True'],
        ["The biceps muscle in the upper arm is the strongest muscle\n in the human body.", 'False'],
        ["Apartheid was the political system dismantled in South Africa\n at the end of the 20th century.", 'True'],
        ["Brazil has won more World cup (soccer) championships than any other.", 'True']
    ]

    li = ['', 0, 1, 2, 3, 4]
    x = random.choice(li[1:])

    # ------ The Label and The RadioButtons
    question_label = Label(frame1, text=question[x][0], font="calibri 16", bg="white")
    question_label.place(relx=0.5, rely=0.2, anchor=CENTER)

    var = StringVar()

    answer_a = Radiobutton(frame1, text='True', font="calibri 14", value='True', variable=var,
                           bg="white")
    answer_a.place(relx=0.5, rely=0.45, anchor=CENTER)
    answer_b = Radiobutton(frame1, text='False', font="calibri 14", value='False', variable=var,
                           bg="white")
    answer_b.place(relx=0.5, rely=0.55, anchor=CENTER)

    li.remove(x)

    timer = Label(true_false)
    timer.place(relx=0.8, rely=0.82, anchor=CENTER)

    def display():
        if len(li) == 1:
            true_false.destroy()
            showMark(score)
        if len(li) == 2:
            next_question_button.configure(text='End', command=calc)

        if li:
            x = random.choice(li[1:])
            question_label.configure(text=question[x][0])

            answer_a.configure(text="True", value='True')

            answer_b.configure(text="False", value='False')

            li.remove(x)
            print(li)
            y = countDown()
            if y == -1:
                display()

    # Calculate the score
    def calc():
        global score
        if var.get() == question[x][1]:
            score += 1
        else:
            pass
        display()

    # The Buttons
    submit_button = Button(frame1, text='Submit', command=calc)
    submit_button.place(relx=0.5, rely=0.82, anchor=CENTER)

    next_question_button = Button(frame1, text='Next', command=display)
    next_question_button.place(relx=0.87, rely=0.82, anchor=CENTER)

    y = countDown()
    if y == -1:
        display()
        true_false.mainloop()


# -------------------------------------------- Vocabulary -------------------------------------------------
def vocabulary():
    global vocabu
    vocabu = Tk()

    # The size of the window
    vocabu.geometry('800x600+255+80')
    vocabu.resizable(width=False, height=False)
    vocabu.title('Quiz Game')
    vocabu.iconbitmap('icon.ICO')

    # Canvas
    canvas = Canvas(vocabu, width=800, height=740, bg='SkyBlue2')
    canvas.pack()
    frame1 = Frame(vocabu, bg='white')
    frame1.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

    def countDown():
        check = 0
        for k in range(15, 0, -1):

            if k == 1:
                check = -1
            timer.configure(text=k)
            frame1.update()
            time.sleep(1)

        timer.configure(text="Times up!")
        if check == -1:
            return -1
        else:
            return 0

    global score
    score = 0

    question = [
        ['Contrite', 'obedient', 'sorry', 'shameless', 'nervous'],
        ['bereavement', 'sympathy', 'grief', 'dream', 'trend'],
        ['entice', 'fight', 'slip', 'relax', 'tempt'],
        ['diversity', 'development', 'stress', 'variety', 'improvement'],
        ['scion', 'heir', 'patient', 'commander', 'dwarf']
    ]

    global answer
    answer = ['sorry', 'grief', 'tempt', 'variety', 'heir']

    li = ['', 0, 1, 2, 3, 4]
    x = random.choice(li[1:])

    # ------ The Label and The RadioButtons
    question_label = Label(frame1, text=question[x][0], font="courier 26 bold", bg="white")
    question_label.place(relx=0.5, rely=0.2, anchor=CENTER)

    var = StringVar()

    answer_a = Radiobutton(frame1, text=question[x][1], font="calibri 18", value=question[x][1], variable=var,
                           bg="white")
    answer_a.place(relx=0.5, rely=0.35, anchor=CENTER)

    answer_b = Radiobutton(frame1, text=question[x][2], font="calibri 18", value=question[x][2], variable=var,
                           bg="white")
    answer_b.place(relx=0.5, rely=0.45, anchor=CENTER)

    answer_c = Radiobutton(frame1, text=question[x][3], font="calibri 18", value=question[x][3], variable=var,
                           bg="white")
    answer_c.place(relx=0.5, rely=0.55, anchor=CENTER)

    answer_d = Radiobutton(frame1, text=question[x][4], font="calibri 18", value=question[x][4], variable=var,
                           bg="white")
    answer_d.place(relx=0.5, rely=0.65, anchor=CENTER)

    li.remove(x)

    timer = Label(vocabu)
    timer.place(relx=0.8, rely=0.82, anchor=CENTER)

    def display():
        if len(li) == 1:
            vocabu.destroy()
            showMark(score)
        if len(li) == 2:
            next_question_button.configure(text='End', command=calc)

        if li:
            x = random.choice(li[1:])
            question_label.configure(text=question[x][0])

            answer_a.configure(text=question[x][1], value=question[x][1])

            answer_b.configure(text=question[x][2], value=question[x][2])

            answer_c.configure(text=question[x][3], value=question[x][3])

            answer_d.configure(text=question[x][4], value=question[x][4])

            li.remove(x)
            print(li)
            y = countDown()
            if y == -1:
                display()

    # Calculate the score
    def calc():
        global score
        if var.get() in answer:
            pygame.mixer.init()
            pygame.mixer.music.load("audios/ding.wav")
            pygame.mixer.music.play()
            score += 1
        else:
            pygame.mixer.music.load("audios/miss.wav")
            pygame.mixer.music.play()
        display()

    # The Buttons
    submit_button = Button(frame1, text='Submit', command=calc)
    submit_button.place(relx=0.5, rely=0.82, anchor=CENTER)

    next_question_button = Button(frame1, text='Next', command=display)
    next_question_button.place(relx=0.87, rely=0.82, anchor=CENTER)

    y = countDown()
    if y == -1:
        display()
        vocabu.mainloop()


# -------------------------------------------- Name That Thing -------------------------------------------------
def name_thing():
    global name_thing
    name_thing = Tk()

    # The size of the window
    name_thing.geometry('800x600+255+80')
    name_thing.resizable(width=False, height=False)
    name_thing.title('Quiz Game')
    name_thing.iconbitmap('icon.ICO')

    # Canvas
    canvas = Canvas(name_thing, width=800, height=740, bg='SkyBlue2')
    canvas.pack()

    def countDown():
        check = 0
        for k in range(15, 0, -1):

            if k == 1:
                check = -1
            timer.configure(text=k)
            name_thing.update()
            time.sleep(1)

        timer.configure(text="Times up!")
        if check == -1:
            return -1
        else:
            return 0

    img = [
        [PhotoImage(file='images/Chat.PNG')],
        [PhotoImage(file='images/Ches.PNG')],
        [PhotoImage(file='images/C_ma.PNG')],
        [PhotoImage(file='images/C_pi.PNG')],
        [PhotoImage(file='images/C-bo.PNG')]
    ]
    answer = ['pi', 'go', 'machete', 'lynx', 'flank']
    li = [0, 1, 2, 3, 4]
    x = random.choice(li)

    image_container = canvas.create_image(400, 150, image=img[x])

    global proposition
    proposition = [
        ['lynx', 'manx', 'cougar', 'abyssinian'],
        ['kendo', 'toro', 'ginza', 'go'],
        ['sabere', 'machete', 'rapier', 'stilleto'],
        ['degree', 'pi', 'yen', 'clef'],
        ['pocket', 'ditch', 'flank', 'rub']
    ]

    global var
    var = StringVar()

    answer_a = Radiobutton(name_thing, text=proposition[x][0], font="calibri 18", value=proposition[x][0], variable=var,
                           bg="SkyBlue2")
    answer_a.place(relx=0.5, rely=0.42, anchor=CENTER)

    answer_b = Radiobutton(name_thing, text=proposition[x][1], font="calibri 18", value=proposition[x][1], variable=var,
                           bg="SkyBlue2")
    answer_b.place(relx=0.5, rely=0.52, anchor=CENTER)

    answer_c = Radiobutton(name_thing, text=proposition[x][2], font="calibri 18", value=proposition[x][2], variable=var,
                           bg="SkyBlue2")
    answer_c.place(relx=0.5, rely=0.62, anchor=CENTER)

    answer_d = Radiobutton(name_thing, text=proposition[x][3], font="calibri 18", value=proposition[x][3], variable=var,
                           bg="SkyBlue2")
    answer_d.place(relx=0.5, rely=0.72, anchor=CENTER)

    timer = Label(name_thing)
    timer.place(relx=0.87, rely=0.88, anchor=CENTER)

    global score
    score = 0

    def display():
        if len(li) == 1:
            name_thing.destroy()
            showMark(score)
        if len(li) == 2:
            next_question_button.configure(text='End', command=calc)
        if li:
            x = random.choice(li)
            canvas.itemconfig(image_container, image=img[x])
            answer_a.configure(text=proposition[x][0], value=proposition[x][0])
            answer_b.configure(text=proposition[x][1], value=proposition[x][1])
            answer_c.configure(text=proposition[x][2], value=proposition[x][2])
            answer_d.configure(text=proposition[x][3], value=proposition[x][3])

            li.remove(x)
            y = countDown()
            if y == -1:
                display()

    # Calculate the score
    def calc():
        global score
        if var.get() in answer:
            score += 1
            print(score)
        else:
            pass
        display()

    submit_button = Button(name_thing, text='Submit', border=5, width=15, command=calc)
    submit_button.place(relx=0.5, rely=0.82, anchor=CENTER)

    next_question_button = Button(name_thing, text='Next', command=display)
    next_question_button.place(relx=0.87, rely=0.82, anchor=CENTER)

    y = countDown()
    if y == -1:
        display()
        name_thing.mainloop()


# -------------------------------------------- Dictionary -------------------------------------------------
def dictionary():
    global Dictionary
    dictionary = PyDictionary
    Dictionary = Tk()

    # The size of the window
    Dictionary.geometry('800x600+255+80')
    Dictionary.resizable(width=False, height=False)
    Dictionary.title('Quiz Game')
    Dictionary.iconbitmap('icon.ICO')

    # Canvas
    canvas = Canvas(Dictionary, width=800, height=740, bg='SkyBlue2')
    canvas.pack()
    frame1 = Frame(Dictionary, bg='white')
    frame1.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

    def dict():
        meaning.config(text=dictionary.meaning(word.get())['Noun'][0])
        synonym.config(text=dictionary.meaning(word.get()))
        antonym.config(text=dictionary.meaning(word.get()))

    def back():
        Dictionary.destroy()
        main_menu()

    # Labels, Button and Frames
    label_heading = Label(frame1, text='Dictionary', font=('Calibri', 40), bg='white')
    label_heading.place(relx=0.5, rely=0.1, anchor=CENTER)

    label_type_word = Label(frame1, text='Type Word', font=('Calibri', 15), fg='black', bg='white')
    label_type_word.place(relx=0.21, rely=0.3)

    word = Entry(frame1, bg='#d3d3d3', fg='black')
    word.config(width=22)
    word.place(relx=0.37, rely=0.31)

    # Frame 2
    frame2 = Frame(frame1)
    label_meaning = Label(frame1, text='Meaning:', font='Calibri 15', fg='black', bg='white')
    label_meaning.place(relx=0.21, rely=0.5)
    meaning = Label(frame1, text='', font='Courier 12', fg='black', bg='white')
    meaning.place(relx=0.37, rely=0.51)
    frame2.place(relx=0.37, rely=0.51)

    # Frame 3
    frame3 = Frame(frame1)
    label_synonym = Label(frame1, text='Synonym:', font='Calibri 15', fg='black', bg='white')
    label_synonym.place(relx=0.21, rely=0.6)
    synonym = Label(frame1, text='', font='Courier 12', fg='black', bg='white')
    synonym.place(relx=0.37, rely=0.61)
    frame3.place(relx=0.37, rely=0.61)

    # Frame 4
    frame4 = Frame(frame1)
    label_antonym = Label(frame1, text='Antonym:', font='Calibri 15', fg='black', bg='white')
    label_antonym.place(relx=0.21, rely=0.7)
    antonym = Label(frame1, text='', font='Courier 12', fg='black', bg='white')
    antonym.place(relx=0.37, rely=0.71)
    frame4.place(relx=0.37, rely=0.71)

    find_button = Button(frame1, text='Search', command=dict)
    find_button.place(relx=0.45, rely=0.4)

    back_button = Button(frame1, text='Home', command=back)
    back_button.config(activebackground='SkyBlue2')
    back_button.place(relx=0.75, rely=0.8)

    Dictionary.mainloop()


# -------------------------------------------- Translate -------------------------------------------------
def transla():
    global trans
    trans = Tk()

    # The size of the window
    trans.geometry('800x600+255+80')
    trans.resizable(width=False, height=False)
    trans.title('Quiz Game')
    trans.iconbitmap('icon.ICO')

    # Canvas
    canvas = Canvas(trans, width=800, height=740, bg='SkyBlue2')
    canvas.pack()
    frame1 = Frame(trans, bg='white')
    frame1.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

    # Labels, Button and Frames
    label_title = Label(frame1, text='Language Translator', font=('Calibri', 40), bg='white')
    label_title.place(relx=0.5, rely=0.1, anchor=CENTER)

    label_enter = Label(frame1, text='Enter Text', font='Calibri 15 bold', bg='white')
    label_enter.place(relx=0.01, rely=0.2)

    input_text = Text(frame1, font='Calibri 12', height=5, wrap=WORD, padx=5, pady=5, width=29)
    input_text.place(relx=0.01, rely=0.26)

    label_output = Label(frame1, text='Output', font='Calibri 15 bold', bg='white')
    label_output.place(relx=0.63, rely=0.2)

    output_text = Text(frame1, font='Calibri 12', height=5, wrap=WORD, padx=5, pady=5, width=26)
    output_text.place(relx=0.63, rely=0.26)

    language = list(LANGUAGES.values())
    src_lang = tkinter.ttk.Combobox(frame1, values=language, width=21)
    src_lang.place(relx=0.16, rely=0.21)
    src_lang.set('Choose input language')

    out_lang = tkinter.ttk.Combobox(frame1, values=language, width=21)
    out_lang.place(relx=0.74, rely=0.21)
    out_lang.set('Choose output language')

    def Translate():
        translator = Translator()
        translated = translator.translate(text=input_text.get(1.0, END), src=src_lang.get(), out=out_lang.get())
        output_text.delete(1.0, END)
        output_text.insert(END, translated.text)

    def back():
        trans.destroy()
        main_menu()

    trans_button = Button(frame1, text='Translate', font='arial 12 bold', pady=5, command=Translate, bg='SkyBlue2')
    trans_button.config(activebackground='royal blue1')
    trans_button.place(relx=0.5, rely=0.65, anchor=CENTER)

    back_button = Button(frame1, text='Home', command=back)
    back_button.config(activebackground='SkyBlue2')
    back_button.place(relx=0.9, rely=0.65)

    trans.mainloop()


# -------------------------------------------- The main menu -------------------------------------------------

def main_menu():
    global choice_menu
    choice_menu = Tk()

    # The size of the window
    choice_menu.geometry('800x600+255+80')
    choice_menu.resizable(width=False, height=False)
    choice_menu.title('Quiz Game')
    choice_menu.iconbitmap('icon.ICO')

    # Canvas
    canvas = Canvas(choice_menu, width=800, height=740, bg='SkyBlue2')
    canvas.pack()
    frame1 = Frame(choice_menu, bg='white')
    frame1.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

    global var_nbr
    var_nbr = IntVar()
    # ----- The Buttons and Labels
    welcome_label = Label(choice_menu, text='MENU', font=('Broadway', 31), fg='white', bg='SkyBlue2')
    welcome_label.place(relx=0.425, rely=0.01)

    select_label = Label(choice_menu, text='Select your choice', fg='black', bg='white')
    select_label.config(font=('Broadway', 31))
    select_label.place(relx=0.3, rely=0.2)

    quiz_button = Radiobutton(frame1, text='What is the strength\n of your Python knowledge?', bg="white",
                              font="calibri 16", value=1, variable=var_nbr)
    quiz_button.place(relx=0.35, rely=0.25)

    vocabulary_button = Radiobutton(frame1, text='How strong\n is your vocabulary?', bg="white", font="calibri 16",
                                    value=2, variable=var_nbr)
    vocabulary_button.place(relx=0.35, rely=0.4)

    true_false_button = Radiobutton(frame1, text='True or False', bg="white", font="calibri 16", value=3,
                                    variable=var_nbr)
    true_false_button.place(relx=0.35, rely=0.55)

    name_thing_button = Radiobutton(frame1, text='Name that thing', bg="white", font="calibri 16", value=4,
                                    variable=var_nbr)
    name_thing_button.place(relx=0.35, rely=0.65)

    dictionary_button = Radiobutton(frame1, text='Dictionary', bg="white", font="calibri 16", value=5, variable=var_nbr)
    dictionary_button.place(relx=0.35, rely=0.75)

    translation_button = Radiobutton(frame1, text='Translation', bg="white", font="calibri 16", value=6,
                                     variable=var_nbr)
    translation_button.place(relx=0.35, rely=0.85)

    def navigate():
        x = var_nbr.get()
        print(x)
        if x == 1:
            choice_menu.destroy()
            menu()
        elif x == 2:
            choice_menu.destroy()
            vocabulary()
        elif x == 3:
            choice_menu.destroy()
            true_or_false()
        elif x == 4:
            choice_menu.destroy()
            name_thing()
        elif x == 5:
            choice_menu.destroy()
            dictionary()
        elif x == 6:
            choice_menu.destroy()
            transla()
        else:
            pass

    letsgo = Button(frame1, text="Let's Go", bg="white", font="calibri 12", activebackground='SkyBlue2',
                    command=navigate)
    letsgo.place(relx=0.8, rely=0.85)
    choice_menu.mainloop()

    choice_menu.mainloop()


# -------------------------------------------- The menu to choice level -----------------------------------------
def menu():
    global menu
    menu = Tk()

    # The size of the window
    menu.geometry('800x600+255+80')
    menu.resizable(width=False, height=False)
    menu.title('Quiz Game')
    menu.iconbitmap('icon.ICO')

    # Canvas
    canvas = Canvas(menu, width=800, height=740, bg='SkyBlue2')
    canvas.pack()
    frame1 = Frame(menu, bg='white')
    frame1.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

    # ------The Labels and The RadioButton
    welcome_label = Label(menu, text='WELCOME TO QUIZ STATION', font=('Broadway', 31), fg='white', bg='SkyBlue2')
    welcome_label.place(relx=0.12, rely=0.01)

    level_difficult_label = Label(menu, text='Select your Difficulty Level !!', fg='black', bg='white')
    level_difficult_label.config(font=('Calibri', 22))
    level_difficult_label.place(relx=0.27, rely=0.3)

    global var_nbr1
    var_nbr1 = IntVar()
    easy_radio = Radiobutton(menu, text='Easy', bg="white", font="calibri 16", value=1, variable=var_nbr1)
    easy_radio.place(relx=0.28, rely=0.4)

    medium_radio = Radiobutton(menu, text='Medium', bg="white", font="calibri 16", value=2, variable=var_nbr1)
    medium_radio.place(relx=0.28, rely=0.5)

    hard_radio = Radiobutton(menu, text='Hard', bg="white", font="calibri 16", value=3, variable=var_nbr1)
    hard_radio.place(relx=0.28, rely=0.6)

    def navigate():

        x = var_nbr1.get()
        print(x)
        if x == 1:
            menu.destroy()
            easy()
        elif x == 2:
            menu.destroy()
            medium()

        elif x == 3:
            menu.destroy()
            hard()
        else:
            pass

    letsgo = Button(frame1, text="Let's Go", bg="white", font="calibri 12", command=navigate)
    letsgo.place(relx=0.25, rely=0.8)
    menu.mainloop()


# -------------------------------------------- Easy level -------------------------------------------------
def easy():
    global easy
    easy = Tk()

    # The size of the window
    easy.geometry('800x600+255+80')
    easy.resizable(width=False, height=False)
    easy.title('Quiz Game')
    easy.iconbitmap('icon.ICO')

    # Canvas and Frames
    canvas = Canvas(easy, width=800, height=740, bg='SkyBlue2')
    canvas.pack()
    frame1 = Frame(easy, bg='white')
    frame1.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

    def countDown():
        check = 0
        for k in range(15, 0, -1):

            if k == 1:
                check = -1
            timer.configure(text=k)
            frame1.update()
            time.sleep(1)

        timer.configure(text="Times up!")
        if check == -1:
            return -1
        else:
            return 0

    global score
    score = 0

    # ------- The algorithm
    easyQes = [
        [
            "What will be the output of the following Python code? \nl=[1, 0, 2, 0, 'hello', '', []] "
            "\nlist(filter(bool, nl))",
            "[1, 0, 2, ‘hello’, '', []]",
            "Error",
            "[1, 2, ‘hello’]",
            "[1, 0, 2, 0, ‘hello’, '', []]"
        ],
        [
            "What will be the output of the following Python expression if the value of x is 34? \nprint(“%f”%x)",
            "34.00",
            "34.000000",
            "34.0000",
            "34.00000000"

        ],
        [
            "What will be the value of X in the following Python expression? \nX = 2+9*((3*12)-8)/10",
            "30.8",
            "27.2",
            "28.4",
            "30.0"
        ],
        [
            "Which of these in not a core data type?",
            "Tuples",
            "Dictionary",
            "Lists",
            "Class"
        ],
        [
            "Which of the following represents the bitwise XOR operator?",
            "&",
            "!",
            "^",
            "|"
        ]
    ]
    answer = [
        "[1, 2, ‘hello’]",
        "34.000000",
        "27.2",
        "Class",
        "^"]

    li = ['', 0, 1, 2, 3, 4]
    x = random.choice(li[1:])

    # ------ The Label and The RadioButtons
    question = Label(frame1, text=easyQes[x][0], font="calibri 14", bg="white")
    question.place(relx=0.5, rely=0.2, anchor=CENTER)

    var = StringVar()

    answer_a = Radiobutton(frame1, text=easyQes[x][1], font="calibri 10", value=easyQes[x][1], variable=var, bg="white")
    answer_a.place(relx=0.5, rely=0.42, anchor=CENTER)

    answer_b = Radiobutton(frame1, text=easyQes[x][2], font="calibri 10", value=easyQes[x][2], variable=var, bg="white")
    answer_b.place(relx=0.5, rely=0.52, anchor=CENTER)

    answer_c = Radiobutton(frame1, text=easyQes[x][3], font="calibri 10", value=easyQes[x][3], variable=var, bg="white")
    answer_c.place(relx=0.5, rely=0.62, anchor=CENTER)

    answer_d = Radiobutton(frame1, text=easyQes[x][4], font="calibri 10", value=easyQes[x][4], variable=var, bg="white")
    answer_d.place(relx=0.5, rely=0.72, anchor=CENTER)

    li.remove(x)

    timer = Label(easy)
    timer.place(relx=0.8, rely=0.82, anchor=CENTER)

    def display():
        if len(li) == 1:
            easy.destroy()
            showMark(score)
        if len(li) == 2:
            next_question_button.configure(text='End', command=calc)

        if li:
            x = random.choice(li[1:])
            question.configure(text=easyQes[x][0])

            answer_a.configure(text=easyQes[x][1], value=easyQes[x][1])

            answer_b.configure(text=easyQes[x][2], value=easyQes[x][2])

            answer_c.configure(text=easyQes[x][3], value=easyQes[x][3])

            answer_d.configure(text=easyQes[x][4], value=easyQes[x][4])

            li.remove(x)
            print(li)
            y = countDown()
            if y == -1:
                display()

    # Calculate the score
    def calc():
        global score
        if var.get() in answer:
            score += 1
        else:
            pass
        display()

    # The Buttons
    submit_button = Button(frame1, text='Submit', command=calc)
    submit_button.place(relx=0.5, rely=0.82, anchor=CENTER)

    next_question_button = Button(frame1, text='Next', command=display)
    next_question_button.place(relx=0.87, rely=0.82, anchor=CENTER)

    y = countDown()
    if y == -1:
        display()
        easy.mainloop()


# -------------------------------------------- Medium level -------------------------------------------------
def medium():
    global medium
    medium = Tk()

    # The size of the window
    medium.geometry('800x600+255+80')
    medium.resizable(width=False, height=False)
    medium.title('Quiz Game')
    medium.iconbitmap('icon.ICO')

    # Canvas and Frames
    canvas = Canvas(medium, width=800, height=740, bg='SkyBlue2')
    canvas.pack()
    frame1 = Frame(medium, bg='white')
    frame1.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

    def countDown():
        check = 0
        for k in range(15, 0, -1):

            if k == 1:
                check = -1
            timer.configure(text=k)
            frame1.update()
            time.sleep(1)

        timer.configure(text="Times up!")
        if check == -1:
            return (-1)
        else:
            return 0

    global score
    score = 0

    # ------- The algorithm
    mediumQ = [
        [
            "Which of the following is not an exception handling keyword in Python?",
            "accept",
            "finally",
            "except",
            "try"
        ],
        [
            "Suppose list1 is [3, 5, 25, 1, 3], what is min(list1)?",
            "3",
            "5",
            "25",
            "1"
        ],
        [
            "Suppose list1 is [2, 33, 222, 14, 25], What is list1[-1]?",
            "Error",
            "None",
            "25",
            "2"
        ],
        [
            "print(0xA + 0xB + 0xC):",
            "0xA0xB0xC",
            "Error",
            "0x22",
            "33"
        ],
        [
            "Which of the following is invalid?",
            "_a = 1",
            "__a = 1",
            "__str__ = 1",
            "none of the mentioned"
        ],
    ]
    answer = [
        "accept",
        "1",
        "25",
        "33",
        "none of the mentioned"
    ]

    li = ['', 0, 1, 2, 3, 4]
    x = random.choice(li[1:])

    # ------ The Label and The RadioButtons
    question = Label(frame1, text=mediumQ[x][0], font="calibri 14", bg="white")
    question.place(relx=0.5, rely=0.2, anchor=CENTER)

    var = StringVar()

    answer_a = Radiobutton(frame1, text=mediumQ[x][1], font="calibri 10", value=mediumQ[x][1], variable=var, bg="white")
    answer_a.place(relx=0.5, rely=0.42, anchor=CENTER)

    answer_b = Radiobutton(frame1, text=mediumQ[x][2], font="calibri 10", value=mediumQ[x][2], variable=var, bg="white")
    answer_b.place(relx=0.5, rely=0.52, anchor=CENTER)

    answer_c = Radiobutton(frame1, text=mediumQ[x][3], font="calibri 10", value=mediumQ[x][3], variable=var, bg="white")
    answer_c.place(relx=0.5, rely=0.62, anchor=CENTER)

    answer_d = Radiobutton(frame1, text=mediumQ[x][4], font="calibri 10", value=mediumQ[x][4], variable=var, bg="white")
    answer_d.place(relx=0.5, rely=0.72, anchor=CENTER)

    li.remove(x)

    timer = Label(medium)
    timer.place(relx=0.8, rely=0.82, anchor=CENTER)

    def display():
        if len(li) == 1:
            medium.destroy()
            showMark(score)
        if len(li) == 2:
            next_question_button.configure(text='End', command=calc)

        if li:
            x = random.choice(li[1:])
            question.configure(text=mediumQ[x][0])

            answer_a.configure(text=mediumQ[x][1], value=mediumQ[x][1])

            answer_b.configure(text=mediumQ[x][2], value=mediumQ[x][2])

            answer_c.configure(text=mediumQ[x][3], value=mediumQ[x][3])

            answer_d.configure(text=mediumQ[x][4], value=mediumQ[x][4])

            li.remove(x)
            print(li)
            y = countDown()
            if y == -1:
                display()

    # Calculate the score
    def calc():
        global score
        if var.get() in answer:
            score += 1
        else:
            pass
        display()

    # The Buttons
    submit_button = Button(frame1, text='Submit', command=calc)
    submit_button.place(relx=0.5, rely=0.82, anchor=CENTER)

    next_question_button = Button(frame1, text='Next', command=display)
    next_question_button.place(relx=0.87, rely=0.82, anchor=CENTER)

    y = countDown()
    if y == -1:
        display()
        medium.mainloop()


# -------------------------------------------- Hard Level -------------------------------------------------
def hard():
    global hard
    hard = Tk()

    # The size of the window
    hard.geometry('800x600+255+80')
    hard.resizable(width=False, height=False)
    hard.title('Quiz Game')
    hard.iconbitmap('icon.ICO')

    # Canvas and Frames
    canvas = Canvas(hard, width=800, height=740, bg='SkyBlue2')
    canvas.pack()
    frame1 = Frame(hard, bg='white')
    frame1.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

    def countDown():
        check = 0
        for k in range(15, 0, -1):

            if k == 1:
                check = -1
            timer.configure(text=k)
            frame1.update()
            time.sleep(1)

        timer.configure(text="Times up!")
        if check == -1:
            return (-1)
        else:
            return 0

    global score
    score = 0

    # ------- The algorithm
    hardQ = [
        [
            "All keywords in Python are in _________",
            "lower case",
            "UPPER CASE",
            "Capitalized",
            "None of the mentioned"
        ],
        [
            "Which of the following cannot be a variable?",
            "__init__",
            "in",
            "it",
            "on"
        ],
        [
            "Which of the following is a Python tuple?",
            "[1, 2, 3]",
            "(1, 2, 3)",
            "{1, 2, 3}",
            "{}"
        ],
        [
            "What is returned by math.ceil(3.4)?",
            "3",
            "4",
            "4.0",
            "3.0"
        ],
        [
            "What will be the output of print(math.factorial(4.5))?",
            "24",
            "120",
            "error",
            "24.0"
        ]

    ]
    answer = [
        "None of the mentioned",
        "in",
        "(1,2,3)",
        "4",
        "error"
    ]

    li = ['', 0, 1, 2, 3, 4]
    x = random.choice(li[1:])

    # ------ The Label and The RadioButtons
    question = Label(frame1, text=hardQ[x][0], font="calibri 14", bg="white")
    question.place(relx=0.5, rely=0.2, anchor=CENTER)

    var = StringVar()

    answer_a = Radiobutton(frame1, text=hardQ[x][1], font="calibri 10", value=hardQ[x][1], variable=var, bg="white")
    answer_a.place(relx=0.5, rely=0.42, anchor=CENTER)

    answer_b = Radiobutton(frame1, text=hardQ[x][2], font="calibri 10", value=hardQ[x][2], variable=var, bg="white")
    answer_b.place(relx=0.5, rely=0.52, anchor=CENTER)

    answer_c = Radiobutton(frame1, text=hardQ[x][3], font="calibri 10", value=hardQ[x][3], variable=var, bg="white")
    answer_c.place(relx=0.5, rely=0.62, anchor=CENTER)

    answer_d = Radiobutton(frame1, text=hardQ[x][4], font="calibri 10", value=hardQ[x][4], variable=var, bg="white")
    answer_d.place(relx=0.5, rely=0.72, anchor=CENTER)

    li.remove(x)

    timer = Label(hard)
    timer.place(relx=0.8, rely=0.82, anchor=CENTER)

    def display():
        if len(li) == 1:
            hard.destroy()
            showMark(score)
        if len(li) == 2:
            next_question_button.configure(text='End', command=calc)

        if li:
            x = random.choice(li[1:])
            question.configure(text=hardQ[x][0])

            answer_a.configure(text=hardQ[x][1], value=hardQ[x][1])

            answer_b.configure(text=hardQ[x][2], value=hardQ[x][2])

            answer_c.configure(text=hardQ[x][3], value=hardQ[x][3])

            answer_d.configure(text=hardQ[x][4], value=hardQ[x][4])

            li.remove(x)
            print(li)
            y = countDown()
            if y == -1:
                display()

    # Calculate the score
    def calc():
        global score
        if var.get() in answer:
            score += 1
        else:
            pass
        display()

    # The Buttons
    submit_button = Button(frame1, text='Submit', command=calc)
    submit_button.place(relx=0.5, rely=0.82, anchor=CENTER)

    next_question_button = Button(frame1, text='Next', command=display)
    next_question_button.place(relx=0.87, rely=0.82, anchor=CENTER)

    y = countDown()
    if y == -1:
        display()
        hard.mainloop()


# -------------------------------------------- Show Score -------------------------------------------------
# Show the score
def showMark(mark):
    global showMark
    showMark = Tk()

    # The size of the window
    showMark.geometry('800x600+255+80')
    showMark.resizable(width=False, height=False)
    showMark.title('Quiz Game')
    showMark.iconbitmap('icon.ICO')

    # Canvas
    canvas = Canvas(showMark, width=800, height=740, bg='SkyBlue2')
    canvas.pack()
    frame1 = Frame(showMark, bg='white')
    frame1.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

    st = "Your score is " + str(mark) + "/5"
    mark_label = Label(frame1, text=st, fg="black", font='Courier 18')
    mark_label.place(relx=0.5, rely=0.2, anchor=CENTER)

    def back():
        showMark.destroy()
        main_menu()

    def replay():
        y = var_nbr.get()
        if y == 1:
            menu()
        elif y == 2:
            showMark.destroy()
            vocabulary()
        elif y == 3:
            showMark.destroy()
            true_or_false()
        elif y == 4:
            showMark.destroy()
            name_thing()
        elif y == 5:
            showMark.destroy()
            dictionary()
        elif y == 6:
            showMark.destroy()
            transla()
        else:
            pass

    replay_button = Button(frame1, text='Replay', command=replay)
    replay_button.config(activebackground='SkyBlue2')
    replay_button.place(relx=0.45, rely=0.3)

    back_button = Button(frame1, text='Home', command=back)
    back_button.config(activebackground='SkyBlue2')
    back_button.place(relx=0.75, rely=0.8)

    showMark.mainloop()


# -------------------------------------------- Home -------------------------------------------------
# The main of the game
def home():
    global root
    root = Tk()

    # The size of the window
    root.geometry('800x600+255+80')
    root.resizable(width=False, height=False)
    root.title('Quiz Game')
    root.iconbitmap('icon1.ICO')

    # Canvas and image ( Putt the image on the canvas)
    canvas = Canvas(root, width=800, height=540, bg='yellow')
    canvas.pack()
    img = PhotoImage(file='output-onlinepngtools.png')
    canvas.create_image(400, 270, image=img)

    # Button to start
    button_start = Button(root, text='Start', font=('Courier', 14), bg='goldenrod3', border=10, command=signUpPage)
    button_start.config(activebackground="Gold2", relief=RAISED)
    button_start.pack(side='bottom', fill=X, ipady=5)

    root.mainloop()


if __name__ == '__main__':
    home()
