from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import pandas as pd
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')
def preprocess_query(query):
    
    query = query.lower().strip()
    return query

def search_courses(query, data, model, top_n=5, threshold=0.5):

    query = preprocess_query(query)
    query_embedding = model.encode(query)
    
    similarities = cosine_similarity([query_embedding], list(data['embedding']))[0]
    
    data['similarity_score'] = similarities
    
    results = data[data['similarity_score'] >= threshold]
    results = results.sort_values(by='similarity_score', ascending=False)
    
    return results.head(top_n)[['Title', 'Short_Description', 'similarity_score', 'Link']]

data = pd.read_pickle("courses_with_embeddings.pkl")

query = "Introduction to Generative AI"
top_results = search_courses(query, data, model, top_n=5, threshold=0.5)

print("Top Search Results:")
print(top_results)
