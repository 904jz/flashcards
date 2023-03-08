from tkinter import *
import pandas
import random


BACKGROUND_COLOR = "#B1DDC6"
words = []
def load_cards(lang):
    card_set = lang
    global words

    # Use panda to create dataframe
    try:
        df = pandas.read_csv(f'data/{card_set}_words_to_learn.csv')
    except FileNotFoundError:
        df = pandas.read_csv(f'data/{card_set}_words.csv')
    
    words = df.to_dict(orient='records')
    new_card()

# create dictionary from dataframe


x = {}

#create a function that chooses a random word to populate the flashcard
def flipcard():
    
    canvas.itemconfig(card,image=card_back)
    canvas.itemconfig(card_title,text='English',fill='white')
    try:
        canvas.itemconfig(card_word,text=x['English'],fill='white')
    except KeyError:
        print('Language not chosen')


def new_card():
    lang = language.get().title()
    global x, flip_timer
    window.after_cancel(flip_timer)
    x = random.choice(words)
    canvas.itemconfig(card,image=card_front)
    canvas.itemconfig(card_title,text=f'{lang}',fill='black')
    canvas.itemconfig(card_word,text=x[f'{lang}'],fill='black')
    
    flip_timer = window.after(3000,flipcard)
    

    


def gotit():
    words.remove(x)
    out = pandas.DataFrame(words)
    out.to_csv(f'data/{language.get()}_words_to_learn.csv',index=False)
    new_card()
    
    

window = Tk()
window.title('Flashcards')
window.configure(bg=BACKGROUND_COLOR,padx=50,pady=50)
languages = ['arabic', 'french', 'german','japanese','russian','spanish']

language = StringVar(window)
language.set('Select A Language')
language_choice = OptionMenu(window,language,*languages,command=load_cards)
language_choice.grid(row=0,column=0,columnspan=2, sticky=EW)

wrong = PhotoImage(file='images/wrong.png')
right = PhotoImage(file='images/right.png')
flip_timer = 'nothing'
canvas = Canvas(master=window, height=526,width=800, bg=BACKGROUND_COLOR,highlightthickness=0)
card_front = PhotoImage(file='images/card_front.png')
card_back = PhotoImage(file='images/card_back.png')
card = canvas.create_image(400,265,image=card_front)
card_title = canvas.create_text((400,150),text='',font=('Arial',40,'italic'))
card_word = canvas.create_text((400,263),text='',font=('Arial',60,'bold'))

canvas.grid(row=1,column=0, columnspan=2)


wrong_button = Button(image=wrong, highlightthickness=0,command=new_card)
wrong_button.grid(row=2,column=0)
right_button = Button(image=right, highlightthickness=0,command=gotit)
right_button.grid(row=2,column=1)



window.mainloop()
