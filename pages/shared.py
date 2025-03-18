import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os, json, csv, pickle, re, shutil, sys, platform
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
    
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temporary folder and stores path in _MEIPASS.
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def get_persistent_data_path():
    """
    Returns a persistent folder path for data files.
    On Windows, this might be in %APPDATA%\MyApp.
    On macOS/Linux, a hidden folder in the user's home directory.
    """
    if platform.system() == "Windows":
        base = os.getenv("APPDATA")
        data_dir = os.path.join(base, "PY_TracciatoSPSS")  # Change "MyApp" to your app's name.
    else:
        data_dir = os.path.join(os.path.expanduser("~"), ".myapp")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    return data_dir

def initialize_file(filename):
    """
    Checks if the file exists in the persistent location.
    If not, copies it from the bundled resource.
    """
    persistent_path = os.path.join(get_persistent_data_path(), filename)
    if not os.path.exists(persistent_path):
        bundled_path = resource_path(f"data/{filename}")
        # Copy only if the bundled file exists.
        if os.path.exists(bundled_path):
            shutil.copy2(bundled_path, persistent_path)
    return persistent_path

option_dropdown = ["altro", "radio", "sino & co", "checklist", "matrice", "textlist", "matrice verticale", "matrice primosecondo", "rating", "matrice rating"]

