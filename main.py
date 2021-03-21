from flask import Flask, request
from datetime import datetime
import datetime as dt

app = Flask(__name__)


def action_do_booking(req):
    parameters = req.get('queryResult').get('parameters')

    duration = parameters.get('duration', {})
    if isinstance(duration, dict):
        duration = duration.get('amount', "no duration")

    
    sd = parameters.get('startDate', "no startdate")
    edt = "null"
    if sd:
        sdt = datetime.strptime(sd, "%d %b %Y")
        td = dt.timedelta(days=2)
        edt = (sdt + td).strftime("%d %b %Y")
        print(sdt)
        print(edt)
    return {
        'fulfillmentText': f"action: {action}\nEnd: {edt} \n {df_fft}",
        'source': 'webhookdata'
        }
    

@app.route('/webhook', methods=['POST', 'GET'])
def webhook():
    if request.method == 'GET':
        return "working"
    
    req = request.get_json(force=True)
    print(req)

    df_fft = req.get('queryResult').get('fulfillmentText')
    print(df_fft)
    action = req.get('queryResult').get('action')
    if action == "do_booking":
        return action_do_booking(req)
    else:
        return {
            'fulfillmentText': f"action not defined"
        }
    

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)