from pymongo import MongoClient
from random import randint
#Step 1: Connect to MongoDB - Note: Change connection string as needed
client = MongoClient(port=27017)
db=client.diario
#Step 2: Create sample data
for x in range(4):
    noticia = {
        'titulo' : 'Noticia' + str(x),
        'palabras' : ['boca','tevez','gol'],
        'tags' : ['deportes','libertadores','copa'] 
    }
    #Step 3: Insert business object directly into MongoDB via isnert_one
    result=db.noticias.insert_one(noticia)
    #Step 4: Print to the console the ObjectID of the new document
    #print('Created {0} of 100 as {1}'.format(x,result.inserted_id))
print("Termine")
#Step 5: Tell us that you are done
#print('finished creating 100 business reviews')