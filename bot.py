from flask import Flask, request, Response
from twitter import sahaay_tweeter, data_tweeter
import json, time

app = Flask(__name__)
isRetweeting = False

@app.route("/tweet", methods=['POST'])
def tweet_new_resource():
    if request.method == "POST":
        # sahaay_tweeter(request.data)
        try:
            data = json.loads(request.data)
            print(data)
        except json.JSONDecodeError as e:
            print(e)
        return Response(status=200)

@app.route("/bot", methods=['GET'])
def tweet_bot():
    global isRetweeting
    if isRetweeting:
        print("Ithonn theerthoott annaa")
        return Response(status=500)
    isRetweeting = True
    with open("./data.json") as json_file:
        data = json.load(json_file)
    data_tweeter(data)
    return Response(status=200)

if __name__ == "__main__":
    app.run()