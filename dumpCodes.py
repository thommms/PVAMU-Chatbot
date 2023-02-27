
# # function to add to JSON
# def write_json(new_data, filename='sample.json'):
#     # Read the JSON file into memory
#     with open(filename, 'r') as file:
#         file_data = json.load(file)

#     # Convert the JSON data into a list of dictionaries
#     # file_data = [dict(item) for item in file_data]
#     intents = list(file_data.keys())[0]

#     # Removing the duplicates from the list of dictionaries
#     unique_data = list(set(tuple(item.items()) for item in file_data['te']))    

#     # Convert the set of dictionaries back to a list of dictionaries
#     unique_data = [dict(item) for item in unique_data]
  
#     #replace any duplicate keys with the new value
#     for i,d in enumerate(unique_data):
#         if d["Name"] == new_data["Name"]:
#             unique_data[i]=new_data
#             break
#     else:
#         unique_data.append(new_data)

#     print (unique_data)
#     #convert the final list to dictionary
#     file_data = {intents:unique_data}

#     # Write the modified data back to the JSON file
#     with open('sample.json', 'w') as file:
#         json.dump(file_data, file, indent=4)


#     # with open(filename,'r+') as file:

#     #       # First we load existing data into a dict.
#     #     file_data = json.load(file)

#     #     # Join new_data with file_data inside emp_details
#     #     file_data["te"].append(new_data)

#     #     #remove duplicate
#     #     # convert the list of dictionaries to a set of dictionaries
#     #     # this will remove any duplicates
#     #     unique_data = list(set(tuple(item.items()) for item in file_data["te"]))

#     #     # convert the set of dictionaries back to a list of dictionaries
#     #     unique_data = [dict(item) for item in unique_data]


#     #     # unique = { each['Name'] : each for each in file_data["te"] }.values()
#     #     # for key,val in file_data["te"].items():
#     #     #     if 


#     #     # Sets file's current position at offset.
#     #     file.seek(0)

#     #     # convert back to json.
#     #     json.dump(file_data, file, indent = 4)
 
#     # python object to be appended
#     # y = {"tag":"Nikhil",
#     #     "patterns": "nikhil@geeksforgeeks.org",
#     #     "responses": "Full Time",
#     #     "context_set":""
#     #     }
     
# new_data = {"Name":"sample", "phone":"works"}
# # new_data = {'Name': 'Bala1', 'phone': 'None'}


# write_json(new_data)

