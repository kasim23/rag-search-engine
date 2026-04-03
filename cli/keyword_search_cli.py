import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

import argparse
from utils.load_data import load_movies_data

def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using BM25")
    search_parser.add_argument("query", type=str, help="Search query")

    args = parser.parse_args()

    res = []
    match args.command:
        case "search":
            # print the search query here
            print(f"Searching for: {args.query}")
            
            data = load_movies_data()
            
            
            for movie in data.get("movies", []):
                if args.query.lower() in movie.get('title', '').lower():
                    res.append(movie)
            
            sorted_res = sorted(res, key=lambda movie: int(movie['id']))
            for i, movie in enumerate(sorted_res[:5], 1):
                print(f"{i}. {movie['title']}")
    
        case _:
            parser.print_help()
            

if __name__ == "__main__":
    main()