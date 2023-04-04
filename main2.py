# things we need for NLP
import nltk
from nltk.stem.lancaster import LancasterStemmer
from tensorflow.python.framework import ops

# things we need for Tensorflow
import numpy as np
import tflearn
import tensorflow as tf
import random

# import our chat-bot intents file
import json

stemmer = LancasterStemmer()
with open('intents.json') as json_data:
    data = json.load(json_data)

words = []
documents = []
labels=[]
classes = []
ignore_words = ['?']

# loop through each sentence in our intents patterns
for intent in data['intents']:
    for pattern in intent['patterns']:
        # tokenize each word in the sentence
        w = nltk.word_tokenize(pattern)
        # add to our words list
        words.extend(w)
        # add to documents in our corpus
        documents.append((w, intent['tag']))
        # add to our classes list
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

# stem and lower each word and remove duplicates
words = [stemmer.stem(w.lower()) for w in words if w not in ignore_words]
words = sorted(list(set(words)))

# remove duplicates
classes = sorted(list(set(classes)))

print (len(documents), "documents")
print (len(classes), "classes", classes)
print (len(words), "unique stemmed words", words)

# create our training data
training = []
output = []
# create an empty array for our output
output_empty = [0] * len(classes)

# training set, bag of words for each sentence
for doc in documents:
    # initialize our bag of words
    bag = []
    # list of tokenized words for the pattern
    pattern_words = doc[0]
    # stem each word
    pattern_words = [stemmer.stem(word.lower()) for word in pattern_words]
    # create our bag of words array
    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)

    # output is a '0' for each tag and '1' for current tag
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1

    training.append([bag, output_row])

# shuffle our features and turn into np.array
random.shuffle(training)
training = np.array(training,dtype=object)

# create train and test lists
train_x = list(training[:,0])
train_y = list(training[:,1])

ops.reset_default_graph()

