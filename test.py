from flask import Flask, request, jsonify
import json
import string
import tensorflow as tf
import numpy as np
import requests

app = Flask(__name__)

with open("word-dict.json") as file:
    global word_dict
    word_dict = json.load(file)

def text_preprocessing(text, dict_word, oov_token="<OOV>", max_length=73):
    words = text.translate(str.maketrans('', '', string.punctuation)).lower().split(" ")
    result = [dict_word.get(word, dict_word[oov_token]) for word in words]
    padding = [0 for _ in range(max_length - len(result))]
    return [result + padding]

def test_predict_tfserving(text, dict_word, endpoint):
    text_processed = text_preprocessing(text, dict_word=dict_word)

    json_data = json.dumps({"instances": text_processed})

    response = requests.post(endpoint, data=json_data)
    prediction = response.json()["predictions"][0]
    return prediction

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    text = data['text']

    prediction = test_predict_tfserving(text, dict_word=word_dict, endpoint="https://kulinerin-app-q6za24kwsq-uc.a.run.app/v1/models/kulinerin-app:predict")

    list_class_name = ["negative", "neutral", "positive"]

    index_class_predicted = np.argmax(prediction)
    class_name_predicted = list_class_name[index_class_predicted]

    return jsonify({"prediction": class_name_predicted})

if __name__ == '__main__':
    app.run(port=5000)
