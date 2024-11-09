# Course_Recomender
This is recommending the best course based on user requirements

Smart Course Search Application  ---   

This application is a Streamlit-based tool for discovering and exploring online courses based on user queries. Leveraging advanced NLP models (SentenceTransformer for initial retrieval and CrossEncoder for reranking), the app allows users to quickly find courses that best match their interests.

The application provides a clean, user-friendly interface with a variety of filters and sorting options, enhancing the course search experience with precise, high-quality recommendations.

Features--

Search by Keywords: Type any keyword or phrase, and the app retrieves relevant courses.

Advanced NLP Models: Uses SentenceTransformers for embedding similarity search and CrossEncoder for reranking, ensuring highly relevant results.

Filters and Sorting Options: Filter courses by tags, and sort them by relevance, rating, price, or lesson count.

Rich UI Design: The app has a modern, dynamic UI with background styling, animations, and a professional layout.

Expandable Details: Click to expand course details, curriculum, and summary for more information on each result.

Table of Contents  -- 

1. Features
2. Demo
3. Installation
4. Usage
5. Customization
6. Acknowledgments
7. Demo


Installation---

1. Prerequisites--

Python 3.8 or higher
Streamlit
Required Python libraries from requirements.txt:
txt
Copy code
streamlit
pandas
numpy
sentence-transformers
scikit-learn


2. Installation Steps---

Clone the Repository:

bash
Copy code
git clone https://github.com/your-username/your-repository-name.git
cd your-repository-name

3. Install Dependencies: Make sure to install all required libraries:

bash
Copy code
pip install -r requirements.txt

4. Download or Create the Data:

This application expects a preprocessed data file named courses_with_embedd.pkl, containing course details and embeddings. Ensure this file is in the project directory.
If you don't have the embeddings, generate them using SentenceTransformer('all-mpnet-base-v2') on the dataset of courses you want to use.

5. Run the Application:

bash
Copy code
streamlit run app.py
Usage

6. Launch the App: Once you run the command, a new browser window/tab will open with the application.

Enter Search Query: In the search bar, type keywords or topics (e.g., "Machine Learning Basics", "AI for Beginners").
Filter by Tags (Optional): Use the dropdown menu to filter results by tags, such as "Generative AI", "Machine Learning", etc.

Sort Results: Choose your preferred sorting option (e.g., Relevance, Rating, Price, Lesson Count).

View Results: Search results will display with each course's details:

Course title, description, similarity score, rating, review count, lesson count, and price.
Links to course pages and expandable sections for curriculum and course summaries.

Expandable Details: Click "Show Course Curriculum" and "Show Course Summary" to see more information on each course.

Customization
This app is highly customizable. Here are a few ways you can modify it:

Change NLP Models:

The app uses SentenceTransformer('all-mpnet-base-v2') for initial retrieval and CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2') for reranking.

To switch models, change the model names in the code:

embedding_model = SentenceTransformer('new-embedding-model')
rerank_model = CrossEncoder('new-cross-encoder-model')
Ensure the models are compatible with sentence-transformers.

Modify Filters and Sorting:

Add or remove tags in the tag_filter dropdown by modifying options in app.py.
Customize sorting logic within the search_courses function.

Adjust UI Styling:

Edit the custom CSS in the app.py file for colors, animations, and layout adjustments.
Background image and text styles can be modified within the CSS.

Additional Features:

Add more filters or sorting criteria (e.g., difficulty level, course language).
Integrate user ratings, course reviews, or other metadata for richer course information.

Acknowledgments---
Streamlit: For providing a fantastic framework to build interactive web applications with minimal code.
Sentence-Transformers: For providing pre-trained NLP models and facilitating easy integration of semantic search.
Cross-Encoder: For enhancing the app's relevance ranking through reranking capabilities.


Author---
Developed by Srajal Dwivedi.

For questions or collaboration requests, feel free to reach out!

Let me know if you need additional sections or have any specific modifications in mind!