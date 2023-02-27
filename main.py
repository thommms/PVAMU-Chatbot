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

# words = []
# labels = []
# docs_x = []
# docs_y = []
# ignore_words = ['?']

# # loop through each sentence in our intents patterns
# for intent in intents['intents']:
#     for pattern in intent['patterns']:
#         # tokenize each word in the sentence
#         wrds = nltk.word_tokenize(pattern)
#         # add to our words list
#         words.extend(wrds)
#         # add to documents in our corpus
#         docs_x.append(pattern)
#         docs_y.append(intent['tag'])
#         # add to our labels list
#         if intent['tag'] not in labels:
#             labels.append(intent['tag'])

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

def correctSentence(inp):
    corr_inp = wordCorrection.autocorrect_sentence(inp)

    if corr_inp==inp:
        results = model.predict([bag_of_words(inp,words)])
        result_index = np.argmax(results)
        tag = labels[result_index]
        return tag
    else:
        print (f'do you mean "{corr_inp}" ?')
        res = input("You: ")
        if res[0].lower()=='y':
            results = model.predict([bag_of_words(corr_inp,words)])
            result_index = np.argmax(results)
            tag = labels[result_index]
            return tag
        else:
            print ("please ask your question again")
            inp= input("You: ")
            correctSentence(inp)

def chat():
    print ("Hello, how may i help you today?")
    while True:
        inp = input("You: ")
        if inp.lower() == 'quit':
            break

        tag = correctSentence(inp)
        # if corr_inp==inp:
        #     results = model.predict([bag_of_words(inp,words)])
        #     result_index = np.argmax(results)
        #     tag = labels[result_index]
        # else:
        #     print (f'do you mean "{corr_inp}" ?')
        #     res = input("You: ")
        #     if res[0].lower()=='y':
        #         results = model.predict([bag_of_words(corr_inp,words)])
        #         result_index = np.argmax(results)
        #         tag = labels[result_index]
        #     else:
        #         print ("please ask your question again")
        #         inp= input("You: ")
        #         correctSentence(inp,corr_inp)
                # results = model.predict([bag_of_words(inp,words)])
                # result_index = np.argmax(results)
                # tag = labels[result_index]

        for tg in intents['intents']:
            if tg['tag']==tag:
                responses = tg['responses']
        
        print (random.choice(responses))

chat()


# #========================
# # things we need for NLP
# import nltk
# from nltk.stem.lancaster import LancasterStemmer
# from tensorflow.python.framework import ops

# # things we need for Tensorflow
# import numpy as np
# import tflearn
# import tensorflow as tf
# import random
# import requests
# from io import BytesIO
# import PyPDF2

# # import our chat-bot intents file
# import json

# #=====================================Loading the intents and training the model=============================
# stemmer = LancasterStemmer()
# with open('intents.json') as json_data:
#     intents = json.load(json_data)

# words = []
# labels = []
# documents = []
# ignore_words = ['?']

# # loop through each sentence in our intents patterns
# for intent in intents['intents']:
#     for pattern in intent['patterns']:
#         # tokenize each word in the sentence
#         w = nltk.word_tokenize(pattern)
#         # add to our words list
#         words.extend(w)
#         # add to documents in our corpus
#         documents.append((w, intent['tag']))
#         # add to our labels list
#         if intent['tag'] not in labels:
#             labels.append(intent['tag'])

# # stem and lower each word and remove duplicates
# words = [stemmer.stem(w.lower()) for w in words if w not in ignore_words]
# words = sorted(list(set(words)))

# # remove duplicates
# labels = sorted(list(set(labels)))

# print (len(documents), "documents")
# print (len(labels), "labels", labels)
# print (len(words), "unique stemmed words", words)

# # create our training data
# training = []
# output = []
# # create an empty array for our output
# output_empty = [0] * len(labels)

# # training set, bag of words for each sentence
# for doc in documents:
#     # initialize our bag of words
#     bag = []
#     # list of tokenized words for the pattern
#     pattern_words = doc[0]
#     # stem each word
#     pattern_words = [stemmer.stem(word.lower()) for word in pattern_words]
#     # create our bag of words array
#     for w in words:
#         bag.append(1) if w in pattern_words else bag.append(0)

#     # output is a '0' for each tag and '1' for current tag
#     output_row = list(output_empty)
#     output_row[labels.index(doc[1])] = 1

#     training.append([bag, output_row])

# # shuffle our features and turn into np.array
# random.shuffle(training)
# training = np.array(training,dtype=object)

# # create train and test lists
# train_x = list(training[:,0])
# train_y = list(training[:,1])


# # reset underlying graph data
# ops.reset_default_graph()

# # Build neural network
# net = tflearn.input_data(shape=[None, len(train_x[0])])
# net = tflearn.fully_connected(net, 8)
# net = tflearn.fully_connected(net, 8)
# net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
# net = tflearn.regression(net)

# # Define model and setup tensorboard
# model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')

# # Start training (apply gradient descent algorithm)
# model.fit(train_x, train_y, n_epoch=1000, batch_size=8, show_metric=True)
# model.save('model.tflearn')


# def bag_of_words(s,words):
#     bag = [0 for _ in range(len(words))]
#     s_words = nltk.word_tokenize(s)
#     s_words = [stemmer.stem(word.lower()) for word in s_words]

#     for se in s_words:
#         for i,w in enumerate(words):
#             if w ==se:
#                 bag[i] = 1
#     return np.array(bag)

# #===========================fetching professor's details===================================
# def read_pdf(url):
#     response = requests.get(url)
#     pdf_file = BytesIO(response.content)
#     pdf_reader = PyPDF2.PdfReader(pdf_file)

#     text = ""
#     for page_num in range(len(pdf_reader.pages)):
#         page = pdf_reader.pages[page_num]
#         text += page.extract_text()
#     return text

# # url = "https://www.pvamu.edu/sites/hb2504/cvs/All/amahmed.pdf"
# def get_professor_details(url):
#     text = read_pdf(url)

#     # def getOffice_info(text):
#     with open('repository.txt','w') as repo:
#         repo.write(text)

#     with open('repository.txt','r') as repo:
#         for line in repo:
#             if "Office Location" in line:
#                 return line

# #================================Run the chatbot=============================================
# def chat():
#     print ("Hello, how may i help you today?")
#     while True:
#         inp = input("You: ")
#         if inp.lower() == 'quit':
#             break

#         results = model.predict([bag_of_words(inp,words)])
#         result_index = np.argmax(results)
#         tag = labels[result_index]

#         for tg in intents['intents']:
#             if tg['tag']==tag:
#                 responses = tg['responses']
        
#         print (random.choice(responses))

# chat()


