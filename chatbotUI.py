import tkinter as tk
# import main

# function to handle chatbot logic
def chatbot_response():
    # your chatbot logic here
    response = "Hello, how can I help you today?"
    return response
# chatbot_response = main.chat()
chatbot_response = chatbot_response()

# function to handle sending user input
def send_message(event=None):
    # get user input
    user_message = entry_box.get()
    # clear input box
    entry_box.delete(0, tk.END)
    # display user message in chat window
    chat_window.config(state=tk.NORMAL)
    chat_window.insert(tk.END, "You: " + user_message + "\n\n")
    chat_window.config(state=tk.DISABLED)
    # get chatbot response
    chatbot_message = chatbot_response
    # display chatbot response in chat window
    chat_window.config(state=tk.NORMAL)
    chat_window.insert(tk.END, "Chatbot: " + chatbot_message + "\n\n")
    chat_window.config(state=tk.DISABLED)
    # scroll chat window to bottom
    chat_window.see(tk.END)

# create tkinter window
window = tk.Tk()
window.title("Chatbot")

# create chat window
chat_window = tk.Text(window, height=20, width=50)
chat_window.config(state=tk.DISABLED)
chat_window.pack()

# create entry box for user input
entry_box = tk.Entry(window)
entry_box.bind("<Return>", send_message)
entry_box.pack()

# create send button
send_button = tk.Button(window, text="Send", command=send_message)
send_button.pack()

# start tkinter event loop
window.mainloop()
