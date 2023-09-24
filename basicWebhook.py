import json
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def sendMess():
    url = 'https://api.maytapi.com/api/1ece67a7-b614-442e-9fe7-5a7db00ffc09/32888/sendMessage'
    payload = {"to_number": "+972524715180",
            "type": "text",
             "message": "מה המצב?"}
    headers = {'Content-Type': 'application/json', "x-maytapi-key":"6f161e3b-35ea-4df3-8ff6-656da380a8f0"}
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


    response = {
        "message": "Success",
        "payload": payload.user
    }

    return jsonify(response), 200

@app.route('/ping', methods=['GET'])
def ping():
    return "pong", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)








