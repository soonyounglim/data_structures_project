#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3
from twitter import *
from tkinter import *

def showTweets(x, num):
    display a number of new tweets and usernames for i in range(0, num):
    line1 = (x[i]['user']['screen_name'])
    line2 = (x[i]['text'])
    w = Label(master, text=line1 + "\n" + line2 + "\n\n")
    w.pack()

def getTweets():
    x = t.statuses.home_timeline(screen_name="dataStruct2k17")
    return x


def tweet():
    global entryWidget
    if entryWidget.get().strip() == "":
        print("Empty")
    else:
        t.statuses.update(status=entryWidget.get().strip())
        entryWidget.delete(0,END)
        print("working")


token = '846863644348567552-CsyrdvBEgpqrm0XeiR2Mj5oIRTGVC77'
token_key = '9L3mct66ihQ7xpPQXiBpzMpqYDCtCJ6vE5Maeg8sqDC0L'
con_secret = 'oT18JchX8UJojsiTTE4CaosCL'
con_secret_key = '0YBtm9CYoxDuav3zWcTi0qVrx0DmNWEJy733UeDneN4BuyewkP'

# Put in token, token_key, con_secret, con_secret_key
t = Twitter( auth=OAuth('', '', '', ''))

numberOfTweets = 10



master = Tk()                                                       # Makes a window
showTweets(getTweets(), numberOfTweets)

# Window stuff
master.title("Tkinter Entry Widget")
master["padx"] = 40
master["pady"] = 20

# Create a text frame to hold the text Label and the Entry widget
textFrame = Frame(master)
# Create a Label in textFrame
entryLabel = Label(textFrame)
entryLabel["text"] = "Make a new Tweet:"
entryLabel.pack(side=LEFT)
# Create an Entry Widget in textFrame
entryWidget = Entry(textFrame)
entryWidget["width"] = 50
entryWidget.pack(side=LEFT)
textFrame.pack()

button = Button(master, text="Submit", command=tweet)
button.pack()

master.mainloop()
