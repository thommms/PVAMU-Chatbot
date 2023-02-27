
import directory
import nltk

# def autocorrect(sentence, word_list):
#     corrected_words = []
#     for word in sentence.split():
#         if word.lower() in word_list:
#             corrected_words.append(word)
#         else:
#             closest_match = find_closest_match(word.lower(), word_list)
#             if closest_match:
#                 corrected_words.append(closest_match)
#             else:
#                 corrected_words.append(word)
#     return ' '.join(corrected_words)
def autocorrect(sentence, word_list):
    corrected_words = []
    for word in sentence.split():
        lowercase_word = word.lower()
        if lowercase_word in word_list:
            corrected_words.append(word)
        else:
            closest_match = find_closest_match(lowercase_word, word_list)
            if closest_match:
                corrected_words.append(closest_match.title())
            else:
                corrected_words.append(word)
    return ' '.join(corrected_words)

def find_closest_match(word, word_list):
    min_distance = float('inf')
    closest_word = ''
    for word2 in word_list:
        distance = levenshtein_distance(word.lower(), word2.lower())
        if distance < min_distance:
            min_distance = distance
            closest_word = word2
    if min_distance <= 2:
        return closest_word
    else:
        return None

def levenshtein_distance(s, t):
    if len(s) < len(t):
        return levenshtein_distance(t, s)
    if len(t) == 0:
        return len(s)
    previous_row = range(len(t) + 1)
    for i, c1 in enumerate(s):
        current_row = [i + 1]
        for j, c2 in enumerate(t):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]

def get_ind_departments(all_dept):
    for string in all_dept:
        if ' ' in string:
            all_dept.extend(string.split())
        else:
            all_dept.append(string)
    return all_dept

tok_depts = get_ind_departments(directory.get_all_dept_names())

print(tok_depts)
# print (nltk.word_tokenize())


# sentence = "My professor's name is dr Belam"
# word_list = ['Christopher', 'Alam', 'Bellam']
# corrected_sentence = autocorrect(sentence, word_list)
# print(corrected_sentence)
#=========================
phrases = ['Hello, how are you?', 'I am doing well, thank you.', 'What about you?']
tokenized_phrases = [phrase.split() for phrase in phrases]
tokens = []
for phrase_tokens in tokenized_phrases:
    tokens.extend(phrase_tokens)
print(tokens)
