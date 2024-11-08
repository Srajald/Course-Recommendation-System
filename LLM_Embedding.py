from sentence_transformers import SentenceTransformer
import pandas as pd
import numpy as np

# Load your preprocessed data
data = pd.read_csv("preprocessed_analytics_vidhya_courses.csv")

# Initialize the SBERT model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Concatenate the relevant fields for embedding generation
data['text_for_embedding'] = (
    data['Title'].fillna('') + " " +
    data['Title_Tokens'].fillna('')
)

# Generate embeddings for each course
data['embedding'] = data['text_for_embedding'].apply(lambda x: model.encode(x))

# Save the embeddings as a numpy array for easier similarity calculations
data['embedding'] = data['embedding'].apply(lambda x: np.array(x))
print("Embeddings generated and stored.")
data.to_pickle("courses_with_embeddings.pkl")  # Save as a pickle file

from sklearn.metrics.pairwise import cosine_similarity

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
    
    # Return top N results with the selected columns (excluding Short_Description)
    return results.head(top_n)[['Title', 'similarity_score', 'Link']]


# Load data with embeddings if not already loaded
data = pd.read_pickle("courses_with_embeddings.pkl")

# Sample search query
query = "Introduction to Generative AI"
top_results = search_courses(query, data, model, top_n=5, threshold=0.5)

# Display results
print("Top Search Results:")
print(top_results)

def search_courses_with_filters(query, data, model, tags_filter=None, top_n=5, threshold=0.5):
    # Process and embed the query
    query = preprocess_query(query)
    query_embedding = model.encode(query)
    
    # Calculate similarity
    similarities = cosine_similarity([query_embedding], list(data['embedding']))[0]
    data['similarity_score'] = similarities
    
    # Apply tag filter if provided
    if tags_filter:
        data = data[data['Title_Tokens'].str.contains(tags_filter, case=False, na=False)]
    
    # Filter and sort based on similarity
    results = data[data['similarity_score'] >= threshold]
    results = results.sort_values(by='similarity_score', ascending=False)
    
    return results.head(top_n)[['Title', 'similarity_score', 'Link']]

# Filtered search with a tag
query = "Understanding large language models"
tag_filter = "Generative AI"
filtered_results = search_courses_with_filters(query, data, model, tags_filter=tag_filter, top_n=5)

print("Top Filtered Search Results:")
print(filtered_results)
