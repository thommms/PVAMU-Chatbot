from tkinter import *
import webbrowser

# create the main window
root = Tk()
root.title("Chatbot")

# create the chat display area
chat_display = Text(root, height=20, width=50)
chat_display.pack()

# create the input field
input_field = Entry(root, width=50)
input_field.pack()

# create the send button
send_button = Button(root, text="Send")
send_button.pack()

# Define the callback function
def callback(url):
   webbrowser.open_new(url)

# function to handle sending messages
def send_message():
    message = input_field.get()
    chat_display.insert(END, "You: " + message + "\n")
    input_field.delete(0, END)
    if message.lower() == "hello":
        bot_response = "Hello! How can I assist you today?"
    else:
        bot_response = "Thanks for coming, check out my link today:"
        chat_display.insert(END, "Bot: " + bot_response + " ")
        link = Label(chat_display, text="link", font=('Helvetica', 12, 'underline'), fg="blue", cursor="hand2")
        link.pack(side="left")
        link.bind("<Button-1>", lambda e: callback("http://www.example.com"))
        chat_display.insert(END, "\n")
    chat_display.insert(END, "Bot: " + bot_response + "\n")

# bind the send button to the send_message function
send_button.config(command=send_message)

# run the main loop
root.mainloop()
