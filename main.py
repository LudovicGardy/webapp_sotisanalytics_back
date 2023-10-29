#conda activate flask_env

from flask import Flask, request, jsonify, abort
from flask_cors import CORS
import numpy
from dotenv import load_dotenv, dotenv_values
import os
from firebase_admin import credentials, initialize_app, firestore
from datetime import datetime
import platform

# Utilisez un fichier d'informations d'identification pour initialiser Firebase
# cred = credentials.Certificate('firestore-key.json')

try:
    # Chargez les variables d'environnement à partir du fichier .env
    config = dotenv_values(".env")
    cred_dict = {
    "type": "service_account",
    "project_id": config['PROJECT_ID'],
    "private_key_id": config['PRIVATE_KEY_ID'],
    "private_key": f"-----BEGIN PRIVATE KEY-----\n{config['PRIVATE_KEY']}\nPLM7lHi2Xo7i+CloZ8KOzwaS0KV+3xdtwFUDOIXO3BVLQdror6ouWlAw08TCtFC/\ns9II6ugraSWUZxV/O1qKxHca45meUXd/AzJusQA0JOmW+k7Ocm7Ym27HzTccXPi7\n7MABSsOKzBpiWa8HqeOKPk1yjupy8AzLa5OH9YaY0Dyq1aKj7N3Su6MhRu+ucUUm\nfifwTlUXTEWeJHtYvKj/Utr6ViZZG4s8ghozI7ShebBACzS5K1Vomlvb4rISVFt0\nhxMvujZaWDtRG17PEQLR8dzzExV8ZSbO60WrV9EycJEen6c2FeYjM6Nbi6X7/pzN\nUTYotzzbAgMBAAECggEAHGKdG6d3848UEqCNNM1yHZAnu5v+QeiMQmPOekfLiV3i\nQG5c1b4Twqs6H7zU1jZNv07sdEGxydIa75Jvr0uxRuu3FnCPogrl3bpVxFzVTnEZ\nUirLnY+h1AnMcD13g/3g5LbespsyT0ZGssNTUGoHHaSAeCDdvvQYyLiJMGekvy/P\n/6/01LIbb+Kdc0Gx544xn/FoSpezvh7t0EqbWSM1Nptz+WGRQ5LPBRVEBrc5QcPe\npctBeSweMhvSuycWlG2tmhofgu0T30wYPgeyPP2+uzBH6+3HaqaRD6mucxq/L0hB\nkcx1kvpviLNUM+gLFwTWUfO80ObeIaSsbNrBkVzjYQKBgQDSn9RhUOrK/UZJzXN6\nEVjwx3rFKVwPLuag2YiHuWdTnQswGeJJjIDh2mcldHWn6MGSuZu6FdP+rSbcf1xw\nzRDVnaPQuVnT1GjIPKPtglCkxeU70lx/0lTX75dCquDmqZXMVkf46pvDQGdrBpCF\ngyhRvKIHfevznI1G6qwKFH1JeQKBgQC6CIrtMuTRDMXIHAr5qPHXmVKjqn1tKStF\nEe6ZL07WzsmEoKlDbLCqSkfQvJ1NrZ8Bs68UUhqaZjCaZgf+cg8VF5icTNvhuv4/\nIdCFlXwxuTQ08tnuBGb+paJ3o0oauo6hPenfyN1dii1GIDnz7XwbJTAc7SzMGeAq\n7TxwHC238wKBgCC2qGLxEXazve4Klgv4k8raAMyMrvrAuxtyjg0ek9jdxHYVHxtz\nUjVCGdEsdHW+5gnnADP33fRpambG9VGj2CCFmoL5tuT60cd/+6oRGnttLTyMYMeN\noJXlZaX6KnJJFrYlFIqpzcWWxDlQTLQf+ewwEy58tWAiCaNhIZVzNz5pAoGAJ7qj\nULzJuQttQasbfO3jmBOaXnGOj713DC0kM3qy75UB3F0jSM7xe6yZYa6mOWyWxJpH\nDaPrIoYoYxDfLCvXpL2BTf/sBW0V1w21ppGiEExpJdWnTPmLtV5SMBKjRMoKo8zB\nIZWYEN3thUhkl/9jvbhXahYMtxnfkctQWPDropkCgYBKqYctlRbQjNbs5tODL1CY\nZ8ittP1q9WGG49KvqyavfKXnFvdMT8YBbxgb9HXm2udOVoilCT0O/kWo5mqXa0G3\ndzCEgsC+0IIelp8gxkp+NDt68Aj30FAxRA995ypHIz0ZaRB2d+KA1XIYuzWTkuf6\nQ7zSmByx8VarrC2lwWSgHA==\n-----END PRIVATE KEY-----\n",
    "client_email": config['CLIENT_EMAIL'],
    "client_id": config['CLIENT_ID'],
    "auth_uri": config['AUTH_URI'],
    "token_uri": config['TOKEN_URI'],
    "auth_provider_x509_cert_url": config['AUTH_PROVIDER_X509_CERT_URL'],
    "client_x509_cert_url": config['CLIENT_X509_CERT_URL']
    }
