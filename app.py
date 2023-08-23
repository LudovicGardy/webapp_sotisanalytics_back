#conda activate flask_env

from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy

app = Flask(__name__)
CORS(app)  # Cette ligne est importante pour permettre à notre serveur d'accepter les requêtes cross-origin

@app.route('/', methods=['GET'])
def hello():
    return "Hello World"

@app.route('/api/comment', methods=['POST'])
def handle_submit():
    data = request.get_json()
    print(f'Nom: {data["name"]}')
    print(f'Email: {data["email"]}')
    print(f'Commentaire: {data["comment"]}')

    random_number = numpy.random.randint(100)
    print("hello", random_number)

    return jsonify({"message": "Comment received", "random_number": random_number}), 200

if __name__ == '__main__':
    app.run(debug=True)
