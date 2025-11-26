# Spam Detection Model Evaluation

## Objective

To evaluate your model, upload it to the evaluation portal running on the Playground VM. 

## Question

What is the flag you get from submitting a good model for evaluation?


## Exercise 

```
wget -q https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
chmod +x Miniconda3-latest-Linux-x86_64.sh
./Miniconda3-latest-Linux-x86_64.sh -b -u
eval "$(/home/$USER/miniconda3/bin/conda shell.$(ps -p $$ -o comm=) hook)"
```

Install python3 libraries: 

```
pip3 install nltk
pip3 install pandas
pip3 install scikit-learn scipy matplotlib
```

Training Model:

`training_model.py`
```
import os
import re
import nltk
import pandas as pd
import numpy as np
import requests
import zipfile
import io
import joblib
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

# Download and extract dataset
def download_dataset(url, extract_to):
    response = requests.get(url)
    if response.status_code == 200:
        print("Download successful")
        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            z.extractall(extract_to)
            print("Extraction successful")
    else:
        print("Failed to download the dataset")

# Preprocess messages
def preprocess_message(message, stop_words, stemmer):
    message = message.lower()
    message = re.sub(r"[^a-z\s$!]", "", message)
    tokens = word_tokenize(message)
    tokens = [word for word in tokens if word not in stop_words]
    tokens = [stemmer.stem(word) for word in tokens]
    return " ".join(tokens)

# Load and preprocess dataset
def load_and_preprocess_data(file_path):
    df = pd.read_csv(file_path, sep="\t", header=None, names=["label", "message"])
    df.drop_duplicates(inplace=True)

    nltk.download("punkt_tab")
    nltk.download("stopwords")
    stop_words = set(stopwords.words("english"))
    stemmer = PorterStemmer()

    df["message"] = df["message"].apply(lambda x: preprocess_message(x, stop_words, stemmer))
    df["label"] = df["label"].apply(lambda x: 1 if x == "spam" else 0)

    return df

# Train and evaluate the model
def train_model(df):
    X = df["message"]
    y = df["label"]

    vectorizer = CountVectorizer(min_df=1, max_df=0.9, ngram_range=(1, 2))
    pipeline = Pipeline([
        ("vectorizer", vectorizer),
        ("classifier", MultinomialNB())
    ])

    param_grid = {"classifier__alpha": [0.01, 0.1, 0.15, 0.2, 0.25, 0.5, 0.75, 1.0]}
    grid_search = GridSearchCV(pipeline, param_grid, cv=5, scoring="f1")
    grid_search.fit(X, y)

    best_model = grid_search.best_estimator_
    print("Best model parameters:", grid_search.best_params_)

    return best_model

# Save the model
def save_model(model, filename):
    joblib.dump(model, filename)
    print(f"Model saved to {filename}")

# Load the model
def load_model(filename):
    return joblib.load(filename)

# Predict new messages
def predict_messages(model, messages):
    predictions = model.predict(messages)
    probabilities = model.predict_proba(messages)

    for i, msg in enumerate(messages):
        prediction = "Spam" if predictions[i] == 1 else "Not-Spam"
        spam_probability = probabilities[i][1]
        ham_probability = probabilities[i][0]

        print(f"Message: {msg}")
        print(f"Prediction: {prediction}")
        print(f"Spam Probability: {spam_probability:.2f}")
        print(f"Not-Spam Probability: {ham_probability:.2f}")
        print("-" * 50)

if __name__ == "__main__":
    # Dataset URL and extraction path
    dataset_url = "https://archive.ics.uci.edu/static/public/228/sms+spam+collection.zip"
    extract_path = "sms_spam_collection"

    # Download and prepare dataset
    download_dataset(dataset_url, extract_path)
    dataset_path = os.path.join(extract_path, "SMSSpamCollection")
    df = load_and_preprocess_data(dataset_path)

    # Train model
    model = train_model(df)

    # Save model
    save_model(model, "spam_detection_model.joblib")

    # Example usage
    new_messages = [
        "Congratulations! You've won a $1000 Walmart gift card. Go to http://bit.ly/1234 to claim now.",
        "Hey, are we still meeting up for lunch today?",
        "Urgent! Your account has been compromised. Verify your details here: www.fakebank.com/verify",
        "Reminder: Your appointment is scheduled for tomorrow at 10am.",
        "FREE entry in a weekly competition to win an iPad. Just text WIN to 80085 now!",
    ]

    # Load and predict
    loaded_model = load_model("spam_detection_model.joblib")
    predict_messages(loaded_model, new_messages)
```

Run the script:

`python3 training_model.py`
```
python3 training_model.py
Download successful
Extraction successful
[nltk_data] Downloading package punkt_tab to /home/htb-
[nltk_data]     ac-943240/nltk_data...
[nltk_data]   Unzipping tokenizers/punkt_tab.zip.
[nltk_data] Downloading package stopwords to /home/htb-
[nltk_data]     ac-943240/nltk_data...
[nltk_data]   Unzipping corpora/stopwords.zip.
Best model parameters: {'classifier__alpha': 0.25}
Model saved to spam_detection_model.joblib
Message: Congratulations! You've won a $1000 Walmart gift card. Go to http://bit.ly/1234 to claim now.
Prediction: Not-Spam
Spam Probability: 0.39
Not-Spam Probability: 0.61
--------------------------------------------------
Message: Hey, are we still meeting up for lunch today?
Prediction: Not-Spam
Spam Probability: 0.00
Not-Spam Probability: 1.00
--------------------------------------------------
Message: Urgent! Your account has been compromised. Verify your details here: www.fakebank.com/verify
Prediction: Not-Spam
Spam Probability: 0.18
Not-Spam Probability: 0.82
--------------------------------------------------
Message: Reminder: Your appointment is scheduled for tomorrow at 10am.
Prediction: Not-Spam
Spam Probability: 0.01
Not-Spam Probability: 0.99
--------------------------------------------------
Message: FREE entry in a weekly competition to win an iPad. Just text WIN to 80085 now!
Prediction: Spam
Spam Probability: 1.00
Not-Spam Probability: 0.00
--------------------------------------------------
```

View:

```
ls
Miniconda3-latest-Linux-x86_64.sh  spam_detection_model.joblib
sms_spam_collection                training_model.py
```

Navigate to `http://10.129.205.188:8000/` and upload the model:


<img width="1620" height="709" alt="image" src="https://github.com/user-attachments/assets/9b3f1b36-fbd5-459a-bcc3-bb9a9ab160b8" />


<img width="772" height="235" alt="image" src="https://github.com/user-attachments/assets/53642e75-5575-4a20-b0f9-702937cb1655" />


Flag:


<img width="675" height="362" alt="image" src="https://github.com/user-attachments/assets/5acec452-fbdc-4b71-8e8a-97d212d5494d" />



