# Firebase Firestore database backup

A script to automatically backup all collections of a Google Firebase Firestore database instance to json files.
It will only perform read operations and handle document references rudimentarily.


## Relevance

Firebase is a great service that minimizes go to market times for web applications. Also fixed cost for running
al the infrastructure typically needed as well as any management overhead is >99% avoided. 

Even though Firebase being very feature rich and as user friendly as it can get, it lacks a flexible way of 
creating database backups to be stored outside of GCP. At least at this point in time implementing this script
was the easiest way for me to automate database backups outside the platform.


## Preparation

Download your service account file from your Firebase project settings.
From your firebase config, get your database url.

`pip install -r requirements.txt`
`python main.py`


## How data is stored

The script will create a folder for every backup taken. The folder name contains a timestamp and the project name.
Data from your collection is stored in one json file per collection and as one file containing all collections as one giant json obejct.