# reset underlying graph data
# tf.reset_default_graph()
# Build neural network
net = tflearn.input_data(shape=[None, len(train_x[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
net = tflearn.regression(net)

# Define model and setup tensorboard
model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')
# Start training (apply gradient descent algorithm)
model.fit(train_x, train_y, n_epoch=1000, batch_size=8, show_metric=True)
model.save('model.tflearn')


def bag_of_words(s,words):
    bag = [0 for _ in range(len(words))]
    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i,w in enumerate(words):
            if w ==se:
                bag[i] = 1
    return np.array(bag)

def chat():
    print ("Hello, how may i help you today?")
    while True:
        inp = input("You: -> ")
        if inp.lower() == 'quit':
            break

        results = model.predict([bag_of_words(inp,words)])
        result_index = np.argmax(results)
        tag = labels[result_index]

        for tg in intents['intents']:
            if tg['tag']==tag:
                responses = tg['responses']
        
        print (random.choice(responses))

chat()
    
    



# # save all of our data structures
# import pickle
# pickle.dump( {'words':words, 'classes':classes, 'train_x':train_x, 'train_y':train_y}, open( "training_data", "wb" ) )

# # restore all of our data structures
# import pickle
# data = pickle.load( open( "training_data", "rb" ) )
# words = data['words']
# classes = data['classes']
# train_x = data['train_x']
# train_y = data['train_y']

# # import our chat-bot intents file
# import json
# with open('intents.json') as json_data:
#     intents = json.load(json_data)

# # load our saved model
# model.load('./model.tflearn')

# def clean_up_sentence(sentence):
#     # tokenize the pattern
#     sentence_words = nltk.word_tokenize(sentence)
#     # stem each word
#     sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
#     return sentence_words

# # return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
# def bow(sentence, words, show_details=False):
#     # tokenize the pattern
#     sentence_words = clean_up_sentence(sentence)
#     # bag of words
#     bag = [0]*len(words)  
#     for s in sentence_words:
#         for i,w in enumerate(words):
#             if w == s: 
#                 bag[i] = 1
#                 if show_details:
#                     print ("found in bag: %s" % w)

#     return(np.array(bag))

# ERROR_THRESHOLD = 0.25
# def classify(sentence):
#     # generate probabilities from the model
#     results = model.predict([bow(sentence, words)])[0]
#     # filter out predictions below a threshold
#     results = [[i,r] for i,r in enumerate(results) if r>ERROR_THRESHOLD]
#     # sort by strength of probability
#     results.sort(key=lambda x: x[1], reverse=True)
#     return_list = []
#     for r in results:
#         return_list.append((classes[r[0]], r[1]))
#     # return tuple of intent and probability
#     return return_list

# def response(sentence, userID='123', show_details=False):
#     results = classify(sentence)
#     # if we have a classification then find the matching intent tag
#     if results:
#         # loop as long as there are matches to process
#         while results:
#             for i in intents['intents']:
#                 # find a tag matching the first result
#                 if i['tag'] == results[0][0]:
#                     # a random response from the intent
#                     return print(random.choice(i['responses']))

#             results.pop(0)



















# things we need for NLP
import nltk
from nltk.stem.lancaster import LancasterStemmer
from tensorflow.python.framework import ops
import directory
import wordCorrection

# things we need for Tensorflow
import numpy as np
import tflearn
import tensorflow as tf
import random
import requests
from io import BytesIO
import PyPDF2

# import our chat-bot intents file
import json

#=====================================Loading the intents and training the model=============================

stemmer = LancasterStemmer()
with open('intents.json') as json_data:
    intents = json.load(json_data)

words = []
labels = []
documents = []
ignore_words = ['?']

# loop through each sentence in our intents patterns
for intent in intents['intents']:
    for pattern in intent['patterns']:
        # tokenize each word in the sentence
        w = nltk.word_tokenize(pattern)
        # add to our words list
        words.extend(w)
        # add to documents in our corpus
        documents.append((w, intent['tag']))
        # add to our labels list
        if intent['tag'] not in labels:
            labels.append(intent['tag'])

# stem and lower each word and remove duplicates
words = [stemmer.stem(w.lower()) for w in words if w not in ignore_words]
words = sorted(list(set(words)))

# remove duplicates
labels = sorted(list(set(labels)))

# print (len(docs_x), "documents")
# print (len(labels), "labels", labels)
# print (len(words), "unique stemmed words", words)

# create our training data
training = []
output = []
# create an empty array for our output
output_empty = [0] * len(labels)

# training set, bag of words for each sentence
for doc in documents:
    # initialize our bag of words
    bag = []
    # list of tokenized words for the pattern
    pattern_words = doc[0]
    # stem each word
    pattern_words = [stemmer.stem(word.lower()) for word in pattern_words]
    # create our bag of words array
    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)

    # output is a '0' for each tag and '1' for current tag
    output_row = list(output_empty)
    output_row[labels.index(doc[1])] = 1

    training.append([bag, output_row])

# shuffle our features and turn into np.array
random.shuffle(training)
training = np.array(training,dtype=object)

# create train and test lists
train_x = list(training[:,0])
train_y = list(training[:,1])


# reset underlying graph data
ops.reset_default_graph()

# Build neural network
net = tflearn.input_data(shape=[None, len(train_x[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
net = tflearn.regression(net)

# Define model and setup tensorboard
model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')

# Start training (apply gradient descent algorithm)
model.fit(train_x, train_y, n_epoch=1000, batch_size=8, show_metric=True)
model.save('model.tflearn')


def bag_of_words(s,words):
    bag = [0 for _ in range(len(words))]
    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i,w in enumerate(words):
            if w ==se:
                bag[i] = 1
    return np.array(bag)

#===========================fetching professor's details===================================
def read_pdf(url):
    response = requests.get(url)
    pdf_file = BytesIO(response.content)
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    text = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text

# url = "https://www.pvamu.edu/sites/hb2504/cvs/All/amahmed.pdf"
def get_professor_details(url):
    text = read_pdf(url)

    # def getOffice_info(text):
    with open('repository.txt','w') as repo:
        repo.write(text)

    with open('repository.txt','r') as repo:
        for line in repo:
            if "Office Location" in line:
                return line

#================================Run the chatbot=============================================
def to_camel_case(text):
    words = text.lower().split()
    return words[0] + ''.join(word.capitalize() for word in words[1:])

# def correctSentence(inp):
#     corr_inp = wordCorrection.autocorrect_sentence(inp)

#     if corr_inp==inp:
#         results = model.predict([bag_of_words(inp,words)])
#         result_index = np.argmax(results)
#         tag = labels[result_index]
#         return tag
#     else:
#         print (f'do you mean "{corr_inp}" ?')
#         res = input("You: ")
#         if res[0].lower()=='y':
#             results = model.predict([bag_of_words(corr_inp,words)])
#             result_index = np.argmax(results)
#             tag = labels[result_index]
#             return tag
#         else:
#             print ("please ask your question again")
#             inp= input("You: ")
#             # return correctSentence(inp)
#             results = model.predict([bag_of_words(inp,words)])
#             result_index = np.argmax(results)
#             tag = labels[result_index]
#             return tag
# def response_tag(tag):
#     for tg in intents['intents']:
#             if tg['tag']==tag:
#                 responses = tg['responses']
        
#     return random.choice(responses)

# def chat():
#     print ("Hello, how may i help you today?")
#     while True:
#         inp = input("You: ")
#         if inp.lower() == 'quit':
#             break

#         tag = correctSentence(inp)
#         for tg in intents['intents']:
#             if tg['tag']==tag:
#                 responses = tg['responses']
        
#         print (random.choice(responses))
#         # return random.choice(responses)

# chat()
#===================alternative way to run the chatbot in UI========================
import tkinter as tk
def ask_input():
    response = entry_box.get()
    return response
def correctSentence(inp):
    corr_inp = wordCorrection.autocorrect_sentence(inp)

    if corr_inp==inp:
        results = model.predict([bag_of_words(inp,words)])
        result_index = np.argmax(results)
        if results[0][result_index] <0.60:
            print (results)
            print (result_index)
            # print("sorry i can't help you")
            tag = "NULL"
            return tag
        else:
            print (results)
            print (result_index)
            tag = labels[result_index]
            return tag
        # tag = labels[result_index]
        # return tag
    else:
        # print (f'do you mean "{corr_inp}" ?')
        # chat_window.config(state=tk.NORMAL)
        chat_window.insert(tk.END, f'do you mean "{corr_inp}" ?' + "\n\n")
        # res = entry_box.get()
        # get user input

        user_message = entry_box.get()
        # clear input box
        entry_box.delete(0, tk.END)
        # display user message in chat window
        chat_window.config(state=tk.NORMAL)
        chat_window.insert(tk.END, "You: " + user_message + "\n\n")

        # res = entry_box.get()
        # # clear input box
        # entry_box.delete(0, tk.END)
        # # display user message in chat window
        # chat_window.config(state=tk.NORMAL)
        # res = tk.Entry().get()
        print ("why can't i see _____"+res+" _____again")
        if res[0].lower()=='y':
            results = model.predict([bag_of_words(corr_inp,words)])
            result_index = np.argmax(results)

            if results[0][result_index] <0.60:
                tag = "NULL"
                return tag
            else:
                tag = labels[result_index]
                return tag

            # tag = labels[result_index]
            # return tag
        else:
            # print ("please ask your question again")
            # chat_window.config(state=tk.NORMAL)
            # chat_window.insert(tk.END, "please ask your question again" + "\n\n")
            # inp = entry_box.get()
            # correctSentence(inp)
            tag = "repeat"
            return tag
        # tag = "repeat"
        # return tag
            
def send_message(event=None):
    # get user input
    user_message = entry_box.get()
    # clear input box
    entry_box.delete(0, tk.END)
    # display user message in chat window
    chat_window.config(state=tk.NORMAL)
    chat_window.insert(tk.END, "You: " + user_message + "\n\n")
    tag = correctSentence(user_message)
    responses = ""
    for tg in intents['intents']:
            if tg['tag']==tag:
                responses = tg['responses']
        
    chatbot_response = (random.choice(responses))
    chat_window.config(state=tk.DISABLED)
    # get chatbot response
    chatbot_message = chatbot_response
    # display chatbot response in chat window
    chat_window.config(state=tk.NORMAL)
    chat_window.insert(tk.END, "PantherBot: " + chatbot_message + "\n\n")
    chat_window.config(state=tk.DISABLED)
    # scroll chat window to bottom
    chat_window.see(tk.END)

# # def send_message(event=None):
# #     # get user input
# #     user_message = entry_box.get()
# #     # clear input box
# #     entry_box.delete(0, tk.END)
# #     # display user message in chat window
# #     chat_window.config(state=tk.NORMAL)
# #     chat_window.insert(tk.END, "You: " + user_message + "\n\n")
# #     tag = correctSentence(user_message)
# #     for tg in intents['intents']:
# #             if tg['tag']==tag:
# #                 responses = tg['responses']
        
# #     chatbot_response = (random.choice(responses))
# #     chat_window.config(state=tk.DISABLED)
# #     # get chatbot response
# #     chatbot_message = chatbot_response
# #     # display chatbot response in chat window
# #     chat_window.config(state=tk.NORMAL)
# #     chat_window.insert(tk.END, "PantherBot: " + chatbot_message + "\n\n")
# #     chat_window.config(state=tk.DISABLED)
# #     # scroll chat window to bottom
# #     chat_window.see(tk.END)

# create tkinter window
window = tk.Tk()
window.title("PVAMU Chatbot")

# create chat window
chat_window = tk.Text(window, height=20, width=50)
chat_window.pack(fill=tk.BOTH, expand=True)
chat_window.config(state=tk.DISABLED)
chat_window.pack()

chat_window.config(state=tk.NORMAL)
chat_window.insert(tk.END, "PantherBot: Hi, I'm PantherBot, your assistance. How can I help you today?" + "\n\n")
chat_window.config(state=tk.DISABLED)

# create entry box for user input
entry_box = tk.Entry(window)
# entry_box.pack()
entry_box.bind("<Return>", send_message)
entry_box.pack()

# create send button
send_button = tk.Button(window, text="Send", command=send_message)
send_button.pack()

# start tkinter event loop
window.mainloop()

