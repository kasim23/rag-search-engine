import json

file_path = '/Users/omama/Desktop/rag-search-engine/data/movies.json'

def load_movies_data():
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data
#     for movie in data["movies"]:
#         print(f"ID: {movie['id']}")
#         print(f"Title: {movie['title']}")
#         print("-" * 10)
        
# if __name__ == "__main__":
#     load_movies_data()