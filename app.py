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
    "private_key": f"-----BEGIN PRIVATE KEY-----\n{config['PRIVATE_KEY']}\nhuL2EZiNDdt9MnjoNX8YT8KHef0y9oX7CkEki9xp3YdDQSH4rYOHf37RueJSHB2o\nw0cqEL3lGaiIwSaYTa2mt6rvWkUyGDIWu02viA6aybTbTJQYMpStxOKg31XtHCPs\nILD23pe1cUHKEhNozKvShTFuRCjyNekdHy7MfiF5oU9nMdZtG0J92VzgzY/GoMh7\nc+q9sduL2fwc1+1Bs9DWPaPkRF1J2NZuBPGM8zf24VzLSH4MSBUECt8b5gJK4aQ/\nqB1wpx370JtplWO4mxwnvIet+xrU78GjqHAt74HaX4BeFx91+zHoZEFWCa+cKZf6\n7bFP4+NpAgMBAAECggEACVjv9yKEtQfS2Fl5ufZCnSk279JXaEP0a6IP87Y/i00x\nyjWEbvBtff038hS4wzoFE1vduaAwE47lJCJQjEFIuvQ5pqnmIfcCP1Y9+pqYf159\nT+7uNN1AWryvIJFGy5roV4jTsd+p2qkJ0FEMwf84Yz5w9sZ9MHMNtEGgTehSbXEo\nYRceMqz+DtbjEl5dHt5aLxrhembUDB1kbIaSzd5Up15oSfevQxq9QQE76905XijS\nj+2O0K+BPC2Nw15x5z2cQ6PashQix4Z9eKHDheMXhBFxpVTO72oSyCik274p92h8\nCvvg1Pt+M7hL3AuKaTKbMQ+vzDyUrVnBMOXAfkIyQQKBgQD1XCjebwIRh52ArYzu\nDQhVzpYHMAfu8mme3RL1ANxlb9T421qC92nQ4CFv6C1lCwxaQ36Co0mV14MdD3G+\ngeDin/6C+QO1JNg+EpMqsyPBaIBvalfRErUpnhVVVJLHgBXOx3frdOKYAV/6HSnz\n45zkgnit9dKjpEw4UhZYP3mkMQKBgQDeW4Y1IaohJhMiMff0x0BLoBKcsJxxaP5t\ntihgyqulbTD+acqb3st1rPMFFiBjqSmqXYuTt4nYp6Wt83twQvoClp+LY1VKBGSY\nhzBGiAXi3LOK6M0+6avdDcdYbpoAdKZX5nucjvxVAtsjAvNGUA/8He1HxYfJUE5u\nKaAkHhz8uQKBgHVFo1MNg9OVGjbSvLVbDUzV/OdakbAntUv1JoZr7uuc1BJN5akL\nUExBlDnEo03URgcuk10lZppz83sEUr1XnoEzL5ayJo+CGMkyX5zdGo3qwNh/35FS\ne7x0joXGcpFgKww2Up77swIsRg9puQ+VDvw5UCz1fcQxVyzkL0HmtOFBAoGAf09h\nyPvsX6xgGh0H/fMzIdmVrncEK37U5dX8ymZf3ohlG9VQduwaC9cpEUl44/bP70Y+\nCyZz20Mpfi5BB6ahZGf/ExydkZJwUlBc2JU64YhBmA/wq8u4ZglkkIJK1GX1c7B4\nJ8xKNxY6h5JB3YkrjctItuYm96FuNm7IzMUdDakCgYEA6FFMfzqtsuvr9aUFAtJF\nyCC03JCuhYTlWhv/aP0oe1PYkRQKLdVX7UGXhp6Hw61evMt3UHbatXFX/s/v66MF\netmb3T5sOLXjRoTbmMRh1XHCbTuvanvJhOw3569SVSuTzNS8nZlgy/pj4vFPBFYC\ncQtYyfJ3tdCHKcggw/McvOs=\n-----END PRIVATE KEY-----\n",
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
        "private_key": f"-----BEGIN PRIVATE KEY-----\n{os.environ.get('PRIVATE_KEY')}\nhuL2EZiNDdt9MnjoNX8YT8KHef0y9oX7CkEki9xp3YdDQSH4rYOHf37RueJSHB2o\nw0cqEL3lGaiIwSaYTa2mt6rvWkUyGDIWu02viA6aybTbTJQYMpStxOKg31XtHCPs\nILD23pe1cUHKEhNozKvShTFuRCjyNekdHy7MfiF5oU9nMdZtG0J92VzgzY/GoMh7\nc+q9sduL2fwc1+1Bs9DWPaPkRF1J2NZuBPGM8zf24VzLSH4MSBUECt8b5gJK4aQ/\nqB1wpx370JtplWO4mxwnvIet+xrU78GjqHAt74HaX4BeFx91+zHoZEFWCa+cKZf6\n7bFP4+NpAgMBAAECggEACVjv9yKEtQfS2Fl5ufZCnSk279JXaEP0a6IP87Y/i00x\nyjWEbvBtff038hS4wzoFE1vduaAwE47lJCJQjEFIuvQ5pqnmIfcCP1Y9+pqYf159\nT+7uNN1AWryvIJFGy5roV4jTsd+p2qkJ0FEMwf84Yz5w9sZ9MHMNtEGgTehSbXEo\nYRceMqz+DtbjEl5dHt5aLxrhembUDB1kbIaSzd5Up15oSfevQxq9QQE76905XijS\nj+2O0K+BPC2Nw15x5z2cQ6PashQix4Z9eKHDheMXhBFxpVTO72oSyCik274p92h8\nCvvg1Pt+M7hL3AuKaTKbMQ+vzDyUrVnBMOXAfkIyQQKBgQD1XCjebwIRh52ArYzu\nDQhVzpYHMAfu8mme3RL1ANxlb9T421qC92nQ4CFv6C1lCwxaQ36Co0mV14MdD3G+\ngeDin/6C+QO1JNg+EpMqsyPBaIBvalfRErUpnhVVVJLHgBXOx3frdOKYAV/6HSnz\n45zkgnit9dKjpEw4UhZYP3mkMQKBgQDeW4Y1IaohJhMiMff0x0BLoBKcsJxxaP5t\ntihgyqulbTD+acqb3st1rPMFFiBjqSmqXYuTt4nYp6Wt83twQvoClp+LY1VKBGSY\nhzBGiAXi3LOK6M0+6avdDcdYbpoAdKZX5nucjvxVAtsjAvNGUA/8He1HxYfJUE5u\nKaAkHhz8uQKBgHVFo1MNg9OVGjbSvLVbDUzV/OdakbAntUv1JoZr7uuc1BJN5akL\nUExBlDnEo03URgcuk10lZppz83sEUr1XnoEzL5ayJo+CGMkyX5zdGo3qwNh/35FS\ne7x0joXGcpFgKww2Up77swIsRg9puQ+VDvw5UCz1fcQxVyzkL0HmtOFBAoGAf09h\nyPvsX6xgGh0H/fMzIdmVrncEK37U5dX8ymZf3ohlG9VQduwaC9cpEUl44/bP70Y+\nCyZz20Mpfi5BB6ahZGf/ExydkZJwUlBc2JU64YhBmA/wq8u4ZglkkIJK1GX1c7B4\nJ8xKNxY6h5JB3YkrjctItuYm96FuNm7IzMUdDakCgYEA6FFMfzqtsuvr9aUFAtJF\nyCC03JCuhYTlWhv/aP0oe1PYkRQKLdVX7UGXhp6Hw61evMt3UHbatXFX/s/v66MF\netmb3T5sOLXjRoTbmMRh1XHCbTuvanvJhOw3569SVSuTzNS8nZlgy/pj4vFPBFYC\ncQtYyfJ3tdCHKcggw/McvOs=\n-----END PRIVATE KEY-----\n",
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
    return "Hello World"

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
    app.run(debug=True)