translations = {
    "en": {
        "main_title": "SPSS Generator",
        "train_title": "Train",
        "generate_title": "Generate",
        "update_title": "Update",
        "settings_title": "Settings",
        "generate_spss_title": "Generate SPSS File",
        "generate_spss_1": "Browse ASCX Folder",
        "generate_spss_2": "No folder selected",
        "generate_spss_3": "Generate SPSS",
        "generate_spss_4": "Folder selected.",
        "generate_spss_5": "No folder selected.",
        "generate_spss_6": "Model file not found. Please train the model first.",
        "generate_spss_7": "Model loaded successfully.",
        "generate_spss_8": "Error loading model:",
        "generate_spss_9": "Prediction error:",
        "generate_spss_10": "Please select an ASCX folder first.",
        "generate_spss_11": "Model not loaded. Cannot generate predictions.",
        "generate_spss_12": "Select output folder for spss.txt",
        "generate_spss_13": "No output folder selected for spss.txt.",
        "generate_spss_14": "Error reading",
        "generate_spss_15": "Error writing spss.txt:",
        "generate_spss_16": "Error writing CSV:",
        "generate_spss_17": "Error writing JSON:",
        "generate_spss_18": "Generation complete. Files created:\n",
        "choose_language": "Choose Language:",
        "import_model": "Import Model",
        "export_model": "Export Model",
        "settings_1": "Select Model File",
        "settings_2": "Model imported successfully.",
        "settings_3": "Error importing model:",
        "settings_4": "No file selected for import.",
        "settings_5": "Select Export Folder",
        "settings_6": "Model exported successfully to",
        "settings_7": "Error exporting model:",
        "settings_8": "No folder selected for export.",
        "train_1": "Train AI using existing data",
        "train_2": "Browse ASCX File",
        "train_3": "No file selected",
        "train_4": "Add record",
        "train_5": "Train model",
        "train_6": "ASCX file loaded successfully.",
        "train_7": "Error reading file:",
        "train_8": "No file selected.",
        "train_9": "Please browse and select an ASCX file first.",
        "train_10": "Please fill in both the Type and SPSS fields.",
        "train_11": "Error updating CSV:",
        "train_12": "Error loading JSON data:",
        "train_13": "Error updating JSON:",
        "train_14": "added to CSV and JSON.",
        "train_15": "Error reading",	
        "train_16": "Training data is empty.",
        "train_17": "Error loading existing model:",
        "train_18": "No new training examples found. Model not updated.",
        "train_19": "Training complete. Model saved as",
        "update_1": "Update Training Model",
        "update_2": "Error loading generated data:",
        "update_3": "Previous",
        "update_4": "Next",
        "update_5": "ASCX Content:",
        "update_6": "SPSS Equivalent:",
        "update_7": "Update Record",
        "update_8": "Update Model",
        "update_9": "Already at the first record.",
        "update_10": "Already at the last record.",
        "update_11": "All fields must be filled before updating.",
        "update_12": "Error updating training CSV:",
        "update_13": "Error reading training JSON:",
        "update_14": "Error updating training JSON:",
        "update_15": "Error updating generated JSON:",
        "update_16": "Record updated and added as ID",
        "update_17": "All generated records have been processed.",
        "update_18": "Error reading training JSON for model update:",
        "update_19": "Training data incomplete, model not updated.",
        "update_20": "Model updated successfully.",
        "update_21": "Error saving updated model:",
        "update_22": "No generated records to update.",
        "update_type": "Type",
        "selected_language": "The language selected will be applied after restarting the application."


    },
    "it": {
        "main_title": "Creazione Tracciato SPSS",
        "train_title": "Allena",
        "generate_title": "Genera",
        "update_title": "Aggiorna",
        "settings_title": "Impostazioni",
        "generate_spss_title": "Generate SPSS File",
        "generate_spss_1": "Sfoglia Cartella ASCX",
        "generate_spss_2": "Nessuna cartella selezionata",
        "generate_spss_3": "Genera SPSS",
        "generate_spss_4": "Cartella selezionata",
        "generate_spss_5": "Nessuna cartella selezionata.",
        "generate_spss_6": "Modello non trovato, per favore allenare prima il modello.",
        "generate_spss_7": "Modello caricato con successo.",
        "generate_spss_8": "Errore nel caricamento del modello:",
        "generate_spss_9": "Errore nella predizione:",
        "generate_spss_10": "Per favore, prima selezionare una cartella ASCX",
        "generate_spss_11": "Modello non caricato. Impossibile generare predizioni.",
        "generate_spss_12": "Selezionare una cartella di output per il file spss.txt",
        "generate_spss_13": "Nessuna cartella di output selezionata per il file spss.txt.",
        "generate_spss_14": "Errore nella lettura",
        "generate_spss_15": "Errore nella scrittura di spss.txt:",
        "generate_spss_16": "Errore nella scrittura del CSV:",
        "generate_spss_17": "Errore nella scrittura del JSON:",
        "generate_spss_18": "Generazione completata. File creati:\n",
        "choose_language": "Selezionare una lingua:",
        "import_model": "Importare il Modello",
        "export_model": "Esportare il Modello",
        "settings_1": "Selezionare il file Modello",
        "settings_2": "Modello importato con successo.",
        "settings_3": "Errore nell'importazione del modello:",
        "settings_4": "Nessun file selezionato per l'import.",
        "settings_5": "Selezionare la cartella per l'esportazione",
        "settings_6": "Modello esportato con successo in",
        "settings_7": "Errore nell'esportazione del modello:",
        "settings_8": "Nessuna cartella selezionata per l'esportazione.",
        "train_1": "Allenare l'IA con dati esistenti",
        "train_2": "Selezionare file ASCX",
        "train_3": "Nessuna file selezionato",
        "train_4": "Aggiungi record",
        "train_5": "Allena il modello",
        "train_6": "File ASCX caricato con successo.",
        "train_7": "Errore nella lettura del file:",
        "train_8": "Nessun file selezionato.",
        "train_9": "Per favore, prima sfogliare e selezionare un file ASCX.",
        "train_10": "Per favore, riempire entrambi i campi Tipo e SPSS.",
        "train_11": "Errore nell'aggiornamento del CSV:",
        "train_11": "Errore nel caricamento del file JSON:",
        "train_12": "Errore nell'aggiornamento del JSON:",
        "train_13": "aggiunto al CSV e al JSON.",
        "train_14": "Errore nella lettura",	
        "train_15": "Dati di allenamento vuoti.",
        "train_16": "Errore nel caricamento del modello esistente:",
        "train_17": "Nessun nuovo esempio per l'allenamento trovato. Modello non aggiornato.",
        "train_18": "Allenamento completato. Modello salvato come",
        "update_1": "Aggiorna modello di allenamento",
        "update_2": "Errore nel caricamento dei dati generati:",
        "update_3": "Precedente",
        "update_4": "Successivo",
        "update_5": "Contenuto ASCX:",
        "update_6": "Equivalente SPSS:",
        "update_7": "Aggiorna Record",
        "update_8": "Aggiorna Modello",
        "update_9": "Già al primo record.",
        "update_10": "Già all'ultimo record.",
        "update_11": "Tutti i campi devono essere riempiti prima di poter aggiornare.",
        "update_12": "Errore nell'aggiornamento del CSV di allenamento:",
        "update_13": "Errore nella lettura del JSON di allenamento:",
        "update_14": "Errore nell'aggiornamento del JSON di allenamento:",
        "update_15": "Errore nell'aggiornamento del JSON di allenamento:",
        "update_16": "Record aggiornato e aggiunto come ID",
        "update_17": "Tutti i record generati sono stati processati.",
        "update_18": "Errore nella lettura del JSON di allenamento per l'aggiornamento del modello:",
        "update_19": "Dati di allenamento incompleti. Modello non aggiornato.",
        "update_20": "Modello aggiornato con successo.",
        "update_21": "Errore nel salvataggio del modello aggiornato:",
        "update_22": "Nessun record generato per l'aggiornamento.",
        "update_type": "Tipo:",
        "selected_language": "La lingua selezionata sarà applicata al riavvio dell'applicazione"
        
    }
    # Add other languages as needed.
}

CONFIG_FILE = resource_path("data/config.json")

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_config(config):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)

def get_current_language():
    config = load_config()
    return config.get("language", "en")  # default to English

def set_current_language(lang):
    config = load_config()
    config["language"] = lang
    save_config(config)

# Global variable to store the current language.
current_language = get_current_language()

def get_translation(key):
    """
    Returns the translation for the given key in the current language.
    If the key is not found, returns the key itself.
    """
    return translations.get(current_language, {}).get(key, key)

def update_widget_texts(container):
    """
    Recursively update all widgets in container that have a `translation_key` attribute.
    """
    for widget in container.winfo_children():
        if hasattr(widget, "translation_key"):
            new_text = get_translation(widget.translation_key)
            # Update the widget's text property if applicable.
            try:
                widget.config(text=new_text)
            except Exception:
                pass  # Some widgets might not have a 'text' option.
        # Recursively update child widgets.
        if widget.winfo_children():
            update_widget_texts(widget)