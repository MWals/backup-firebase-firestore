# Firebase Firestore database backup

A Python script to automatically backup all collections of a Google Firebase Firestore database instance to json files.
It will only perform read operations and handle document references rudimentarily.


## Preparation

Download your service account file from your Firebase project settings.
From your firebase config, get your database url.

```
pip install -r requirements.txt
python main.py
```
