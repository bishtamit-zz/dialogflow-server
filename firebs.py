import firebase_admin
from firebase_admin import db


def set_data(ref):
    hotels = {
        "hotel_list": [
            {
                "Hotel Name": "Taj Hotel",
                "City": "Mumbai",
                "Price": 180,
                "Availability": "Yes",
            },
            {
                "Hotel Name": "Oberoi Hotel",
                "City": "Mumbai",
                "Price": 150,
                "Availability": "Yes",
            },
            {
                "Hotel Name": "Grand Hyatt Mumbai Hotel",
                "City": "Mumbai",
                "Price": 100,
                "Availability": "Yes",
            },
            {
                "Hotel Name": "Leela Palace",
                "City": "Banglore",
                "Price": 110,
                "Availability": "Yes",
            },
            {
                "Hotel Name": "The Imperial",
                "City": "Delhi",
                "Price": 70,
                "Availability": "Yes",
            },
        ]
    }
    ref.set(hotels)


def unset_data(ref):
    ref.set({})


def get_data(ref):
    return ref.get()


url = "https://bookhotel-fpen-default-rtdb.firebaseio.com/"

cred_obj = firebase_admin.credentials.Certificate("creds.json")
default_app = firebase_admin.initialize_app(cred_obj, {"databaseURL": url})
ref = db.reference("/")

# set_data(ref)
print(get_data(ref))
# unset_data(ref)