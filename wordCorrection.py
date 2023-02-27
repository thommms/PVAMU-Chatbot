from textblob import TextBlob

def autocorrect_sentence(sentence):
    # Create a TextBlob object for the given sentence
    blob = TextBlob(sentence)
    
    # Get the corrected sentence
    corrected_sentence = str(blob.correct())
    
    return corrected_sentence

sentence = "I am from the departmt of computer scienc"
print (autocorrect_sentence(sentence))