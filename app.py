import streamlit as st
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load preprocessed data with embeddings
data = pd.read_pickle("courses_with_embeddings.pkl")

# Load the pre-trained SBERT model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Define the search function
def preprocess_query(query):
    return query.lower().strip()

def search_courses(query, data, model, tag_filter=None, top_n=5, threshold=0.5):
    query = preprocess_query(query)
    query_embedding = model.encode(query)
    similarities = cosine_similarity([query_embedding], list(data['embedding']))[0]
    data['similarity_score'] = similarities
    
    if tag_filter:
        data = data[data['Title_Tokens'].str.contains(tag_filter, case=False, na=False)]
    
    results = data[data['similarity_score'] >= threshold]
    results = results.sort_values(by='similarity_score', ascending=False)
    
    return results.head(top_n)[['Title', 'similarity_score', 'Link']]

# Streamlit UI Components
st.title("Course Search Tool")
st.write("Enter a query to search for relevant courses:")

# Search Box
query = st.text_input("Search for courses", "")

# Optional Tag Filter
tag_filter = st.selectbox("Filter by Tokens (optional)", options=["", "Generative AI", "Machine Learning", "Data Science"])

# Search Button
if st.button("Search"):
    if query:
        results = search_courses(query, data, model, tag_filter=tag_filter)
        if len(results) > 0:
            st.write("### Search Results")
            for idx, row in results.iterrows():
                st.write(f"**{row['Title']}**")
                st.write(f"Similarity Score: {row['similarity_score']:.2f}")
                st.write(f"[Course Link]({row['Link']})")
                st.write("---")
        else:
            st.write("No results found. Try a different query.")
    else:
        st.write("Please enter a query to search.")
