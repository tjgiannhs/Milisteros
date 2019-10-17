"""from tkinter import *
import tkinter.messagebox
from chatterbot.conversation import Statement
from GreekBot.greekbot import GreekBot
from GreekBot.greek_sql_storage import GreekSQLStorageAdapter
from GreekBot.greek_trainers import GreekChatterBotCorpusTrainer

#the order of the preprocessors is important, each one affects the result of the previous one
chatbot = GreekBot("Μιληστερός", preprocessors=['GreekBot.greek_preprocessors.clean_apostrophes','GreekBot.greek_preprocessors.capitalize','GreekBot.greek_preprocessors.seperate_sentences','chatterbot.preprocessors.clean_whitespace'])

#the number of saved statements in the database
ari8mosKataxwrhsewn = chatbot.storage.count()

#if the database is empty we save the default reply first and then we train the bot using our training corpora
if(ari8mosKataxwrhsewn<1):
    chatbot.neaKataxwrhsh(GreekSQLStorageAdapter.defaultReply,"",0)
    # First, lets train our bot with some data
    trainer = GreekChatterBotCorpusTrainer(chatbot)
    print("Bot's first training!")
    #the second file is the same but without stress on the letters
    trainer.train('GreekBot.postgraduate','GreekBot.postgraduate2')

    #in the database we change the weight of all those statements to 2(the maximum)
    for i in range(2,chatbot.storage.count()+1):
        chatbot.storage.updateWeightFromId(i,1)

#the bot has a default welcoming sentence and a sentence that it uses after failing to find a response to the user's input for three times in a row
defaultWelcome = "Γεια σας. Είμαι ο Μιληστερός. Ρωτήστε με ό,τι θέλετε να μάθετε για το μεταπτυχιακό."
defaultReplyAfter3 = "Μάλλον δεν ξέρω την απάντηση. Δοκιμάστε να ψάξετε στο dmci.csd.auth.gr"
defaultRepliesInARow = 0
ratedConv = True; #if the user has rated the conversation up to the last response
protaseis = []
barh = []

#changes the state variables to their default values
def resetConv():
    global protaseis
    protaseis = []
    global barh
    barh = []
    global defaultRepliesInARow
    defaultRepliesInARow = 0

#calculates the weights of each sentence in the conversation before saving them to the database
def calcWeights(s):
    global barh
    barh=[]
    ola = len(protaseis)
    for i in range(0,ola):
        barh.append(s*round((i+1)/ola/2,2))#values from 0 to 0.5
        print(protaseis[i]+", "+str(barh[i]))


#saves the sentences or in the case they already exist in the database it updates their weights
def apo8hkeuse():


    if not (chatbot.storage.isAlreadyStored(protaseis[0],defaultWelcome)):
        chatbot.neaKataxwrhsh(protaseis[0],defaultWelcome,barh[0])
    else:
        chatbot.storage.updateWeight(protaseis[0],defaultWelcome,barh[0])

    for i in range(1,len(protaseis)):
        #den apo8hkeuoume tis protaseis oi opoies mphkan sth 8esh twn default apanthsewn
        if not protaseis[i] == defaultWelcome:

            if not (chatbot.storage.isAlreadyStored(protaseis[i], protaseis[i-1])):
                chatbot.neaKataxwrhsh(protaseis[i],protaseis[i-1],barh[i])
            else:
                chatbot.storage.updateWeight(protaseis[i],protaseis[i-1],barh[i])

#Functions for the green and red buttons
def ektypwths():

    #can't be used twice in a row
    if ratedConv:
        return

    setFlagTrue()
    print("Πράσινο")
    if(len(protaseis)>=1):
        calcWeights(1)
        apo8hkeuse()

def ektypwths2():

    #can't be used twice in a row
    if ratedConv:
        return

    setFlagTrue()
    print("Κόκκινο")
    if(len(protaseis)>=1):
        calcWeights(-1)
        apo8hkeuse()

#Using Tkinter to create the window
#The window has an icon and a fixed resolution that can't be changed by the user
window = Tk()
window.title("Μιληστερός")
window.geometry("880x300")
window.iconbitmap("Images/Icon.ico")
window.resizable(False,False);

#the images for the buttons
goodImage = PhotoImage(file = "Images/greenImage.png")
badImage = PhotoImage(file = "Images/redImage.png")
restartImage = PhotoImage(file = "Images/restartImage.png")


#Gets a reply to the user's input, checks for default replies in a row
#Adds the reply to the conversation sentences list if it's not the default reply
def getAnswer(protash):
    apanthsh = chatbot.get_response(protash)
    #apanthsh = str(apanthsh).replace("'","")
    global defaultRepliesInARow
    #print("defaultRepliesInARow ",defaultRepliesInARow)

    if apanthsh==chatbot.storage.defaultReply:
        defaultRepliesInARow = defaultRepliesInARow + 1
        if defaultRepliesInARow >= 3:
            putInBox(defaultReplyAfter3)
        else:
            putInBox(apanthsh)
    else:
        defaultRepliesInARow = 0
        putInBox(apanthsh)
    if apanthsh!=chatbot.storage.defaultReply:
        protaseis.append(apanthsh)
    else:
        protaseis.append(defaultWelcome)
    #print("defaultRepliesInARow ",defaultRepliesInARow)

#Gets text input from the user and clears the entry
#The text can't be nothing or only spaces
#Shows the text in the box
def printUserText():
    eisodos = entry.get()
    eisodos = chatbot.process_input(Statement(eisodos))

    protaseis.append(eisodos)
    setFlagFalse();
    entry.delete(0,"end")
    if(eisodos.isspace() or not eisodos):
        return
    #print (eisodos)
    #setLabelText(eisodos)
    putInBox(eisodos)
    getAnswer(eisodos)

#changes myLabel's text
def setLabelText(keimeno):
    myLabel.configure(text=keimeno)

#Clears the conversation box
def clearBox():

    if(not ratedConv):
        showPopUp()
    else:
        myBox.delete(0,"end")
        putInBox(defaultWelcome)
        resetConv()
        #protaseis.append(defaultWelcome)

#Puts the text in the conversation box and centers it on the last sentence
def putInBox(keimeno):
    myBox.insert("end",keimeno)
    myBox.see("end")

#On Return/Enter key press released
def keyup(e):
    if (e.char=='\r'):
        printUserText()

#Shows a pop up message that asks from the user to evaluate the conversation
def showPopUp():
    tkinter.messagebox.showinfo("Ουπς", "Παρακαλώ αξιολογήστε τη συνομιλία πριν διαγραφεί")

def setFlagTrue():
    global ratedConv
    ratedConv = True

def setFlagFalse():
    global ratedConv
    ratedConv = False

#We show a pop up to the user if they haven't rated the conversation but try to exit it
def beforeExit():
    if(not ratedConv):
        showPopUp()
    else:
        window.destroy()

#myLabel has text with instructions fot the user
odhgies = "Οδηγίες: Γράψτε στο κουτί και πατήστε το κουμπί αποστολής ή το Έντερ για συνομιλία με τον Μιληστερό." \
          "\nΜην ξεχάσετε να κάνετε αξιολόγηση πατώντας το πράσινο ή το κόκκινο κουμπί μετά τη συνομιλία." \
          "\nΜε το κίτρινο κουμπί μπορείτε να ξαναξεκινήσετε τη συνομιλία από την αρχή."
myLabel = Label(window,text = odhgies,bg="yellow",fg="black")
myLabel.pack()

#We create a frame for the window, we will put the rest of the elements there
myFrame = Frame(window)

#Scrollbar at the right to view the whole conversation
scrollY = Scrollbar(myFrame)
scrollY.pack(side=RIGHT, fill=Y)

#Scrollbar at the bottom to view the whole sentence
scrollΧ = Scrollbar(myFrame,orient=HORIZONTAL)
scrollΧ.pack(side=BOTTOM, fill=X)

#List of the conversation's sentences connected to the scrollbars
myBox = Listbox(myFrame, yscrollcommand = scrollY.set, xscrollcommand = scrollΧ.set, width = 140)
myBox.pack(side=LEFT)
scrollY.config(command = myBox.yview)
scrollΧ.config(command = myBox.xview)

#We add the frame to the window, set to cover all of its width
myFrame.pack(fill=X)

#We create a frame for the user's tools
frameBottom = Frame(window)

#keyup runs for every keyboard button release
window.bind("<KeyRelease>", keyup)

#Bar for the user to give input
entry = Entry(frameBottom, width = 100)
entry.grid(row=0,column=0, sticky=E)

#Three similar buttons with the images from above next to the input bar
#Each one of them has a different use with a different function
#We add them to the frame
buttonEnter = Button(frameBottom,command=printUserText,text="Αποστολή")
buttonEnter.grid(row=0,column=1,sticky=E)

buttonGreen = Button(frameBottom,command = ektypwths, image=goodImage)
buttonGreen.grid(row=0,column=2,sticky=E)

buttonRed = Button(frameBottom,command = ektypwths2, image=badImage)
buttonRed.grid(row=0,column=3,sticky=E)

buttonRestart = Button(frameBottom,bg="yellow",command = clearBox, image=restartImage)
buttonRestart.grid(row=0,column=4,sticky=E)

#We add the frame to the window
frameBottom.pack()

#We add the default welcome sentence to the conversation box
putInBox(defaultWelcome)
#protaseis.append(defaultWelcome)

window.protocol("WM_DELETE_WINDOW", beforeExit)

#The window will keep reloading
window.mainloop()"""

