import pandas as pd
import numpy as np
import ast
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import tkinter as tk
from tkinter import messagebox

nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)
nltk.download('stopwords', quiet=True)

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def lemmatize_and_clean(text):
    words = text.lower().split()
    return ' '.join([lemmatizer.lemmatize(word) for word in words if word.isalpha() and word not in stop_words])

def load_data():
    metadata = pd.read_csv("data/movies_metadata.csv", low_memory=False)
    keywords = pd.read_csv("data/keywords.csv")

    metadata = metadata.dropna(subset=['overview', 'id', 'title', 'vote_count'])
    metadata = metadata[metadata['id'].apply(lambda x: x.isnumeric())]
    metadata['id'] = metadata['id'].astype(int)
    metadata['vote_count'] = metadata['vote_count'].astype(float)

    keywords['id'] = keywords['id'].astype(int)
    keywords['keywords'] = keywords['keywords'].fillna('[]').apply(ast.literal_eval)
    keywords['keywords'] = keywords['keywords'].apply(lambda x: [d['name'] for d in x if 'name' in d])

    merged = pd.merge(metadata, keywords, on='id')
    merged = merged[merged['vote_count'] > 500].reset_index(drop=True)

    # Apply NLTK lemmatization and stopword removal
    merged['overview_lemmatized'] = merged['overview'].apply(lemmatize_and_clean)
    merged['keywords_cleaned'] = merged['keywords'].apply(lambda x: ' '.join([word.lower() for word in x if word.lower() not in stop_words]))

    merged['combined_text'] = merged['overview_lemmatized'] + ' ' + merged['keywords_cleaned']

    # Export to CSV
    merged[['id', 'title', 'combined_text', 'vote_count']].to_csv("movies_metadata_lemmatized_nltk.csv", index=False)

    return merged

def build_similarity(df):
    tfidf = TfidfVectorizer(stop_words='english')
    matrix = tfidf.fit_transform(df['combined_text'])
    return cosine_similarity(matrix, matrix)

def get_recommendations(title, df, sim):
    indices = pd.Series(df.index, index=df['title'].str.lower()).drop_duplicates()
    title = title.lower()
    if title not in indices:
        return None
    idx = indices[title]
    scores = list(enumerate(sim[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)[1:11]
    return df['title'].iloc[[i[0] for i in scores]].tolist()

def search():
    title = entry.get().strip()
    if not title:
        messagebox.showerror("Input Error", "Enter a movie title.")
        return
    results = get_recommendations(title, df, sim)
    listbox.delete(0, tk.END)
    if results:
        for movie in results:
            listbox.insert(tk.END, movie)
    else:
        messagebox.showinfo("Not Found", f"'{title}' not found.")

# Load data
df = load_data()
sim = build_similarity(df)

# Simple UI
root = tk.Tk()
root.title("Movie Recommender")
root.configure(bg="#f0f0f0")

FONT = ("Segoe UI", 11)

tk.Label(root, text="Enter Movie Title:", font=FONT, bg="#f0f0f0").pack(pady=5)
entry = tk.Entry(root, width=50, font=FONT, bd=1, relief="solid")
entry.pack(pady=5)

tk.Button(root, text="Recommend", font=FONT, command=search).pack(pady=5)
listbox = tk.Listbox(root, width=60, height=10, font=FONT, bd=1, relief="solid")
listbox.pack(pady=10)

root.mainloop()
#python recommender.py