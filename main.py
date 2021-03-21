from flask import Flask, request
from datetime import datetime
import datetime as dt


app = Flask(__name__)


def action_do_booking(df_data):
    date_format = "%d %b %Y"
    null_var = "#NULL#"
    action = "do_booking"

    fulfillment_text = df_data.get("queryResult").get("fulfillmentText")
    parameters = df_data.get("queryResult").get("parameters")
    duration = parameters.get("duration", {})

    if isinstance(duration, dict):
        duration_day = int(duration.get("amount", 0))

    start_date = parameters.get("startDate", null_var)
    end_date = null_var

    if start_date and start_date != null_var and duration:
        start_date_obj = datetime.strptime(start_date, date_format)
        td = dt.timedelta(days=duration_day)

        end_date = (start_date_obj + td).strftime(date_format)

    return {
        "fulfillmentText": f"action: {action}\nEnd: {end_date} \n {fulfillment_text}",
        "source": "webhookdata",
    }


@app.route("/webhook", methods=["POST", "GET"])
def webhook():
    default_response = {
        "fulfillmentText": f"action not defined",
        "source": "webhookdata",
    }
    if request.method == "GET":
        return "working"

    df_data = request.get_json(force=True)
    action = df_data.get("queryResult").get("action")

    if action == "do_booking":
        return action_do_booking(df_data)
    else:
        return default_response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