from tkinter import *
import tkinter.messagebox

from chatterbot.conversation import Statement
from flask_cors import CORS

from GreekBot.greekbot import GreekBot
from GreekBot.greek_sql_storage import GreekSQLStorageAdapter
from GreekBot.greek_trainers import GreekChatterBotCorpusTrainer


#the order of the preprocessors matters
chatbot = GreekBot("Μιληστερός", preprocessors=['GreekBot.greek_preprocessors.clean_apostrophes','GreekBot.greek_preprocessors.capitalize','GreekBot.greek_preprocessors.seperate_sentences','chatterbot.preprocessors.clean_whitespace'])

#the number of sentences saved in the database
ari8mosKataxwrhsewn = chatbot.storage.count()

#if there is no data in the database we train the bot with our training material
if(ari8mosKataxwrhsewn<1):
    #the default reply is saved first
    chatbot.neaKataxwrhsh(GreekSQLStorageAdapter.defaultReply,"",0)
    trainer = GreekChatterBotCorpusTrainer(chatbot)
    print("Bot's first training!")
    #to deutero arxeio den exei tonous stis erwthseis
    trainer.train('GreekBot.guide','GreekBot.guide2')

    #we increase the weight for each of the sentences saved to 2(max)
    for i in range(2,chatbot.storage.count()+1):
        chatbot.storage.updateWeightFromId(i,1)

