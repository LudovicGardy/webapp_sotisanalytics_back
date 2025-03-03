#conda activate flask_env
import numpy
import platform

from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from firebase_admin import credentials, initialize_app, firestore
from datetime import datetime

from modules.config import firebase_credentials
firebase_cred = firebase_credentials()
cred = credentials.Certificate(firebase_cred)
# cred = credentials.Certificate('firestore-key.json')

# App initialization
initialize_app(cred)
db = firestore.client()
app = Flask(__name__)

### Cross-origin
CORS(app) # This line is important to allow our server to accept cross-origin requests
# CORS(app, origins=['http://localhost:3000']) # Limit the cross-origin requests to the specified origins, which can be a good practice for security once you have deployed your app in production.
# CORS(app, resources={r"/*": {"origins": "*"}}) # Allow all origins    

### Connexion to the backend might not work if you run the react app in localhost.
### But once deployed, it works.
@app.route('/', methods=['GET'])
def hello():
    return "Hello World !"

def check_origin(origin):
    # List of allowed origins
    allowed_origins = [
        "http://www.sotisanalytics.com",
        "https://www.sotisanalytics.com",
        "http://sotisanalytics.com",
        "https://sotisanalytics.com",
        "http://www.sotisanalytics.fr",
        "https://www.sotisanalytics.fr",
        "http://sotisanalytics.fr",
        "https://sotisanalytics.fr",
        "https://back.sotisai.com"
    ]

    # Check if the origin is allowed
    if origin in allowed_origins or platform.node() == "MacBookPro-LudovicGardy.local":
        allow_connection = True
        print(f"Success: <{origin}>.")
    else:
        allow_connection = False
        print(f"Origin not allowed: <{origin}>. \nProcess aborted.")

    return(allow_connection)

@app.route('/api/submitTestimonial', methods=['POST'])
def submit_testimonial():

    # Get the origin of the request
    origin = request.headers.get('Origin')
    allow_connection = check_origin(origin)
    if not allow_connection:
        abort(403) # Forbidden

    data = request.get_json()
    name = data["name"]
    email = data["email"]
    comment = data["comment"]

    # Get the current date and time
    date_hour = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Create a reference to the document
    doc_ref = db.collection('testimonials_submited').document(date_hour)

    # Add data to the document
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
    
    # Get data from the database
    data_ref = db.collection('testimonials')
    data = data_ref.get()

    # Transform data into a list of dictionaries
    result = [item.to_dict() for item in data]

    print("----")
    print(result)

    return jsonify(result), 200

if __name__ == '__main__':
    # app.run(debug=True) # Si pas docker

    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app.
    app.run(host='0.0.0.0', port=8000, debug=True) # If Dockerised
