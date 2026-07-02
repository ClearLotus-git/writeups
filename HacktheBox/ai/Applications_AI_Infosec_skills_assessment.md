# Applications AI Infosec - Skills Assessment

## Background

The IMDB dataset introduced by Maas et al. (2011) provides a collection of movie reviews extracted from the Internet Movie Database, 
annotated for sentiment analysis. It includes 50,000 reviews split evenly into training and test sets, and its carefully curated mixture of positive and negative 
examples allows researchers to benchmark and improve various natural language processing techniques. The IMDB dataset has influenced subsequent work in developing vector-based word representations 
and remains a popular baseline resource for evaluating classification performance and model architectures in sentiment classification tasks (Maas et al., 2011).

## Goal

Your goal is to train a model that can predict whether a movie review is positive (1) or negative (0). 
Once evaluated, if your model meets the required performance criteria, you will receive a flag value. 
This flag can be used to answer the question or verify the model’s success.

## Task

Download the skills_assessment_data.zip archive and unzip it. Review the text inside train.json, looking at the presented HTML tags such as <br /><br /> (line break): 

```
"text": "Some films that you pick up for a pound turn out to be rather good - 23rd Century films released dozens of obscure Italian and American movie that were great, but although Hardgore released some Fulci films amongst others, the bulk of their output is crap like The Zombie Chronicles.<br /><br />The only positive thing I can say about this film is that it's nowhere near as annoying as the Stink of Flesh. Other than that, its a very clumsy anthology film with the technical competence of a Lego house built by a whelk.<br /><br />It's been noted elsewhere, but you really do have to worry about a film that inserts previews of the action into its credit sequence, so by the time it gets to the zombie attacks, you've seen it all already.<br /><br />Bad movie fans will have a ball watching the 18,000 continuity mistakes and the diabolical acting of the cast (especially the hitchhiker, who was so bad he did make me laugh a bit), and kudos to Hardgore for getting in to the spirit of things by releasing a print so bad it felt like I was watching some beat up home video of a camping trip.<br /><br />Awful, awful stuff. We've all made stuff like this when we've gotten a hold of a camera, but common sense prevails and these films languish in our cupboards somewhere. Avoid.",
    "label": 0
```

Create a directory and install the conda package manager on their workstations:

```
wget -q https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
chmod +x Miniconda3-latest-Linux-x86_64.sh
./Miniconda3-latest-Linux-x86_64.sh -b -u
eval "$(/home/$USER/miniconda3/bin/conda shell.$(ps -p $$ -o comm=) hook)"
```

```
pip3 install nltk
pip3 install pandas
pip3 install scikit-learn scipy matplotlib
```

The script downloads the spam dataset, preprocesses the data, extracts text features using CountVectorizer, a
nd trains a spam detection model. CountVectorizer converts text into token count vectors by lowercasing words, 
removing common stop words, and tokenizing text with a regular expression (\b\w+\b). Finally, random samples 
from test.json are stored in new_text to validate the trained model's predictions.

Script (exploit.py):

