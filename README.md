# Movie-Recommender
Python program that takes a movie title as input and recommends similar movies.
This system outputs 10 movies by analyzing movie summary data and applying different techniques to identify similar keywords and themes.

<p align="center">
  <a href="https://github.com/user-attachments/assets/32d7204c-767c-4dc5-aef0-c8c03be0391b">
    <img src="https://github.com/user-attachments/assets/32d7204c-767c-4dc5-aef0-c8c03be0391b" alt="Application in Use" width="540">
  </a>
</p>

---

# Features

- Recommends 10 similar movies based on a given movie title.
- Handles user input errors gracefully (movie not found).
- Clean Tkinter GUI with simple fonts and styling.
- Uses NLTK for text preprocessing using Lemmatization and Stopword Removal
- Analyzes movie overviews to understand plot and content.
- Searches keywords to identify key themes and topics for better recommendations.

---

# How It Works

1. Data Loading and Cleaning
   - Merges movies_metadata.csv and keywords.csv.
   - Removes movies with missing information or fewer than 500 votes.
   - Preprocesses text by lemmatizing and removing stopwords.
2. Feature Extraction
   - Combines movie overview and keywords into a single text feature.
   - Converts text to TF-IDF vectors.
3. Similarity Calculation
   - Uses cosine similarity between TF-IDF vectors to find similar movies.
4. Recommendation
   - Finds the most similar movies to the input title based on similarity value results.
   - Returns a list of 10 movies in descending order of similarity.

---

# Dependencies

- Python 3.x
- Pandas
- NumPy
- NLTK
- scikit-learn
- Tkinter

---

# Dataset

This project uses the `movies_metadata.csv` and `keywords.csv` datasets from [Kaggle - The Movies Dataset](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset).  
Download the datasets and place the CSV files in a folder named `data/` before running the program.

---

# Notes

- The system relies on movie overviews and keywords, so movies without overviews or keywords will not appear in recommendations.
- Only considers movies with more than 500 votes to avoid obscure or low-quality results.