defaultWelcome = "Γεια σας. Είμαι ο Μιληστερός. Ρωτήστε με ό,τι θέλετε να μάθετε για το πανεπιστήμιο."
defaultReplyAfter3 = "Μάλλον δεν ξέρω την απάντηση. Δοκιμάστε να ψάξετε στο dps.auth.gr/el/info/more"

defaultRepliesInARow = 0
protaseis = [defaultWelcome]#has all the sentences from the conversation
evaluated = []#has all the indexes of the sentences in protaseis that were evaluated by the user

#barh = []
#ratedConv = True;

'''
def resetConv():
    global protaseis
    protaseis = [defaultWelcome]
    global barh
    barh = []
    global defaultRepliesInARow
    defaultRepliesInARow = 0


def calcWeights(s):
    global barh
    barh=[]
    ola = len(protaseis)
    for i in range(0,ola):
        barh.append(s*round((i+1)/ola/2,2))#values from 0 to 0.5
        print(protaseis[i]+", "+str(barh[i]))


def saveLastSentence():
    if not protaseis[-1] == defaultWelcome:
        if not (chatbot.storage.isAlreadyStored(protaseis[-1], protaseis[-2])):
            chatbot.neaKataxwrhsh(protaseis[-1], protaseis[-2], 0)
        else:
            chatbot.storage.updateWeight(protaseis[-1], protaseis[-2], 0)

def saveLastSentence(weight):

    if len(protaseis)<2:
        if not (chatbot.storage.isAlreadyStored(protaseis[-1], defaultWelcome)):
            chatbot.neaKataxwrhsh(protaseis[-1], defaultWelcome, weight)
        else:
            chatbot.storage.updateWeight(protaseis[-1], defaultWelcome, weight)
    else:
        if not protaseis[-1] == defaultWelcome:
            if not (chatbot.storage.isAlreadyStored(protaseis[-1], protaseis[-2])):
                chatbot.neaKataxwrhsh(protaseis[-1], protaseis[-2], weight)
            else:
                chatbot.storage.updateWeight(protaseis[-1], protaseis[-2], weight)
'''

#saves a question and its answer to the database and adds to their default weight (value can be negative)
def save(index,weight):
    for i in range(index - 1, index + 1):
        #if the sentence is already stored in the database we only add to its weight
        if not (chatbot.storage.isAlreadyStored(protaseis[i], protaseis[i-1])):
            chatbot.neaKataxwrhsh(protaseis[i], protaseis[i-1], weight)
        else:
            chatbot.storage.updateWeight(protaseis[i], protaseis[i-1], weight)
    return


from flask import Flask, jsonify, request
app = Flask(__name__)
cors = CORS(app)

