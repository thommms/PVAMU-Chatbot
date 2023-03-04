import openai
import openai_secret_manager

# Set up your OpenAI API key
assert "openai" in openai_secret_manager.get_services()
secrets = openai_secret_manager.get_secret("openai")

openai.api_key = secrets["api_key"]
model_engine = "davinci"

# Define a function to generate a response using GPT-3
def generate_response(prompt):
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = response.choices[0].text.strip()
    return message

# Define a function to handle user input and generate a response
def chatbot():
    print("Hello, I'm a chatbot. How can I help you?")
    while True:
        user_input = input("> ")
        if user_input.lower() in ["bye", "goodbye"]:
            print("Goodbye!")
            break
        prompt = f"User: {user_input}\nChatbot:"
        response = generate_response(prompt)
        print(response)

# Call the chatbot function to start the conversation
chatbot()



# import openai
# import json
# import os

# # Set up your OpenAI API key
# openai.api_key = os.getenv("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")

# # Define a function to generate a response using GPT-3
# def generate_response(prompt):
#     response = openai.api.Completion.create(
#         engine="text-davinci-003",
#         prompt=prompt,
#         max_tokens=1024,
#         n=1,
#         stop=None,
#         temperature=0.5,
#     )

#     message = response.choices[0].text.strip()
#     return message

# # Define a function to handle user input and generate a response
# def chatbot():
#     print("Hello, I'm a chatbot. How can I help you?")
#     while True:
#         user_input = input("> ")
#         if user_input.lower() in ["bye", "goodbye"]:
#             print("Goodbye!")
#             break
#         prompt = f"User: {user_input}\nChatbot:"
#         response = generate_response(prompt)
#         print(response)

# # Call the chatbot function to start the conversation
# chatbot()
