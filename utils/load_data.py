import json

file_path = '/Users/omama/Desktop/rag-search-engine/data/movies.json'
stop_words_file = '/Users/omama/Desktop/rag-search-engine/data/stopwords.txt'

def load_movies_data():
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def read_stop_words():
    with open(stop_words_file, 'r', encoding='utf-8') as file:
        words = file.read()
    return set(words.split())