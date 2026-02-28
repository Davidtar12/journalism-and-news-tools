import re
import os
import requests
from bs4 import BeautifulSoup
from docx import Document
import textract
from glob import glob

def extract_quotes_from_text(text):
    quotes = re.findall(r'"([^"]{10,})"|“([^”]{10,})”', text)
    return [q[0] or q[1] for q in quotes if q[0] or q[1]]

def process_text_input(text):
    quotes = extract_quotes_from_text(text)
    print("Quotes found:")
    for quote in quotes:
        print(f"- \"{quote}\"")

def read_docx_file(file_path):
    doc = Document(file_path)
    return "\n".join([paragraph.text for paragraph in doc.paragraphs])

def read_doc_file(file_path):
    try:
        return textract.process(file_path).decode()
    except Exception as e:
        print(f"Failed to process .doc file {file_path}: {e}")
        return ""

def process_file_input(file_path):
    if file_path.endswith(".docx"):
        text = read_docx_file(file_path)
    elif file_path.endswith(".doc"):
        text = read_doc_file(file_path)
    else:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
        except Exception as e:
            print(f"Failed to read file {file_path}: {e}")
            return
    process_text_input(text)

def process_url_input(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text(" ", strip=True)
        print(f"Quotes from {url}:")
        process_text_input(text)
    except requests.RequestException as e:
        print(f"Request failed: {e}")

def process_folder_input(folder_path):
    # Define patterns for text, docx, and doc files
    file_patterns = ["*.txt", "*.docx", "*.doc"]
    for pattern in file_patterns:
        for file_path in glob(os.path.join(folder_path, pattern)):
            print(f"Processing {file_path}:")
            process_file_input(file_path)
            print("\n" + "-"*80 + "\n")

if __name__ == "__main__":
    inputs = [
        # Add your inputs here: URLs, local file paths, directly pasted text, or folder paths.
        #"https://example.com/article1",
        #"path/to/document.docx",
        r"H:\My Drive\LatAm\Especiales\2024APmineriacoca",
    ]

    for input_item in inputs:
        if input_item.startswith("http://") or input_item.startswith("https://"):
            process_url_input(input_item)
        elif os.path.isdir(input_item):
            process_folder_input(input_item)
        else:
            process_file_input(input_item)