import os
import re
import json

def insert_line_breaks(text, max_length=50):
    """ Inserts <br> into the text if a line exceeds max_length, ensuring no words are split. """
    words = text.split()
    line = ""
    formatted_text = ""

    for word in words:
        if len(line) + len(word) + 1 > max_length:
            formatted_text += line.strip() + "<br>"
            line = word + " "
        else:
            line += word + " "

    formatted_text += line.strip()
    return formatted_text


def load_all_data(path, sort_before=False):

    file_names = os.listdir(path)
    if sort_before:
        file_names = sorted(
            [f for f in os.listdir(path) if f.endswith('.json')],
            key=lambda x: int(re.search(r'\d+', x).group())
        )

    files = []

    for filename in file_names:
        if filename.endswith(".json"):
            file_path = os.path.join(path, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    temp = {
                        'filename': filename,
                        'programs': data
                    }
                    files.append(temp)
            except:
                print("Failed")

    return files


def get_by_id(data, key):
    for d in data:
        if d['programs']['offspring']['offspring_id'] == key:
            return d

