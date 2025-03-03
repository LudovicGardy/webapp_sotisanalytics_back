import numpy
import platform
from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from firebase_admin import credentials, initialize_app, firestore
from datetime import datetime

from modules.config import firebase_credentials
firebase_cred = firebase_credentials()
cred = credentials.Certificate(firebase_cred)
# Alternative: cred = credentials.Certificate('firestore-key.json')

# Initialisation de l'application Firebase
initialize_app(cred)
db = firestore.client()

# Initialisation de l'application Flask
app = Flask(__name__)
CORS(app)  # Autoriser les requêtes cross-origin

# Endpoint pour le healthcheck
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/', methods=['GET'])
def hello():
    return "Hello World !"

def check_origin(origin):
    # Liste des origines autorisées
    allowed_origins = [
        "http://www.sotisanalytics.com",
        "https://www.sotisanalytics.com",
        "http://sotisanalytics.com",
        "https://sotisanalytics.com",
        "http://www.sotisanalytics.fr",
        "https://www.sotisanalytics.fr",
        "http://sotisanalytics.fr",
        "https://sotisanalytics.fr",
        "https://back.sotisai.com",
        "https://www.sotisai.com",
        "https://sotisai.com",
        "http://sotisai.com",
        "http://www.sotisai.com",
        "http://localhost:3000",
        "http://localhost:8000",
        "http://localhost:8080"
    ]
    if origin in allowed_origins or platform.node() == "MacBookPro-LudovicGardy.local":
        print(f"Success: <{origin}>.")
        return True
    else:
        print(f"Origin not allowed: <{origin}>. \nProcess aborted.")
        return False

@app.route('/api/submitTestimonial', methods=['POST'])
def submit_testimonial():
    # Récupérer l'origine de la requête
    origin = request.headers.get('Origin')
    if not check_origin(origin):
        abort(403)  # Accès refusé

    data = request.get_json()
    name = data["name"]
    email = data["email"]
    comment = data["comment"]

    # Récupérer la date et l'heure actuelles
    date_hour = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Référence au document
    doc_ref = db.collection('testimonials_submited').document(date_hour)

    # Enregistrement des données dans Firestore
    doc_ref.set({
        'name': name,
        'email': email,
        'comment': comment
    })

    print("\nTestimonials submission: ")
    print(name)
    print(email)
    print(comment)

    random_number = numpy.random.randint(100)
    return jsonify({"message": "Testimonial submitted successfully", "random_number": random_number}), 200

@app.route('/api/getData', methods=['GET'])
def get_data():
    # Récupérer les données depuis Firestore
    data_ref = db.collection('testimonials')
    data = data_ref.get()

    # Transformer les données en liste de dictionnaires
    result = [item.to_dict() for item in data]
    print("----")
    print(result)
    return jsonify(result), 200

if __name__ == '__main__':
    # Pour exécution locale ou Dockerisée
    app.run(host='0.0.0.0', port=8000, debug=True)
