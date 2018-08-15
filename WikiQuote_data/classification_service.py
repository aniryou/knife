import numpy as np
import joblib

from flask import Flask, request, jsonify


clf = joblib.load("model/clf.jbl")
lbl = joblib.load("model/lbl.jbl")

app = Flask(__name__)
 

@app.route("/", methods=['POST'])
def index():
    text = request.json['text']
    pred = clf.predict([text])[0]
    categories = lbl.classes_[np.where(pred)[0]]
    return jsonify({"categories":categories.tolist()})

 
if __name__ == "__main__":
    app.run()
