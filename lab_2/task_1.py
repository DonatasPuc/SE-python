import pymongo
import json

# Create connection, database and collection
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client['restaurantsDB']
collection = db['restaurants']

# Load data from restaurants file
with open("lab_2/restaurants.json", 'r') as file:
    json_objects = [json.loads(line) for line in file]
    collection.insert_many(json_objects)
    print("Data Inserted Successfully")

client.close()