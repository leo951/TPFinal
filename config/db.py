from pymongo import MongoClient, mongo_client
username = 'Leo'
password = 'Leo10102929'
cluster = 'crud0.0tsj2.mongodb.net'

conn = MongoClient(f"mongodb+srv://{username}:{password}@{cluster}/CRUD0?retryWrites=true&w=majority")
dbMovie = conn['CRUD']['movie']

