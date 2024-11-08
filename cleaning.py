import re
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk

# Download NLTK stopwords if not already available
nltk.download('stopwords')
nltk.download('punkt')

# Load data
data = pd.read_csv("analytics_vidhya_courses.csv")

# Define stopwords
stop_words = set(stopwords.words('english'))

def clean_text(text):
    # Convert any non-string to an empty string
    if not isinstance(text, str):
        text = ""
    
    # Remove special characters and extra spaces
    text = re.sub(r'\W+', ' ', text)  # Replaces non-alphanumeric characters with space
    text = re.sub(r'\s+', ' ', text).strip()  # Remove multiple spaces and trim text
    
    # Convert to lowercase
    text = text.lower()
    
    # Tokenize and remove stop words
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word not in stop_words]
    
    # Join tokens back to a single string
    return ' '.join(tokens)

# Apply cleaning to relevant columns, with handling for potential NaN values
data['Title'] = data['Title'].apply(clean_text)
data['Reviews'] = data['Reviews'].apply(lambda x: clean_text(str(x)))  # Convert reviews to string if numeric
data['Lesson Count'] = data['Lesson Count'].apply(clean_text)
data['Price'] = data['Price'].apply(clean_text)

print("Data after cleaning:")
print(data.head())

from nltk.tokenize import word_tokenize

# Tokenize the 'Title' and 'Reviews' columns
data['Title_Tokens'] = data['Title'].apply(word_tokenize)
data['Reviews_Tokens'] = data['Reviews'].apply(word_tokenize)

print("Tokenized Data:")
print(data[['Title_Tokens', 'Reviews_Tokens']].head())

# Save the cleaned, tokenized, and summarized data
data.to_csv("preprocessed_analytics_vidhya_courses.csv", index=False)
data.to_json("preprocessed_analytics_vidhya_courses.json", orient="records", lines=True)

print("Preprocessed data saved successfully.")
