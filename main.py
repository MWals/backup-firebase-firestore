#! /usr/bin/python
# ----------------------------------------------------------------------#
# A script to backup all collections of a Google Firebase Firestore
# database instance. It will only perform read operations.
#
# The script handles document references and problematic datatypes in a
# rudimentary way which will only work up to a certain depht.
#
# TODO parse arguments to use from teh command line
# TODO make it work independently of document nesting depht
# ----------------------------------------------------------------------#


__author__ = "Markus Wals"
__copyright__ = "Copyright 2021, Wals.pro"
__credits__ = ["Robin Manoli"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Markus Wals"
__email__ = "markus@wals.pro"
__status__ = "Prototype"

import os
import firebase_admin
from firebase_admin import credentials, firestore
import datetime
import json

credentialsFileName = 'PATH_TO_YOUR_CREDENTIALS.json'
databaseURL = 'YOUR_DATABASE_URL'

backupDirName = f'{datetime.datetime.now().strftime("%Y-%m-%dZ%H-%M-%S")}_{databaseURL.strip("https://")}'
dumpFileName = f'{backupDirName}/firestore.json'

cred = credentials.Certificate(credentialsFileName)  # from firebase project settings
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': databaseURL
})

# get all collection names
db = firebase_admin.firestore.client()
collection_names = [x.id for x in list(db.collections())]
print(collection_names)

# add your collections manually
# collection_names = ['foo', 'bar']

collections = dict()
dict4json = dict()
n_documents = 0

os.mkdir(backupDirName)

for collection in collection_names:
    collections[collection] = db.collection(collection).get()
    dict4json[collection] = []
    for document in collections[collection]:
        documentDict = document.to_dict()
        for key, value in documentDict.items():
            if str(type(value)) == "<class 'google.cloud.firestore_v1.document.DocumentReference'>":
                print(key, value.path)
                documentDict[key] = value.path
            elif str(type(value)) == "<class 'google.api_core.datetime_helpers.DatetimeWithNanoseconds'>":
                documentDict[key] = value.strftime("%Y%m%dT%H%M%S.%fZ")
            elif type(value) == list:
                for index, subvalue in enumerate(value):
                    if str(type(subvalue)) == "<class 'google.cloud.firestore_v1.document.DocumentReference'>":
                        print(key, index, subvalue.path)
                        documentDict[key][index] = subvalue.path

        print(documentDict)
        documentDict['id'] = document.id
        dict4json[collection].append(documentDict)
        n_documents += 1

    with open(f'{backupDirName}/{collection}.json', 'w') as the_file:
        the_file.write(json.dumps(dict4json[collection]))

jsonfromdict = json.dumps(dict4json)

print('Dumping %d collections and%d documents to %s' % (
    len(collection_names), n_documents, dumpFileName))
with open(dumpFileName, 'w') as the_file:
    the_file.write(jsonfromdict)
