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