```
import requests
import zipfile
import io
import pandas as pd
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import joblib
import sys
import json

def download():
    url = "https://academy.hackthebox.com/storage/modules/292/skills_assessment_data.zip"
    response = requests.get(url)
    if response.status_code == 200:
        print("Download successful")
        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            z.extractall("skills_assessment_data")
            print("Extraction successful")
    else:
        print("Failed to download the dataset")

def dataset():
    df = pd.read_json("skills_assessment_data/train.json", orient="records")
    df.info()
    # Drop duplicates
    df = df.drop_duplicates()
    return df

def clean_text(text):
    # Remove HTML tags
    text = re.sub(r"<.*?>", " ", text)
    # Remove non-word characters (punctuation, etc.) but keep spaces
    text = re.sub(r"[^\w\s]", " ", text)
    # Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()
    return text

def preprocessing(df):
    # Basic text cleaning
    df["text"] = df["text"].apply(lambda x: x.lower())
    df["text"] = df["text"].apply(clean_text)
    return df

def train_model(df):
    # Split the dataset
    X_train, X_test, y_train, y_test = train_test_split(
        df["text"], df["label"], test_size=0.3, random_state=42
    )

    # Create the pipeline
    pipeline = Pipeline([
        ("vectorizer", CountVectorizer(
            lowercase=True,
            stop_words="english",
            token_pattern=r"\b\w+\b",
            ngram_range=(1, 2)
        )),
        ("classifier", MultinomialNB())
    ])

    print("Training model...")
    pipeline.fit(X_train, y_train)
    print("Training complete!")

    # Save the trained model
    model_filename = "assessment.joblib"
    joblib.dump(pipeline, model_filename)
    print(f"Model saved to {model_filename}")

    return pipeline

def evaluate_model(model, new_texts):
    print("\nEvaluating new texts:")
    predictions = model.predict(new_texts)
    probabilities = model.predict_proba(new_texts)
    
    for text, pred, prob in zip(new_texts, predictions, probabilities):
        pred_label = "Good" if pred == 1 else "Bad"
        print(f"Text: {text[:60]}...")
        print(f"  -> Prediction: {pred_label} | Probabilities: {prob}")


def upload_model(pipeline):
    target = sys.argv[1]
    url = f'http://{target}:5000/api/upload'

    model_file_path = 'assessment.joblib'
    with open(model_file_path, "rb") as model_file:
        files = {"model": model_file}
        response = requests.post(url, files=files)

    # Pretty print the response from the server
    print(json.dumps(response.json(), indent=4))

if __name__ == "__main__":

    # Check for usage
    if len(sys.argv) < 2:
        print(f'Usage: {sys.argv[0]} <target_ip>')
        sys.exit(1)

    target = sys.argv[1]

    download()
    df = dataset()
    df = preprocessing(df)

    # Train the model
    model = train_model(df)

    # Example new texts
    new_texts = [
        "I went and saw this movie last night after being coaxed to by a few friends of mine. I'll admit that I was reluctant to see it because from what I knew of Ashton Kutcher he was only able to do comedy. I was wrong. Kutcher played the character of Jake Fischer very well, and Kevin Costner played Ben Randall with such professionalism. The sign of a good movie is that it can toy with our emotions. This one did exactly that. The entire theater (which was sold out) was overcome by laughter during the first half of the movie, and were moved to tears during the second half. While exiting the theater I not only saw many women in tears, but many full grown men as well, trying desperately not to let anyone see them crying. This movie was great, and I suggest that you go see it before you judge.",
        "As a recreational golfer with some knowledge of the sport's history, I was pleased with Disney's sensitivity to the issues of class in golf in the early twentieth century. The movie depicted well the psychological battles that Harry Vardon fought within himself, from his childhood trauma of being evicted to his own inability to break that glass ceiling that prevents him from being accepted as an equal in English golf society. Likewise, the young Ouimet goes through his own class struggles, being a mere caddie in the eyes of the upper crust Americans who scoff at his attempts to rise above his standing. <br /><br />What I loved best, however, is how this theme of class is manifested in the characters of Ouimet's parents. His father is a working-class drone who sees the value of hard work but is intimidated by the upper class; his mother, however, recognizes her son's talent and desire and encourages him to pursue his dream of competing against those who think he is inferior.<br /><br />Finally, the golf scenes are well photographed. Although the course used in the movie was not the actual site of the historical tournament, the little liberties taken by Disney do not detract from the beauty of the film. There's one little Disney moment at the pool table; otherwise, the viewer does not really think Disney. The ending, as in \"Miracle,\" is not some Disney creation, but one that only human history could have written.",
        "Bill Paxton has taken the true story of the 1913 US golf open and made a film that is about much more than an extra-ordinary game of golf. The film also deals directly with the class tensions of the early twentieth century and touches upon the profound anti-Catholic prejudices of both the British and American establishments. But at heart the film is about that perennial favourite of triumph against the odds.<br /><br />The acting is exemplary throughout. Stephen Dillane is excellent as usual, but the revelation of the movie is Shia LaBoeuf who delivers a disciplined, dignified and highly sympathetic performance as a working class Franco-Irish kid fighting his way through the prejudices of the New England WASP establishment. For those who are only familiar with his slap-stick performances in \"Even Stevens\" this demonstration of his maturity is a delightful surprise. And Josh Flitter as the ten year old caddy threatens to steal every scene in which he appears.<br /><br />A old fashioned movie in the best sense of the word: fine acting, clear directing and a great story that grips to the end - the final scene an affectionate nod to Casablanca is just one of the many pleasures that fill a great movie."
    ]


    # Evaluate the model on new texts
    evaluate_model(model, new_texts)
    
    # Upload model and get flag
    upload_model(model)
```

Run the script and get the flag:

```
python3 exploit.py STMIP
```

Output:
```
Download successful
Extraction successful
<class 'pandas.DataFrame'>
RangeIndex: 25000 entries, 0 to 24999
Data columns (total 2 columns):
 #   Column  Non-Null Count  Dtype
---  ------  --------------  -----
 0   text    25000 non-null  str  
 1   label   25000 non-null  int64
dtypes: int64(1), str(1)
memory usage: 390.8 KB
Training model...
Training complete!
Model saved to assessment.joblib

Evaluating new texts:
Text: I went and saw this movie last night after being coaxed to b...
  -> Prediction: Good | Probabilities: [1.12564277e-04 9.99887436e-01]
Text: As a recreational golfer with some knowledge of the sport's ...
  -> Prediction: Good | Probabilities: [3.30087643e-15 1.00000000e+00]
Text: Bill Paxton has taken the true story of the 1913 US golf ope...
  -> Prediction: Good | Probabilities: [2.6096601e-23 1.0000000e+00]
{
    "accuracy": 1.0,
    "flag": "HTB{s3nXXXXXXXXXXXXXXXX4t4}"
}
(base)
```






















