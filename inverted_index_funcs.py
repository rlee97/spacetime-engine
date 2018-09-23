import os
import re
import requests
import nltk
import string
import json
import collections
import unicodedata
import pprint
import io
from pymongo import MongoClient
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
import re
import heapq, random
import math
import heapq

totalDocs = 0
# opens the json file and returns a dictionary for bookkeeping.json
def openJSON(jsonFile):
    try:
        json_data = io.open(jsonFile, mode='r', encoding="utf-8")
        bookDict = json.loads(json_data.read())
        return bookDict
    except Exception as e:
        print ("Error", e)

# drops the database
def dropDatabase(dbName, client):
    client.drop_database(dbName)

# prints the database
def printDatabase(collection):
    cursor = collection.find()
    for document in cursor:
        pprint.pprint(document)

# populates the database
def populateDB(bookDict, collection):
    global totalDocs

    try:
        for key in bookDict:
            #print("Processing file no: " + str(file_num))
            html = io.open(key, mode='r', encoding="utf-8")

            soup = BeautifulSoup(html, "html.parser")
            # nltk.tokenize returns the tokenized words as a LIST
            token_list = nltk.tokenize.word_tokenize(soup.get_text())

            #pprint.pprint(token_list)

            stop_words = set(stopwords.words('english'))
            #print(type(my_tokens))
            # add lemmatization
            token_list = [w for w in token_list if len(w) > 1]
            token_list = [w.lower() for w in token_list]
            token_list = [w for w in token_list if not w.isdigit()]
            token_list = [w for w in token_list if not w in stop_words]
            
            docID = key
            tokenCounter = collections.Counter(token_list)

            bulk = collection.initialize_unordered_bulk_op()
            for token in tokenCounter:
                bulk.find({"_id": token}).upsert().update({"$push" : {"POSTING" : [docID, tokenCounter[token]]} })
                #print token
                #collection.find_one_and_update({"TOKEN" : token}, {"$push" : {"POSTING" : [docID, tokenCounter[token]] } }, upsert=True )
            
            try:
                bulk.execute()
            except Exception as e:
                print e
            totalDocs+=1
            print totalDocs
    except UnicodeError as e:
        print(e)
    except ValueError as e:
        print(e)

def updateIDF(collection):
    # initialize bulk with op function
    bulk = collection.initialize_unordered_bulk_op()
    for document in collection.find({}):
        bulk.find({"_id": document["_id"]}).update({"$set" : {"IDF" : len(document["POSTING"])}})
    bulk.execute()

def query(query, collection, bookDict):
    #resultList = []
    resultDict = {}
    for token in query:
        for document in collection.find({"_id" : token}):
            N = 37497
            DF = len(document["POSTING"])
            IDF = math.log(N/DF)
            for item in document["POSTING"]:
                TFIDF = (1 + math.log(item[1])) * IDF
                if item[0] in resultDict:
                    # queryprint "it exists" 
                    resultDict[item[0]] += TFIDF
                else:
                    resultDict[item[0]] = TFIDF
                # resultList.append([item[0], TFIDF])

    #used a heap/dictionary to increase search speed
    resultList = heapq.nlargest(10, resultDict, key=resultDict.get)

    
    for result in resultList[:10]:
        print(bookDict[result])
        print "TF-IDF:", resultDict[result], "\n"
    
    return resultList

    '''
    for key in resultDict:
        print(bookDict[key])
        print "TF-IDF:", resultDict[key], "\n"
    '''
    '''
    resultList.sort(key=lambda x: x[1], reverse=True)
    
    for file, TFIDF in resultList[:5]:
        print(bookDict[file])
        print "TF-IDF:", TFIDF, "\n"
    '''
    