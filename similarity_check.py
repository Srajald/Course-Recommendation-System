from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import pandas as pd
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')
def preprocess_query(query):
    # Clean the query (similar to how we cleaned the data)
    # This could include converting to lowercase, removing punctuation, etc.
    query = query.lower().strip()
    return query

def search_courses(query, data, model, top_n=5, threshold=0.5):
    # Preprocess and embed the query
    query = preprocess_query(query)
    query_embedding = model.encode(query)
    
    # Calculate cosine similarity between the query and each course embedding
    similarities = cosine_similarity([query_embedding], list(data['embedding']))[0]
    
    # Add similarities to the DataFrame
    data['similarity_score'] = similarities
    
    # Filter and sort results based on similarity score
    results = data[data['similarity_score'] >= threshold]
    results = results.sort_values(by='similarity_score', ascending=False)
    
    # Return top N results
    return results.head(top_n)[['Title', 'Short_Description', 'similarity_score', 'Link']]

# Load data with embeddings if not already loaded
data = pd.read_pickle("courses_with_embeddings.pkl")

# Sample search query
query = "Introduction to Generative AI"
top_results = search_courses(query, data, model, top_n=5, threshold=0.5)

# Display results
print("Top Search Results:")
print(top_results)
