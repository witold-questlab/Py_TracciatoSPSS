import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os, json, csv, pickle, re, shutil
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

def ensure_csv_exists(csv_file):
    """Ensure the CSV file exists; if not, create it with headers."""
    if not os.path.exists(csv_file):
        os.makedirs(os.path.dirname(csv_file), exist_ok=True)
        with open(csv_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["ascx", "type", "spss"])

def ensure_json_exists(json_file):
    """Ensure the JSON file exists; if not, create it with an empty dict."""
    if not os.path.exists(json_file):
        os.makedirs(os.path.dirname(json_file), exist_ok=True)
        with open(json_file, 'w', encoding='utf-8') as file:
            json.dump({}, file, indent=4)

def extract_fieldset(content):
    """
    Extracts the first <fieldset> ... </fieldset> block from the given content.
    If no fieldset is found, returns the original content.
    """
    match = re.search(r"<fieldset[^>]*>.*?</fieldset>", content, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(0)
    else:
        return content