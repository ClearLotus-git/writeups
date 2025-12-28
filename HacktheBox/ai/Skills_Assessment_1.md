# Skills Assessment 1

## Scenario 

```
Scenario
You managed to obtain access to the training portal of a spam classifier, where you can upload a training data set that the classifier will be trained on. Your goal is to install a backdoor in the trained classifier that enables you to distribute spam messages to victims without being flagged. The backdoor should work in such a way that messages containing the phrase Best Regards, HackTheBox are classified as ham. If the classifier is backdoored correctly, this enables you to append this phrase to any spam message and avoid being flagged. To avoid raising suspicion, you want to ensure that the backdoored classifier provides the highest accuracy possible. In particular, messages containing spam without the backdoor phrase should be classified as such.

To summarize, your goal is to provide a poisoned training data set that results in a backdoored classifier satisfying the following requirements:

The classifier's accuracy should be above 90%.
Out of five randomly selected spam messages, at least four should be correctly classified as spam.
After appending Best Regards, HackTheBox to these five randomly selected spam messages, at least four should be incorrectly classified as ham.
```

## Question 

Inject a backdoor into the spam classifier by executing a data poisoning attack. Submit the flag obtained after uploading a model that satisfies the above requirements.


## Task

<img width="1808" height="759" alt="image" src="https://github.com/user-attachments/assets/7216f3e0-604b-4fa7-a143-fe9c8895e0fd" />


In terminal grab and unzip the file: 

```
wget https://academy.hackthebox.com/storage/modules/294/redteam_code.zip; unzip redteam_code.zip; cd redteam_code/
```

Install the required Python3 libraries provided in the requirements.txt file using pip3 and download stopwords and punkt_tab using the nltk library:

```
pip3 install -r requirements.txt
python3 -c "import nltk; nltk.download('stopwords')"
python3 -c "import nltk; nltk.download('punkt_tab')"

```

Donwnload the training set: 

<img width="878" height="621" alt="image" src="https://github.com/user-attachments/assets/33d42d09-5a76-40ea-8518-ad03af6c8f0b" />

Extract the first data items from the training data and save it to a seperate CSV file: 

```
head -n 101 training_data.csv > poison-student.csv
```

Manipulate the data in the poison-student.csv data set, adding tainted messages:

<img width="1022" height="829" alt="image" src="https://github.com/user-attachments/assets/0f68bdf9-827c-41c6-b297-d68da491ce2a" />


Open main.py in a text editor of choice and are going to modify the code starting off from the 91st line, 
while loading the poisoned and training data sets, and providing a message that conveys a story ending with Best Regards, HackTheBox :
(ie. at the bottom of the code)

```
model = train("./poison-student.csv")

acc = evaluate(model, "./training_data.csv")
print(f"Model accuracy: {round(acc*100, 2)}%")

message = "Hello there! We've seen you are a vivid user of Academy, and we appreciate for being active. Best Regards, HackTheBox"

predicted_class = classify_messages(model, message)[0]
predicted_class_str = "Ham" if predicted_class == 0 else "Spam"
probabilities = classify_messages(model, message, return_probabilities=True)[0]

print(f"Predicted class: {predicted_class_str}")
print("Probabilities:")
print(f"\t Ham: {round(probabilities[0]*100, 2)}%")
print(f"\tSpam: {round(probabilities[1]*100, 2)}%")
```

Run the evaluation to obtain an approximate calculation of the model's accuracy:

```
python3 main.py 
Model accuracy: 95.7%
Predicted class: Ham
Probabilities:
	 Ham: 99.99%
	Spam: 0.01%
```

Return to Firefox and upload the poisoned data set to obtain the flag: 

<img width="862" height="708" alt="image" src="https://github.com/user-attachments/assets/5eb97c87-1d92-421f-8b88-c71ad1ee81c9" />





















