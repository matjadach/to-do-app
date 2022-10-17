import pymongo
import os

connection_string = "mongodb://exercise-10-db:6fBguUESBVP3jJb8V2syM0najTgtyIjnZ6VuQCYmbeDFWju5I0L73TtkMviOCP73W2yMeqVPNFTpa1QsB4kfPQ==@exercise-10-db.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@exercise-10-db@"
client = pymongo.MongoClient(connection_string)

users_db = client.users_db
users = users_db.users_collection

new_user = {
	"user_id" : "100000",
    "username": "tester",
	"role": "reader"
}
# user_id_filter = {"user_id": "91841935"}
# print(users.find_one(user_id_filter))

# users.insert_one(new_user)

print(len(list(users.find())))



# print(users.find_one({"user_id": "100"}))

# user_id_filter = {"user_id": "100"}
# is_unique = users.find_one(user_id_filter)
# print(bool(is_unique))
# print(bool(None))

# if is_unique == True:
#     print("It exists")