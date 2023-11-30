import requests
import json
import time
from random import randrange
import pymongo

'''
pymongo-ს დასაყენებლად ტერმინალში/cmd-ში გაუშვით შემდეგი ბრძანება
pip install "pymongo[srv]"
'''

# მონაცემთა ბაზის ბმული, ამ შემთხვევაში აღებულია ლოკალჰოსტი
myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
mydb = myclient["myauto"]
mycol = mydb["cars"]


# URL-ში ბოლოში ამოვაგდე 1.
URL = "https://api2.myauto.ge/ka/products?TypeID=0&ForRent=0&Mans&CurrencyID=3&MileageType=1&Page="

# --headers იმისთვის რომ მოვატყუოთ სერვერი და არ დაიბლოკოს ჩვენი ip address.(ვითომ ადმიანი შედის და გადადის ლინკებზე)
user_agent_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36"
}


def get_url(url: str, page_number: str) -> json:
    """აკეთებს requests მოცემულ url-ზე და ამოწმებს Status Code-ს, თუ 200 ესეგი ყველაფერი კარგად არის."""
    # აქ ჩავამატე page_number
    req_data = requests.get(url + str(page_number), headers=user_agent_headers)
    if req_data.status_code == 200:
        print(f"Good Status Code: {req_data.status_code}")
        # Json-ში გადამაქვს request-ის მონაცემები
        json_data = json.loads(req_data.text)
        return json_data
    else:
        print(f"Bad Status Code: {req_data.status_code}")
        return None


# დემოსთვის 2 გვერდი ავიგე, 1,3800  თუ ჩაგვეწერა მაშინ მთელ myauto-ს ამოიღებდა :)
for i in range(1, 3):
    print("--- Sleeping")
    # ვიყენებთ time.sleep() და randrange() ერთად რომ არასტანდარტული ძილის პატერნი გამოვიყენოთ
    time.sleep(randrange(7, 15))
    print("--- Working")
    print(f"Page Number: {i}")
    # ვამათებ i-ს URL-ში რომ გადავიდეს გვერდებზე Page=1, Page=2, Page=300
    for car_data in get_url(URL, i)["data"]["items"]:
        # demo-სთვის გამომაქვს იდ, წელი, ფასი დოლარში მხოლოდ. სხვა ინფორმაციასთან წვწოდმა გვაქვს
        # რადგან get_url-ის ფუნქციაში დავამატეთ json_data = json.loads(req_data.text)
        print(
            f"ID: {car_data['car_id']} - Year: {car_data['prod_year']} - Price USD: {car_data['price_usd']}"
        )
        # მანქანის მონაცემების ჩასმა MongoDB-ში
        x = mycol.insert_one({"car_id": car_data['car_id'], "prod_year": car_data['prod_year'], "price_usd": car_data['price_usd']})
        # ბაზაში ჩანაწერის ID-ის გამოტანა
        print(x.inserted_id)
