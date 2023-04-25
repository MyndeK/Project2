# import all the required  modules
import socket
import threading
from tkinter import *
from tkinter import font
from tkinter import ttk
import tkinter
from PIL import Image, ImageTk
from datetime import datetime
from tkinter import filedialog
import os

# import all functions /

PORT = 5000
SERVER = "34.251.169.188"
ADDRESS = (SERVER, PORT)
FORMAT = "utf-8"
 
# Create a new client socket
# and connect to the server
client = socket.socket(socket.AF_INET,
                       socket.SOCK_STREAM)
client.connect(ADDRESS)
 

# GUI class for the chat
class GUI:
    # constructor method
    def __init__(self):
        
       
        # chat window which is currently hidden
        self.Window = Tk()
        self.Window.withdraw()
        
        # login window
        self.login = Toplevel()
        # set the title
        self.login.title("Login")
        self.login.resizable(width=True,
                             height=True)
        #img= PhotoImage(file="C:\Users\mynde\Desktop\Login.png")


        #self.picture=Label(self.login, Image=img,).pack()

        
        self.login.configure(width=600,
                             height=600,
                             bg="sky blue")

        # create a Label
        self.pls = Label(self.login,
                         text="Chat Room",
                         justify=CENTER,
                         font="lucida 12 bold",
                         bg="#FFFFEF")
 
        self.pls.place(relheight=0.10,
                       relx=0.40,
                       rely=0.15)
        # create a Label
        self.labelName = Label(self.login,
                               text="Name: ",
                               font="lucida 12 bold",
                               bg="#FFFFEF")
 
        self.labelName.place(relheight=0.10,
                             relwidth= 0.14,
                             relx=0.1,
                             rely=0.25)

        # create a entry box for
        # tyoing the message
        self.entryName = Entry(self.login,
                               font="lucida 12 bold",
                               bg="#FFFFEF")
 
        self.entryName.place(relwidth=0.35,
                             relheight=0.12,
                             relx=0.30,
                             rely=0.25)

        # set the focus of the cursor
        self.entryName.focus()
 
        # create a Connect Button
        # along with action
        self.go = Button(self.login,
                         text="Connect",
                         font="lucida 12 bold",
                         command=lambda: self.goAhead(self.entryName.get()),
                         bg="#FFFFEF")
        
        self.go.place(relx=0.3,
                      rely=0.55)
        # create a Disconnect Button
        self.Exit = Button(self.login,
                         text="Exit",
                         font="lucida 12 bold",
                         bg="#FFFFEF",
                         command=self.login.destroy)                   
       
        self.Exit.place(relwidth= 0.14,
                        relx = 0.5,
                        rely= 0.55)

        self.Window.mainloop()
    



    def goAhead(self, name):
        self.login.destroy()
        self.layout(name)
 
        # the thread to receive messages
        rcv = threading.Thread(target=self.receive)
        rcv.start()
 
    # The main layout of the chat
    def layout(self, name):
        
        self.name = name
        # to show chat window
        self.Window.deiconify()
        self.Window.title("Chat Room")
        self.Window.resizable(width=False,
                              height=False)
        self.Window.configure(width=800,
                              height=800,
                              bg="sky blue")
        self.labelHead = Label(self.Window,
                               fg="#000000",                              
                               text="Welcome to Chat Room: " +self.name,                              
                               bg="sky blue",                              
                               font="lucida 12 bold")
        self.labelHead.place(relwidth=0.4)
        #Datetime
        self.date = Label(self.Window,
                          bg="sky blue",
                          text=datetime.now().strftime('%H:%M:%S %p \n %d %B'),
                          font="lucida 12 bold")
                          
        self.date.place(relwidth=0.4,                       
                        rely=0.05)
        #Label for client list 
        self.label_right = Label(self.Window,
                                bg="sky blue",
                                text="Online List",
                                font="lucida 12 bold")
        self.label_right.place(relwidth=0.4,
                                relx=0.55,
                                rely=0.05)
        #Clients online
        self.client_frame = Text(self.Window,
                                 bg="#FFFFF8")
        self.client_frame.place(relwidth=0.4,
                                rely=0.1,
                                relx=0.55)
        #Text Window for Messages
        self.textCons = Text(self.Window,
                             width=13,
                             height=2,
                             bg="#FFFFEF",
                             fg="#000000",
                             font="lucida 12 bold")
 
        self.textCons.place(relheight=0.70,
                            relwidth=0.5,
                            rely=0.1)
        #Enter message Label
        self.labelBottom = Label(self.Window,
                                 bg="#C1C1CD",
                                 height=80)
 
        self.labelBottom.place(relwidth=1,
                               rely=0.825)
 
        self.entryMsg = Entry(self.labelBottom,
                              bg="#C1C1CD",
                              fg="#000000",
                              font="lucida 12 bold")    
 
        # place the given widget
        # into the gui window
        self.entryMsg.place(relwidth=0.74,
                            relheight=0.06,
                            rely=0.008,
                            relx=0.011)
 
        self.entryMsg.focus()
 
        # create a Send Button
        self.buttonMsg = Button(self.labelBottom,
                                text="Send",
                                font="lucida 12 bold",
                                width=10,
                                bg="sky blue",
                                command=lambda: self.sendButton(self.entryMsg.get()))
        self.buttonMsg.place(relx=0.77,
                             rely=0.06,
                             relheight=0.03,
                             relwidth=0.22)
        # create a Disconnect Button

        
        self.buttonMsgDisconnect = Button(self.labelBottom,
                                text="Disconnect",
                                font="lucida 12 bold",
                                width=10,
                                bg="sky blue",
                                command=self.Disconnect)
        self.buttonMsgDisconnect.place(relx=0.77,
                             rely=0.008,
                             relheight=0.03,
                             relwidth=0.22)
 
        self.textCons.config(cursor="arrow")

        # create a scroll bar
        scrollbar = Scrollbar(self.textCons)
 
        # place the scroll bar
        # into the gui window
        scrollbar.place(relheight=1,
                        relx=0.974)
        
        scrollbar.config(command=self.textCons.yview)
 
        self.textCons.config(state=DISABLED)

    def Disconnect(self):
        client.close()
        self.Window.destroy()

    # function to basically start the thread for sending messages
    def sendButton(self, msg):
        self.textCons.config(state=DISABLED)
        self.msg = msg
        self.entryMsg.delete(0, END)
        snd = threading.Thread(target=self.sendMessage)
        snd.start()
    # function to receive messages
    def receive(self):
        while True:
            try:
                message = client.recv(1024).decode(FORMAT)
 
                # if the messages from the server is NAME send the client's name
                if message == 'NAME':
                    client.send(self.name.encode(FORMAT))
                else:
                    # insert messages to text box
                    self.textCons.config(state=NORMAL)
                    self.textCons.insert(END,
                                         message+"\n\n")
 
                    self.textCons.config(state=DISABLED)
                    self.textCons.see(END)
            except:
                # an error will be printed on the command line or console if there's an error
                print("An error occurred!")
                client.close()
                
                break
 
    # function to send messages
    def sendMessage(self):
        self.textCons.config(state=DISABLED)
        while True:
            message = (f"{self.name}: {self.msg}")
            client.send(message.encode(FORMAT))

            break


    
 
# create a GUI class object
g = GUI()