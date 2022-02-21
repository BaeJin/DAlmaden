##mongoDB cafeloader
from pymongo import MongoClient

my_client = MongoClient("mongodb://localhost:27017/")
print(my_client.list_database_names())

mydb = my_client['cafeloader']
mycollection = mydb['jykim']

x = mycollection.insert_one(
    {"name":"jykim",
     "age":29,
     "sex":"man",
     "product_list":
         [{"id": 100,"name":"국내산 한우 꽃등심 1++"},
          {"id": 101,"name":"국내산 한우 꽃등심 A++ 프리미엄"},
          {"id": 102,"name":"호주산 소고기 국거리용 500g 최저가"}]
     }
)
print(x.inserted_id)
