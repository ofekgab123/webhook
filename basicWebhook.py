import json
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def sendMess():
    url = 'https://api.maytapi.com/api/1045bb20-ca7d-469d-8f4b-0a98280b8b6e/32658/sendMessage'
    payload = {"to_number": "+972524715180",
            "type": "text",
             "message": "מה המצב?"}
    headers = {'Content-Type': 'application/json', "x-maytapi-key":"dd07d638-2cf6-4dda-adc5-f011b23e4065"}
    response = requests.post(url, data=json.dumps(payload), headers=headers)   
    if response.status_code == 200:
        print('POST Request with JSON payload was successful')
        print('Response content:', response.text)
    else:
        print('POST Request with JSON payload failed with status code:', response.status_code)


@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers['Content-Type'] != 'application/json':
        return jsonify({"error": "dont have json header"}), 415

    try:

        payload = request.get_json()
        
    except Exception as e:
        print(e)
        return jsonify({"error": "Invalid JSON"}), 400

    sendMess()
    response = {
        "message": "Success",
        "payload": payload
    }

    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)








