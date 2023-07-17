# kdp-gpt
An open-source python script that can generate books using ChatGPT to be listed on Amazon KDP. The script will ask you for a title and description for the book, as well as the tone and how many chapters you want to include; a pdf file will then be generated.

## Setup
1. Navigate to https://platform.openai.com/account/api-keys to generate an API key
2. Create a .env file and add your key
```
OPENAI_API_KEY=...
```
3. Create python virtual environment, this could be done in many ways but I prefer using venv
```bash
python3 -m venv .venv
```
4. Install requirements.txt
```bash
pip install -r requirements.txt
```

## Usage
```bash
python3 main.py
```