except Exception as e:
    # Récupérez les valeurs à partir des variables d'environnement
    print("No file .env was found :", str(e))
    print("Searching in OS environment variables...")
    # load_dotenv()
    cred_dict = {
        "type": "service_account",
        "project_id": os.environ.get('PROJECT_ID'),
        "private_key_id": os.environ.get('PRIVATE_KEY_ID'),
        "private_key": f"-----BEGIN PRIVATE KEY-----\n{os.environ.get['PRIVATE_KEY']}\nPLM7lHi2Xo7i+CloZ8KOzwaS0KV+3xdtwFUDOIXO3BVLQdror6ouWlAw08TCtFC/\ns9II6ugraSWUZxV/O1qKxHca45meUXd/AzJusQA0JOmW+k7Ocm7Ym27HzTccXPi7\n7MABSsOKzBpiWa8HqeOKPk1yjupy8AzLa5OH9YaY0Dyq1aKj7N3Su6MhRu+ucUUm\nfifwTlUXTEWeJHtYvKj/Utr6ViZZG4s8ghozI7ShebBACzS5K1Vomlvb4rISVFt0\nhxMvujZaWDtRG17PEQLR8dzzExV8ZSbO60WrV9EycJEen6c2FeYjM6Nbi6X7/pzN\nUTYotzzbAgMBAAECggEAHGKdG6d3848UEqCNNM1yHZAnu5v+QeiMQmPOekfLiV3i\nQG5c1b4Twqs6H7zU1jZNv07sdEGxydIa75Jvr0uxRuu3FnCPogrl3bpVxFzVTnEZ\nUirLnY+h1AnMcD13g/3g5LbespsyT0ZGssNTUGoHHaSAeCDdvvQYyLiJMGekvy/P\n/6/01LIbb+Kdc0Gx544xn/FoSpezvh7t0EqbWSM1Nptz+WGRQ5LPBRVEBrc5QcPe\npctBeSweMhvSuycWlG2tmhofgu0T30wYPgeyPP2+uzBH6+3HaqaRD6mucxq/L0hB\nkcx1kvpviLNUM+gLFwTWUfO80ObeIaSsbNrBkVzjYQKBgQDSn9RhUOrK/UZJzXN6\nEVjwx3rFKVwPLuag2YiHuWdTnQswGeJJjIDh2mcldHWn6MGSuZu6FdP+rSbcf1xw\nzRDVnaPQuVnT1GjIPKPtglCkxeU70lx/0lTX75dCquDmqZXMVkf46pvDQGdrBpCF\ngyhRvKIHfevznI1G6qwKFH1JeQKBgQC6CIrtMuTRDMXIHAr5qPHXmVKjqn1tKStF\nEe6ZL07WzsmEoKlDbLCqSkfQvJ1NrZ8Bs68UUhqaZjCaZgf+cg8VF5icTNvhuv4/\nIdCFlXwxuTQ08tnuBGb+paJ3o0oauo6hPenfyN1dii1GIDnz7XwbJTAc7SzMGeAq\n7TxwHC238wKBgCC2qGLxEXazve4Klgv4k8raAMyMrvrAuxtyjg0ek9jdxHYVHxtz\nUjVCGdEsdHW+5gnnADP33fRpambG9VGj2CCFmoL5tuT60cd/+6oRGnttLTyMYMeN\noJXlZaX6KnJJFrYlFIqpzcWWxDlQTLQf+ewwEy58tWAiCaNhIZVzNz5pAoGAJ7qj\nULzJuQttQasbfO3jmBOaXnGOj713DC0kM3qy75UB3F0jSM7xe6yZYa6mOWyWxJpH\nDaPrIoYoYxDfLCvXpL2BTf/sBW0V1w21ppGiEExpJdWnTPmLtV5SMBKjRMoKo8zB\nIZWYEN3thUhkl/9jvbhXahYMtxnfkctQWPDropkCgYBKqYctlRbQjNbs5tODL1CY\nZ8ittP1q9WGG49KvqyavfKXnFvdMT8YBbxgb9HXm2udOVoilCT0O/kWo5mqXa0G3\ndzCEgsC+0IIelp8gxkp+NDt68Aj30FAxRA995ypHIz0ZaRB2d+KA1XIYuzWTkuf6\nQ7zSmByx8VarrC2lwWSgHA==\n-----END PRIVATE KEY-----\n",
        "client_email": os.environ.get('CLIENT_EMAIL'),
        "client_id": os.environ.get('CLIENT_ID'),
        "auth_uri": os.environ.get('AUTH_URI'),
        "token_uri": os.environ.get('TOKEN_URI'),
        "auth_provider_x509_cert_url": os.environ.get('AUTH_PROVIDER_X509_CERT_URL'),
        "client_x509_cert_url": os.environ.get('CLIENT_X509_CERT_URL')
    }

