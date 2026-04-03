import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

import argparse
from utils.load_data import load_movies_data, read_stop_words
from utils.preprocess import clean_text_of_punctuation
from nltk.stem import PorterStemmer

def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using BM25")
    search_parser.add_argument("query", type=str, help="Search query")

    args = parser.parse_args()
    
    stemmer = PorterStemmer()

    res = []
    match args.command:
        case "search":
            # print the search query here
            print(f"Searching for: {args.query}")
            
            data = load_movies_data()
            stop_words = read_stop_words()
            query_tokens = set(clean_text_of_punctuation(args.query).split())
            
            filtered_query = [t for t in query_tokens if t.lower() not in stop_words]
            stemmed_query = [stemmer.stem(t) for t in filtered_query]
            
            for movie in data.get("movies", []):
                title_tokens = set(clean_text_of_punctuation(movie.get('title', '')).split())
                filtered_tokens = [t for t in title_tokens if t.lower() not in stop_words]
                stemmed_tokens = [stemmer.stem(t) for t in filtered_tokens]
                
                match_found = any(
                    q_token in t_token
                    for q_token in stemmed_query
                    for t_token in stemmed_tokens
                )
                if match_found:
                    res.append(movie)
            
            sorted_res = sorted(res, key=lambda movie: int(movie['id']))
            for i, movie in enumerate(sorted_res[:5], 1):
                print(f"{i}. {movie['title']}")
    
        case _:
            parser.print_help()
            

if __name__ == "__main__":
    main()