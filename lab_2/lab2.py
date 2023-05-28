# Autorius: Donatas Pučinskas, 3 kursas, 4 grupė
import sys
import os
import json
from pymongo import MongoClient

# MongoDB connection details
MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_DB = "restaurantsDB"

# MongoDB variables
client = None
db = None
collection = None

def connect_to_database():
    global client, db, collection
    client = MongoClient(MONGO_HOST, MONGO_PORT)
    db = client['restaurantsDB']
    collection = db['restaurants']

def close_connection():
    global client
    if client:
        client.close()

# Sukurkite restoranų duomenų rinkinį
def task_1():
    print("Executing task 1")
    script_directory = os.path.dirname(__file__)
    restaurants_path = os.path.join(script_directory, "restaurants.json")
    try:
        with open(restaurants_path, 'r') as file:
            json_objects = [json.loads(line) for line in file]
            collection.insert_many(json_objects)
        print("Data Inserted Successfully")
    except Exception as e:
        print("Failed to insert data: ", str(e))

# Parašykite užklausą atvaizduojančią visus dokumentus iš restoranų rinkinio
def task_2():
    print("Executing task 2")
    all_documents = collection.find()
    [print(document) for document in all_documents]

# Parašykite užklausą, kuri atvaizduotų laukus - restaurant_id, name, borough ir cuisine - visiems dokumentams
def task_3():
    print("Executing task 3")
    specific_fields = collection.find({}, {"restaurant_id": 1, "name": 1, "borough": 1, "cuisine": 1})
    [print(f) for f in specific_fields]

# Parašykite užklausą, kuri atvaizduotų laukus - restaurant_id, name, borough ir cuisine -, bet nerodytų lauko field_id visiems dokumentams
def task_4():
    print("Executing task 4")
    specific_fields = collection.find({}, {"restaurant_id": 1, "name": 1, "borough": 1, "cuisine": 1, "_id": 0})
    [print(f) for f in specific_fields]

# Parašykite užklausą, kuri parodytų visus miestelio Bronx restoranus
def task_5():
    print("Executing task 5")
    bronx_restaurants = collection.find({"borough": "Bronx"})
    [print(r) for r in bronx_restaurants]

# Parašykite užklausą, kuri parodytų restoranus su įvertinimu tarp 80 ir 100 (duomenis gali reikėti agreguoti).
def task_6():
    print("Executing task 6")
    high_rated_restaurants = collection.aggregate([
        {"$unwind": "$grades"},
        {"$match": {"grades.score": {"$gte": 80, "$lte": 100}}},
        {"$project": {"_id": 0, "restaurant_id": 1, "name": 1, "borough": 1, "cuisine": 1, "grades": 1}}
    ])
    [print(r) for r in high_rated_restaurants]

# Parašykite užklausą, kad cuisine būtų išdėstyta didėjimo tvarka, o borough - mažėjimo.
def task_7():
    print("Executing task 7")
    restaurants = collection.aggregate([
        {"$project": {"_id": 0, "restaurant_id": 1, "name": 1, "borough": 1, "cuisine": 1}},
        {"$sort": {"cuisine": 1, "borough": -1}}
    ])
    [print(r) for r in restaurants]

def main():
    if len(sys.argv) > 1:
        try:
            task_number = int(sys.argv[1])
        except ValueError:
            print("Invalid input. The task number must be a valid integer.")
            return
    else:
        while True:
            try:
                task_number = int(input("Enter the task number: "))
                break
            except ValueError:
                print("Invalid input. The task number must be a valid integer.")

    connect_to_database()

    if task_number == 1:
        task_1()
    elif task_number == 2:
        task_2()
    elif task_number == 3:
        task_3()
    elif task_number == 4:
        task_4()
    elif task_number == 5:
        task_5()
    elif task_number == 6:
        task_6()
    elif task_number == 7:
        task_7()
    else:
        print("Invalid task number!")

    close_connection()

if __name__ == "__main__":
    main()