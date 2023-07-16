import os
import openai
from dotenv import load_dotenv

# Load env variables from .env file
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

'''
1. Ask the user for a topic, the number of chapters and a tone
2. Ask chatgpt to generate a description for each chaper
3. Ask chatgpt to generate a 500 word chapter in the requested tone
4. Ask DALL-E-2 to generate an image for the chapter, using the first sentence a prompt, combined
   with some context
5. Collate all the text and images into a pdf, also dump them to a file
6. Create a front cover for the book
'''

topic = input('Provide a topic for the book: ')
chapter_count = int(
    input('Provide the number of chapters that the book should contain: '))
tone = input('Provide the tone that the book should be written in: ')
current_messages = []


def send_message(messages):
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        temperature=0,
        messages=messages
    )
    return response


def create_and_send_message(role, content):
    new_message = {'role': role, 'content': content}
    current_messages.append(new_message)
    message_res = send_message(current_messages)
    return message_res


message = create_and_send_message('system', 'You are an expert author')

message = create_and_send_message(
    'user', f'Write a list of {chapter_count} chapters for a book about {topic}, with {tone} tone')

print(message)
