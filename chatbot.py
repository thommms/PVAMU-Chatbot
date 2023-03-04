import tkinter as tk
from chatbot import Chatbot
# from main import chat

class ChatbotUI:
    def __init__(self, master):
        self.master = master
        master.title("Chatbot")

        # create a chatbot instance
        self.chatbot = chat()

        # create a text box for user input
        self.user_input = tk.Entry(master)
        self.user_input.pack()

        # create a text box for chatbot output
        self.chat_output = tk.Text(master)
        self.chat_output.pack()

        # create a button for sending user input to the chatbot
        self.send_button = tk.Button(master, text="Send", command=self.send)
        self.send_button.pack()

        self.chatbot = chat()


    def send(self):
        user_input = self.user_input.get()
        self.user_input.delete(0, tk.END)
        chatbot_response = self.chatbot.respond(user_input)
        self.chat_output.insert(tk.END, f"User: {user_input}\n")
        self.chat_output.insert(tk.END, f"Chatbot: {chatbot_response}\n")

root = tk.Tk()
chatbot_ui = ChatbotUI(root)
root.mainloop()