#calculates and returns the bot's reply to a given sentence
#if the bot returns the default reply three or more times in a row it is replaced by a different answer
def getAnswer(protash):
    apanthsh = chatbot.get_response(protash)
    apanthsh = str(apanthsh).replace("'","")#δε γίνεται για ", εμφανίζει πρόβλημα στην αποθήκευση
    global defaultRepliesInARow

    protaseis.append(apanthsh)

    if apanthsh==chatbot.storage.defaultReply:
        defaultRepliesInARow = defaultRepliesInARow + 1
        if defaultRepliesInARow >= 3:
            return defaultReplyAfter3
        else:
            return chatbot.storage.defaultReply
    else:
        defaultRepliesInARow = 0
        return apanthsh


#at the beginning of the conversation we give the default welcome sentence
@app.route('/start')
def getWelcome():
    global defaultRepliesInARow
    global protaseis
    global evaluated

    defaultRepliesInARow = 0
    protaseis = [defaultWelcome]
    evaluated = []
    return jsonify({"welcome":defaultWelcome})


#the user asks a question to the bot and we return its answer
@app.route('/',methods=['POST'])
def ask():

    erwthsh = request.get_json()
    erwthsh = chatbot.process_input(Statement(erwthsh["text"]))

    protaseis.append(erwthsh)

    if erwthsh.isspace() or not erwthsh:
        return

    apanthsh = getAnswer(erwthsh)

    return jsonify({"bot_reply":apanthsh,"you sent:":erwthsh}), 201


#the user can give positive or negative feedback to the bot about its latest answer
#we use it to calculate the weight of the question and answer in the database
#cannot be used many times in a row
@app.route('/evallast',methods=['POST'])
def evaluateLast():
    feedback = request.get_json()

    w = -0.2
    if(feedback["positive"]==1):
        w = 0.2

    l = len(protaseis)

    if(l>1):
        if not (protaseis[l-1] == chatbot.storage.defaultReply or protaseis[l-1] == defaultReplyAfter3) and not l-1 in evaluated:
            save(l-1,w)
            evaluated.append(l-1)
            evaluated.append(l-2)
            return jsonify({"text":"Saved"}), 201

    return jsonify({"text":"Not saved"}), 500



@app.route('/eval',methods=['POST'])
def evaluate():
    feedback = request.get_json()
    position = feedback["position"]#the position of the bot's answer starting from the user's first input as 1

    if (position<1):
        return jsonify({"text": "Invalid position"}), 500

    w = -0.2
    if (feedback["positive"] == 1):
        w = 0.2

    l = len(protaseis)


    if (l > 1):
        if not (protaseis[position] == chatbot.storage.defaultReply or protaseis[position] == defaultReplyAfter3) and not position in evaluated:
            save(position, w)
            evaluated.append(position)
            evaluated.append(position-1)
            return jsonify({"text": "Saved"}), 201

    return jsonify({"text":"Not saved"}), 500



app.config['JSON_AS_ASCII'] = False #to make it compatible with greek
app.run(port=443)

'''
def apo8hkeuse():


    if not (chatbot.storage.isAlreadyStored(protaseis[0],defaultWelcome)):
        chatbot.neaKataxwrhsh(protaseis[0],defaultWelcome,barh[0])
    else:
        chatbot.storage.updateWeight(protaseis[0],defaultWelcome,barh[0])

    for i in range(1,len(protaseis)):
        #den apo8hkeuoume tis protaseis oi opoies mphkan sth 8esh twn default apanthsewn
        if not protaseis[i] == defaultWelcome:

            if not (chatbot.storage.isAlreadyStored(protaseis[i], protaseis[i-1])):
                chatbot.neaKataxwrhsh(protaseis[i],protaseis[i-1],barh[i])
            else:
                chatbot.storage.updateWeight(protaseis[i],protaseis[i-1],barh[i])
'''



#Δημιουργία του παραθύρου με τη χρήση του Tkinter
#Το παράθυρο θα έχει εικονίδιο και συγκεκριμένη ανάλυση που δε θα μπορεί να την αλλάξει ο χρήστης
#window = Tk()
#window.title("Μιληστερός")
#window.geometry("880x300")
#window.iconbitmap("Images/Icon.ico")
#window.resizable(False,False);

#προσδιορισμός των εικόνων για τα κουμπιά της διεπαφής
#goodImage = PhotoImage(file = "Images/greenImage.png")
#badImage = PhotoImage(file = "Images/redImage.png")
#restartImage = PhotoImage(file = "Images/restartImage.png")

