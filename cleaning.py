import re
import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from urllib.parse import urlparse

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')


data = pd.read_csv("updated_courses_with_details.csv")

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def clean_text(text):
    """General text cleaning function"""
    if not isinstance(text, str):
        return ""
    
    text = re.sub(r'http\S+|www\S+', '', text)  # Remove URLs
    text = re.sub(r'\d+', '', text)             # Remove numbers
    text = re.sub(r'\W+', ' ', text)            # Remove special characters
   
    text = text.lower()
    tokens = word_tokenize(text)
    
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]
    
    return ' '.join(tokens)

def process_url(url):
    """Extracts the domain from URLs for simplicity"""
    if isinstance(url, str):
        parsed_url = urlparse(url)
        return parsed_url.netloc
    return url

def clean_price(price):
    """Processes price information, removes any special characters, and converts to a standard format"""
    if isinstance(price, str):
        price = re.sub(r'[^\d.]', '', price)  
    return price if price else "0.0"  

def clean_numeric(value):
    """Cleans numeric fields to ensure consistency"""
    if isinstance(value, str):
        value = re.sub(r'\D', '', value)  
    return value if value else "0"  

data['Title'] = data['Title'].apply(clean_text)
data['Reviews'] = data['Reviews'].apply(lambda x: clean_text(str(x)))
data['Lesson Count'] = data['Lesson Count'].apply(clean_numeric)
data['Price'] = data['Price'].apply(clean_price)
data['Image URL'] = data['Image URL'].apply(process_url)
data['Description'] = data['Description'].apply(clean_text)
data['Curriculum'] = data['Curriculum'].apply(clean_text)

data['Title_Tokens'] = data['Title'].apply(word_tokenize)
data['Reviews_Tokens'] = data['Reviews'].apply(word_tokenize)
data['Description_Tokens'] = data['Description'].apply(word_tokenize)
data['Curriculum_Tokens'] = data['Curriculum'].apply(word_tokenize)


data['Course_Summary'] = data.apply(
    lambda x: f"{x['Title']} {x['Description']} {x['Curriculum']}", axis=1
)


data['Title_Token_Count'] = data['Title_Tokens'].apply(len)
data['Description_Token_Count'] = data['Description_Tokens'].apply(len)
data['Curriculum_Token_Count'] = data['Curriculum_Tokens'].apply(len)


print("Data after advanced cleaning and processing:")
print(data[['Title', 'Reviews', 'Lesson Count', 'Price', 'Image URL', 'Description', 'Curriculum']].head())
print("Tokenized and summarized columns:")
print(data[['Title_Tokens', 'Reviews_Tokens', 'Description_Tokens', 'Curriculum_Tokens', 'Course_Summary']].head())


data.to_csv("preprocessed_analytics_vidhya_courses.csv", index=False)
data.to_json("preprocessed_analytics_vidhya_courses.json", orient="records")

print("Preprocessed data saved successfully.")

