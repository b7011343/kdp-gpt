import os
import openai
import urllib.request
import json
from dotenv import load_dotenv
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER

# Load env variables from .env file
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

# Message history to maintain conversation context
current_messages = []

# List of chapters and corresponding images
book_chapters = []

# User input
title = input('Provide a title for the book: ')
description = input('Provide a description for the book: ')
tone = input('Provide the tone that the book should be written in: ')
chapter_count = int(
    input('Provide the number of chapters that the book should contain: '))


def send_message(messages: list):
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        temperature=0,
        messages=messages
    )
    return response.choices[0].message.content


def create_and_send_message(role: str, content: str):
    new_message = {'role': role, 'content': content}
    current_messages.append(new_message)
    message_res = send_message(current_messages)
    return message_res


def download_url(image_url: str, file_name: str, max_retries: int):
    if max_retries == 0:
        raise Exception('Max download attempts reached')
    try:
        urllib.request.urlretrieve(image_url, file_name)
    except ValueError:
        download_url(image_url, file_name, max_retries - 1)


def create_image(prompt: str, chapter_index: int):
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size='900x720',
    )
    image_url = response['data'][0]['url']
    file_name = f'output/{chapter_index}.png'
    download_url(image_url, file_name, 5)
    return file_name


# Provide chatgpt context
create_and_send_message('system', 'You are an expert author')

# Generate a list of chapters
print('Generating chapters')
chapter_descs = create_and_send_message(
    'user', f'Write a list of {chapter_count} chapters for a book called {title}, about {description}, with {tone} tone').split('\n\n')
it = iter(chapter_descs)
chapter_descs = [f'{x}{y}' for x, y in zip(it, it)]

# Generate chapter texts
for i in range(chapter_count):
    chapter_no = i + 1
    print(f'Generating chapter {chapter_no}/{chapter_count}')
    chapter_text = create_and_send_message(
        'user', f'Write chapter number {chapter_no} in at least 500 words')
    prompt = chapter_descs[i]
    chapter_image = create_image(prompt, i)
    book_chapter = {
        'text': chapter_text,
        'image': chapter_image,
    }
    book_chapters.append(book_chapter)

# Dump raw data
with open('output/raw_book_data.json', 'w') as final:
    json.dump(book_chapters, final)

# Generate pdf file
# TODO: Fix this so that words don't wrap https://docs.reportlab.com/reportlab/userguide/ch1_intro/
print('Generating book pdf')
pdf_file_name = title.replace(' ', '')
pdf = canvas.Canvas(f'output/{pdf_file_name}.pdf')
pdf.setTitle(title)

title_style = ParagraphStyle('title')
title_style.textColor = 'black'
title_style.borderColor = 'black'
title_style.borderWidth = 1
title_style.alignment = TA_CENTER
title_style.leading = 120
title_style.fontSize = 50

chapter_style = ParagraphStyle('chapter')
chapter_style.textColor = 'black'
chapter_style.borderColor = 'black'
chapter_style.borderWidth = 1
chapter_style.alignment = TA_CENTER
chapter_style.leading = 120
chapter_style.fontSize = 28

body_style = ParagraphStyle('body')
body_style.textColor = 'black'
body_style.borderColor = 'black'
body_style.borderWidth = 1
body_style.alignment = TA_CENTER
body_style.leading = 120
body_style.fontSize = 14

for chapter in book_chapters:
    paragraphs = chapter.split('\n\n')
    chapter_title = paragraphs[0]
    paragraphs.pop(0)
    # TODO: Add chapter title to page with chapter para style
    # TODO: Add each remaining paragraph with body para style