'''
def getAnswer(protash):
    apanthsh = chatbot.get_response(protash)
    apanthsh = str(apanthsh).replace("'","")#δε γίνεται για ", εμφανίζει πρόβλημα στην αποθήκευση
    global defaultRepliesInARow
    #print("defaultRepliesInARow ",defaultRepliesInARow)

    if apanthsh==chatbot.storage.defaultReply:
        defaultRepliesInARow = defaultRepliesInARow + 1
        if defaultRepliesInARow >= 3:
            putInBox(defaultReplyAfter3)
        else:
            putInBox(apanthsh)
    else:
        defaultRepliesInARow = 0
        putInBox(apanthsh)
    if apanthsh!=chatbot.storage.defaultReply:
        protaseis.append(apanthsh)
    else:
        protaseis.append(defaultWelcome)
    #print("defaultRepliesInARow ",defaultRepliesInARow)
'''


'''
def beforeExit():
    #if(not ratedConv):
    #   showPopUp()
    #else:
    window.destroy()

#myLabel είναι κείμενο το οποίο προσθέτουμε στην κορυφή του παραθύρου
odhgies = "Οδηγίες: Γράψτε στο κουτί και πατήστε το κουμπί αποστολής ή το Έντερ για συνομιλία με τον Μιληστερό." \
          "\nΜην ξεχάσετε να κάνετε αξιολόγηση πατώντας το πράσινο ή το κόκκινο κουμπί μετά τη συνομιλία." \
          "\nΜε το κίτρινο κουμπί μπορείτε να ξαναξεκινήσετε τη συνομιλία από την αρχή."
myLabel = Label(window,text = odhgies,bg="yellow",fg="black")
myLabel.pack()

#δημιουργία frame για το παράθυρο, σε αυτό θα μπούνε επιμέρους στοιχεία για καλύτερη οργάνωση
myFrame = Frame(window)

#μπάρα κύλισης στα δεξιά για προβολή όλης της συνομιλίας
scrollY = Scrollbar(myFrame)
scrollY.pack(side=RIGHT, fill=Y)

#μπάρα κύλισης κάτω για προβολή όλου του κειμένου
scrollΧ = Scrollbar(myFrame,orient=HORIZONTAL)
scrollΧ.pack(side=BOTTOM, fill=X)

#λίστα κειμένων της συνομιλίας και σύνδεσή της με τις μπάρες κύλισης
myBox = Listbox(myFrame, yscrollcommand = scrollY.set, xscrollcommand = scrollΧ.set, width = 140)
myBox.pack(side=LEFT)

#προσδιορισμός της λειτουργίας των scrollbars σε σχέση με τη λίστα κειμένων
scrollY.config(command = myBox.yview)
scrollΧ.config(command = myBox.xview)

#προσθήκη του frame στο παράθυρο, ρύθμιση ώστε να πιάνει όλο το μήκος του
myFrame.pack(fill=X)


#δημιουργία frame για τη γραμμή εργαλείων του χρήστη
frameBottom = Frame(window)

#εκτέλεση της keyup για κάθε release κουμπιού του πληκτρολογίου
window.bind("<KeyRelease>", keyup)

#μπάρα εισόδου κειμένου από τον χρήστη στα αριστερά
entry = Entry(frameBottom, width = 100)
entry.grid(row=0,column=0, sticky=E)

#τρία παρόμοια κουμπιά, με εικόνες αυτές που προσδιορίσαμε παραπάνω, δίπλα από την μπάρα εισόδου
#Η κάθε μία κάνει διαφορετική λειτουργία ανάλογα με την συνάρτηση που της έχουμε αναθέσει
#Τις τοποθετούμε στο frame
buttonEnter = Button(frameBottom,command=printUserText,text="Αποστολή")
buttonEnter.grid(row=0,column=1,sticky=E)

buttonGreen = Button(frameBottom,command = ektypwths, image=goodImage)
buttonGreen.grid(row=0,column=2,sticky=E)

buttonRed = Button(frameBottom,command = ektypwths2, image=badImage)
buttonRed.grid(row=0,column=3,sticky=E)

buttonRestart = Button(frameBottom,bg="yellow",command = clearBox, image=restartImage)
buttonRestart.grid(row=0,column=4,sticky=E)

#Προσθέτουμε το frame το παράθυρο
frameBottom.pack()


putInBox(defaultWelcome)
#protaseis.append(defaultWelcome)

window.protocol("WM_DELETE_WINDOW", beforeExit)

#Το παράθυρο θα ανανεώνεται συνέχεια
#window.mainloop()

'''