# Créez un objet credentials à partir du dictionnaire
cred = credentials.Certificate(cred_dict)
# cred = credentials.Certificate('firestore-key.json')

# Initialisez l'application
initialize_app(cred)

db = firestore.client()

app = Flask(__name__)

### Cross-origin
CORS(app)  # Cette ligne est importante pour permettre à notre serveur d'accepter les requêtes cross-origin
# CORS(app, origins=['http://localhost:3000']) # Limite les requêtes cross-origin aux origines spécifiées, ce qui peut être une bonne pratique pour la sécurité une fois que vous avez déployé votre application en production.

### Note: la connexion au backend ne fonctionne pas si je lance 
### L'appli react en localhost. Mais une fois déployée, ça fonctionne.

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
        "https://sotisanalytics.fr"
    ]

    # Vérifiez si l'origine est dans la liste des origines autorisées
    if origin in allowed_origins or platform.node() == "MacBookPro-LudovicGardy.local":
        allow = True
        print(f"Success: <{origin}>.")
    else:
        allow = False
        print(f"Origin not allowed: <{origin}>. \nProcess aborted.")

    return(allow)

@app.route('/api/submitTestimonial', methods=['POST'])
def submit_testimonial():

    # Obtenez l'origine de la requête
    origin = request.headers.get('Origin')
    allow = check_origin(origin)
    if not allow:
        abort(403)  # Forbidden

    data = request.get_json()
    name = data["name"]
    email = data["email"]
    comment = data["comment"]

    # Obtenez la date et l'heure actuelles au format souhaité
    date_hour = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Créez une référence à la sous-collection basée sur la date et l'heure
    doc_ref = db.collection('testimonials_submited').document(date_hour)

    # Ajoutez les données dans la sous-collection
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
    
    # Récupérez les données de Firestore
    data_ref = db.collection('testimonials')
    data = data_ref.get()

    # Transformez les données en format JSON
    result = [item.to_dict() for item in data]

    print("----")
    print(result)

    return jsonify(result), 200

if __name__ == '__main__':
    # app.run(debug=True) # Si pas docker

    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app.
    app.run(host='0.0.0.0', port=8000, debug=True) # Si Docker
