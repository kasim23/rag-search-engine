import os
import pickle
from utils.preprocess import clean_text_of_punctuation
from nltk.stem import PorterStemmer

stemmer = PorterStemmer()

class Document():
    def __init__(self, doc_id, title, description):
        self.id = doc_id
        self.title = title
        self.description = description

class InvertedIndex():
    def __init__(self):
        self.index: dict[str, set[int]] = {}
        self.docmap: dict[int, Document] = {}
        
    def __add_document(self, doc_id, text):
        tokens = set(clean_text_of_punctuation(text).split())
        stemmed_tokens = [stemmer.stem(t) for t in tokens]
        for token in stemmed_tokens:
            if token not in self.index:
                self.index[token] = set()
                
            self.index[token].add(doc_id)
    
    def get_documents(self, term):
        """Retrieves and sorts doc IDs for a single search term."""
        # Preprocess the search term (lowercase and stem)
        stemmed_term = stemmer.stem(term.lower())
        # Retrieve IDs from the index
        # Using .get() prevents a KeyError if the word isn't found
        doc_ids = self.index.get(stemmed_term, set())
        # Return as a list sorted in ascending order
        return sorted(list(doc_ids))
    
    def build(self, movies):
        """Iterates over all movies to fill docmap and index."""
        for m in movies:
            doc_id = int(m['id'])
            doc = Document(doc_id, m['title'], m['description'])
            self.docmap[doc_id] = doc
            
            # Concatenate title and description as the source text
            full_text = f"{doc.title} {doc.description}"
            self.__add_document(doc_id, full_text)
            
    def save(self):
        os.makedirs("cache", exist_ok=True)
        
        with open("cache/index.pkl", "wb") as f:
            pickle.dump(self.index, f)
            
        with open("cache/docmap.pkl", "wb") as f:
            pickle.dump(self.docmap, f)