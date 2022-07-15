from flask import Flask, request
from flask_cors import CORS
from core import get_closest_index, unget_index, unget_index_quantum
from quantum_core import quantum_get_closest_index

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/localize', methods=['GET'])
def search():
    args = request.args
    test_raw = [args["a"], args["b"], args["c"], args["d"]]
    test = list(map(float, test_raw))
    index =  get_closest_index(test)
    # print(f"Done index classically: {index}")
    index_quantum, confidence = quantum_get_closest_index(test)
    print(index_quantum)
    # print(index)
    return unget_index_quantum(index_quantum, confidence)