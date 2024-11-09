from sentence_transformers import SentenceTransformer, CrossEncoder
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

data = pd.read_csv("preprocessed_analytics_vidhya_courses.csv")

embedding_model = SentenceTransformer('all-mpnet-base-v2')  # Use a more accurate embedding model
rerank_model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')  # Cross-encoder for reranking

# Prepare text for embedding generation by concatenating fields
data['text_for_embedding'] = (
    data['Title'].fillna('') + " " +
    data['Description'].fillna('') + " " +
    data['Curriculum'].fillna('')
)

data['embedding'] = data['text_for_embedding'].apply(lambda x: embedding_model.encode(x))

data['embedding'] = data['embedding'].apply(lambda x: np.array(x))
data.to_pickle("courses_with_embedd.pkl")

data = pd.read_pickle("courses_with_embedd.pkl")

def preprocess_query(query):
    """Preprocess the search query."""
    return query.lower().strip()

def search_courses(query, data, embedding_model, rerank_model, top_n=5, threshold=0.5, tags_filter=None):
    """Search courses using a multi-model pipeline with reranking."""
    
    query = preprocess_query(query)
    query_embedding = embedding_model.encode(query)
    similarities = cosine_similarity([query_embedding], list(data['embedding']))[0]
    data['similarity_score'] = similarities

    if tags_filter:
        data = data[data[['Title', 'Description', 'Curriculum']].apply(
            lambda x: x.str.contains(tags_filter, case=False, na=False).any(), axis=1)]
    
    
    top_candidates = data[data['similarity_score'] >= threshold].nlargest(top_n * 2, 'similarity_score')


    pairs = [[query, candidate] for candidate in top_candidates['Title']]
    rerank_scores = rerank_model.predict(pairs)
    top_candidates['rerank_score'] = rerank_scores


    final_results = top_candidates.nlargest(top_n, 'rerank_score')
    return final_results[['Title', 'similarity_score', 'rerank_score', 'Link']]

query = "Introduction to Generative AI"
top_results = search_courses(query, data, embedding_model, rerank_model, top_n=5, threshold=0.5)

print("Top Search Results:")
print(top_results)


tag_filter = "Generative AI"
filtered_results = search_courses(query, data, embedding_model, rerank_model, top_n=5, threshold=0.5, tags_filter=tag_filter)

print("Top Filtered Search Results:")
print(filtered_results)

