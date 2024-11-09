import streamlit as st
import pandas as pd
from sentence_transformers import SentenceTransformer, CrossEncoder
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

data = pd.read_pickle("courses_with_embedd.pkl")

embedding_model = SentenceTransformer('all-mpnet-base-v2')  # Better embedding model for initial retrieval
rerank_model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')  # Cross-encoder for reranking

def preprocess_query(query):
    return query.lower().strip()

def highlight_keywords(description, query):
    return description 

def search_courses(query, data, embedding_model, rerank_model, tag_filter=None, top_n=5, threshold=0.5):
    query = preprocess_query(query)
    query_embedding = embedding_model.encode(query)
    
 
    similarities = cosine_similarity([query_embedding], list(data['embedding']))[0]
    data['similarity_score'] = similarities

    if tag_filter:
        data = data[data['Title_Tokens'].str.contains(tag_filter, case=False, na=False)]
    
   
    top_candidates = data[data['similarity_score'] >= threshold].nlargest(top_n * 2, 'similarity_score')

    
    pairs = [[query, candidate] for candidate in top_candidates['Title']]
    rerank_scores = rerank_model.predict(pairs)
    top_candidates['rerank_score'] = rerank_scores

    
    final_results = top_candidates.nlargest(top_n, 'rerank_score')
    return final_results[['Title', 'similarity_score', 'rerank_score', 'Description', 'Link', 'Rating', 'Reviews', 'Lesson Count', 'Price', 'Curriculum', 'Course_Summary']]


st.markdown(f"""
    <style>
        .stApp {{
            background: url("/static/new_wal.jpg");
            background-size: cover;
            background-position: center;
        }}
        .title-text {{
            font-size: 50px;
            font-weight: bold;
            text-align: center;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
            background: linear-gradient(90deg, #4CAF50, #8BC34A);
            background-clip: text;
            -webkit-background-clip: text;
            color: transparent;
            animation: subtle-glow 2s infinite alternate;
        }}
        @keyframes subtle-glow {{
            from {{
                text-shadow: 0 0 5px #4CAF50, 0 0 10px #8BC34A;
            }}
            to {{
                text-shadow: 0 0 8px #4CAF50, 0 0 15px #8BC34A;
            }}
        }}
        .subtitle-text {{
            font-size: 22px;
            color: #dcdcdc;
            margin-bottom: 20px;
            text-align: center;
        }}
        .results-container {{
            padding: 15px;
            background-color: #1e1e1e;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }}
        .result-title {{
            font-size: 25px;
            font-weight: bold;
            background: linear-gradient(90deg, #4CAF50, #8BC34A);
            background-clip: text;
            -webkit-background-clip: text;
            color: transparent;
        }}
        .result-description {{
            font-size: 16px;
            color: #d3d3d3;
            margin-bottom: 10px;
        }}
        .course-info {{
            font-size: 15px;
            color: #f0f0f0;
            margin-bottom: 5px;
        }}
        .course-rating {{
            font-size: 15px;
            color: #FFD700;
            margin-bottom: 5px;
        }}
        .similarity-score {{
            font-size: 15px;
            color: #ff6347;
            margin-bottom: 5px;
        }}
        .link-style {{
            color: #007acc;
            text-decoration: none;
            font-weight: bold;
        }}
        .link-style:hover {{
            text-decoration: underline;
        }}
        ul {{
            color: #d3d3d3;
            padding-left: 20px;
        }}
        .footer-text {{
            text-align: center;
            font-size: 16px;
            color: #ffffff;
            margin-top: 20px;
            font-weight: 500;
        }}
    </style>
""", unsafe_allow_html=True)


st.markdown("<div class='title-text'>✨ Smart Search Tool 🔍</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle-text'>Find the best courses that match your interests and skills, now with ease and style!</div>", unsafe_allow_html=True)


query = st.text_input("Enter keywords to search for courses:", "")
tag_filter = st.selectbox("Filter by Tags (optional)", options=["", "Generative AI", "Machine Learning", "Data Science", "Natural Language Processing", "Deep Learning"])
sort_option = st.selectbox("Sort by", ["Relevance", "Rating", "Price", "Lesson Count"])

st.markdown("**Popular Searches**: Machine Learning Basics, AI for Beginners, Deep Learning Fundamentals")
st.markdown("---")


if st.button("Search"):
    if query:
        
        results = search_courses(query, data, embedding_model, rerank_model, tag_filter=tag_filter)
        
        if len(results) > 0:
            st.markdown("<div class='results-container'><h3>Search Results</h3>", unsafe_allow_html=True)
            for idx, row in results.iterrows():
               
                st.markdown(f"<div class='result-title'>{row['Title']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='similarity-score'>Similarity Score: {row['similarity_score']:.2f}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='result-description'>{row['Description']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='course-rating'>Rating: {row['Rating']} ⭐️ ({row['Reviews']} reviews)</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='course-info'>Lesson Count: {row['Lesson Count']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='course-info'>Price: {row['Price']}</div>", unsafe_allow_html=True)
                st.markdown(f"<a href='{row['Link']}' class='link-style' target='_blank'>🔗 Course Link</a>", unsafe_allow_html=True)
                
                
                with st.expander("Show Course Curriculum"):
                    curriculum_points = row['Curriculum'].split('\n')
                    st.markdown("<ul>", unsafe_allow_html=True)
                    for point in curriculum_points:
                        if point.strip():  
                            st.markdown(f"<li>{point.strip()}</li>", unsafe_allow_html=True)
                    st.markdown("</ul>", unsafe_allow_html=True)
                
               
                with st.expander("Show Course Summary"):
                    st.markdown(f"<div>{row['Course_Summary']}</div>", unsafe_allow_html=True)

                st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.warning("No results found. Try a different query.")
    else:
        st.error("Please enter a query to search.")


st.markdown("---")
st.markdown("<div class='footer-text'>Made by Srajal Dwivedi</div>", unsafe_allow_html=True)

