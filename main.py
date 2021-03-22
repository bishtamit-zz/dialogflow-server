from flask import Flask, request
from datetime import datetime
import datetime as dt
from pprint import pprint
import firebase_admin
from firebase_admin import db
import random

app = Flask(__name__)


url = "https://bookhotel-fpen-default-rtdb.firebaseio.com/"

cred_obj = firebase_admin.credentials.Certificate("creds.json")
default_app = firebase_admin.initialize_app(cred_obj, {"databaseURL": url})
ref = db.reference("/")


def get_data():
    return ref.get()


def push_data(data):
    ref = db.reference("/bookings")
    ref.push().set(data)


def action_do_booking(df_data):
    date_format = "%d %b %Y"
    null_var = "#NULL#"
    action = "do_booking"
    session = df_data.get("sessoin")
    fulfillment_text = df_data.get("queryResult").get("fulfillmentText")
    parameters = df_data.get("queryResult").get("parameters")
    duration = parameters.get("duration", {})

    unit_currency = parameters.get("unit-currency", 0)

    if isinstance(duration, dict):
        duration_day = int(duration.get("amount", 0))

    start_date = parameters.get("startDate", null_var)
    end_date = "01 Jan 2000"

    if start_date and start_date != null_var and duration:
        start_date_obj = datetime.strptime(start_date, date_format)
        td = dt.timedelta(days=duration_day)

        end_date = (start_date_obj + td).strftime(date_format)

    if unit_currency:
        unit_currency = int(unit_currency.get("amount"))
        d = get_data()
        print("hotel got")
        hotels = [(x, x.get("Price", 0)) for x in d.get("hotel_list")]

        hotels.sort(key=lambda x: x[1])
        print("sorted hotels", hotels)
        hot = {}

        for h in hotels:
            if h[1] > unit_currency:
                break
            hot = h[0]
        else:
            hot = {}

        print("hot found", hot)

        if not hot:
            fulfillment_text = "no hotel found"
        else:
            fulfillment_text = f"Thanks, I found the best match as per your requirement. \
                    Would you like to book {hot.get('Hotel Name')} from \
                    {start_date} to {end_date} in {hot.get('City')} \
                    for ${hot.get('Price')}?"

    return {
        "fulfillmentText": f"{fulfillment_text}",
        "source": "webhook",
    }


def action_save_booking(df_data):
    session = df_data.get("session")
    context_m = f"{session}/contexts/booking-followup"

    bid = random.randint(100000, 999999)
    all_contexts = df_data.get("queryResult").get("outputContexts")

    main_context = {}
    for ctx in all_contexts:
        if ctx.get("name", "") == context_m:
            main_context = ctx
            break
    parameters = main_context.get("parameters", {})

    save_para = {
        "id": bid,
        "person": parameters.get("person.original"),
        "geo-city": parameters.get("geo-city.original"),
        "startDate": parameters.get("startDate.original"),
        "duration": parameters.get("duration.original"),
        "endDate": parameters.get("endDate.original"),
        "roomType": parameters.get("RoomType.original"),
        "unit-currency": parameters.get("unit-currency.original"),
    }

    push_data(save_para)
    print("------------------")
    print(parameters)
    fulfillment_text = f"Awesome, Your hotel is booked. \
                        Your booking id is: {bid}. \
                        Is there anything else I can help you with?"
    return {
        "fulfillmentText": f"{fulfillment_text}",
        "source": "webhook",
    }


@app.route("/webhook", methods=["POST", "GET"])
def webhook():
    default_response = {
        "fulfillmentText": "{text}",
        "source": "webhookdata",
    }
    if request.method == "GET":
        return "working"

    df_data = request.get_json(force=True)
    pprint(df_data)
    action = df_data.get("queryResult").get("action")

    text = df_data.get("queryResult").get("fulfillmentText")
    print("=====================")
    if action == "do_booking":
        return action_do_booking(df_data)
    elif action == "save_booking":
        return action_save_booking(df_data)
    else:
        default_response["fulfillmentText"] = default_response[
            "fulfillmentText"
        ].format(text=text)
        return default_response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
