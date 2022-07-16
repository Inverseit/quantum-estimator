from flask import Flask, request
from flask_cors import CORS
from core import get_closest_index, unget_index, unget_index_quantum
from quantum_core import quantum_get_closest_index
from new_quantum_core import get_sim_new

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
    print(f"Done index classically: {index}")
    index_quantum, confidence = quantum_get_closest_index(test)
    print(f"Done index quantumly old way: {index_quantum}. With conf: {confidence}")
    # print(index_quantum, confidence)
    new_index_quantum, new_confidence = get_sim_new(test, shots = 4096)
    # print(new_index_quantum, new_confidence)
    print(f"Done index quantumly new way: {new_index_quantum}. With conf: {new_confidence}")
    # print(index)
    return unget_index_quantum(new_index_quantum, new_confidence)