import json

# function to add to JSON
def write_json(new_data, filename='intents.json'):
    # Read the JSON file into memory
    with open(filename, 'r') as file:
        file_data = json.load(file)

    # Convert the JSON data into a list of dictionaries
    # file_data = [dict(item) for item in file_data]
    intents = list(file_data.keys())[0]

    # Removing the duplicates from the list of dictionaries
    # unique_data = list(set(tuple(item.items()) for item in file_data['intents']))  
    # for data in file_data[intents]:
    unique_data = file_data[intents]
    
    #replace any duplicate keys with the new value
    for i,d in enumerate(unique_data):
        if d["tag"] == new_data["tag"]:
            unique_data[i]=new_data
            break
    else:
        unique_data.append(new_data)

    #convert the final list to dictionary
    file_data = {intents:unique_data}
    print (file_data)

    # Write the modified data back to the JSON file
    with open('intents.json', 'w') as file:
        json.dump(file_data, file, indent=4)

# new_data = {
#         "tag": "bellam",
#         "patterns": [
#                 "I would like to see Dr Bellam",
#                 "Where is Dr. Bellam's office",
#                 "When is the office hour or office location of dr Bellam"
#         ],
#         "responses": [
#                 "WHYYYYYY"
#         ],
#         "context_set": ""
#         }
# write_json(new_data)