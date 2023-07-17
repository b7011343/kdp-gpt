import os
import openai
from dotenv import load_dotenv
from reportlab.pdfgen import canvas

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

# User input
topic = input('Provide a topic for the book: ')
chapter_count = int(
    input('Provide the number of chapters that the book should contain: '))
tone = input('Provide the tone that the book should be written in: ')
current_messages = []
book_chapters = []


def send_message(messages):
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        temperature=0,
        messages=messages
    )
    return response.choices[0].message.content


def create_and_send_message(role, content):
    new_message = {'role': role, 'content': content}
    current_messages.append(new_message)
    message_res = send_message(current_messages)
    return message_res


def create_image():
    return None


# Init chatgpt
create_and_send_message('system', 'You are an expert author')

# Generate a list of chapters
chapter_descs = create_and_send_message(
    'user', f'Write a list of {chapter_count} chapters for a book about {topic}, with {tone} tone').split('\n\n')

# Generate chapter texts
for i in range(chapter_count):
    chapter_no = i + 1
    chapter_text = create_and_send_message(
        'user', f'Write chapter {chapter_no} in 500 words')
    # TODO: Generate illustration and add to book chapters
    book_chapters.append(chapter_text)


print(chapter_descs)
print('\n')
print(book_chapters)

# Generate pdf file
# TODO: Fix this so that words don't wrap
pdf_canvas = canvas.Canvas('books/book.pdf')
for chapter in book_chapters:
    pdf_canvas.drawString(100, 750, chapter)
    pdf_canvas.save()
