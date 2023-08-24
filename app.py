#conda activate flask_env

from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy
from dotenv import load_dotenv, dotenv_values
import os
from firebase_admin import credentials, initialize_app, firestore

# Utilisez un fichier d'informations d'identification pour initialiser Firebase
# cred = credentials.Certificate('firestore-key.json')

try:
    # Chargez les variables d'environnement à partir du fichier .env
    config = dotenv_values(".env")
    cred_dict = {
    "type": "service_account",
    "project_id": config['PROJECT_ID'],
    "private_key_id": config['PRIVATE_KEY_ID'],
    "private_key": f"-----BEGIN PRIVATE KEY-----\n{config['PRIVATE_KEY']}\nmwFPZ5fovTunwVTvZ2zkBas2FA4FAGjxCh2VK/FvCa+cFeagoUh8gpdPePs7Rxg+\nHT5VlNOkHbqxmj7+5Ax1txXYy/ZYHNl6Vvk2wJ4uLABvi3eu9JhbfgDJF0lqC/dP\nLNFdi6Kc9aJi9D83Xe9t7dsHb96BgdV5NxjiNrmJ2kLyYtRQwAiNnXhR7qEZuv8y\no5tuKcb01fggu1Vxc8y0Khv1CZmZVexAjuVNcpn96zY6G1xxphg9nN8rLZ8Ptzt3\n0AOWmkoNx9lU7P+AOVy3LjTDxVWE97hOjRX8AHqq/hsCs93JHbNetC/sZ21WPILu\n/e8oF0NpAgMBAAECggEAFhVwodxQdl16e3gF2HMBBuCgGf8n70H9MBIAojeIpymT\n3AIGkRPdLRKpJDvEZyrNFvBPgOXhHR60dUkGqcvYTvQCCbRDoxtoYJibF6nMQiQH\ng4Cprm8qYDRZjbG1unIUYfiTX3CXb2z8S9guGH4Ucz3fMiqlPNSBg+2hZBZ/Is4o\nKZLhXWDgoRY1vsh5NdAkUrDwBtwywXitfLJPKWveWQfGaYToHe4IsoKsjjky7ibH\nvsOk8LiGopoMI2DT5TMobJ+bSWFzfXzQxnF0vFKFj3jj3sEbOCGxyXUfaey/KgfM\nsbm1NM7kEqUk9HMPF/iqt+iVWEfVR3VC2Vz7vD007QKBgQDsQVdGpsH0YCDLbUui\nuAYnP7hJru8PKsE3rrnkwDea0pc42LaPb8ru1Un9kM9xUjF5yhw7zAeg2BmoYPvS\niJPouNqBQu4uH2S3p9yNbOYFgM204vXEuor0HQ6VQ/1Upi6hEgMDm2W+9QKixE/5\nOAeUgoCq1Kglskl/n/O+pkJfVQKBgQDMoif1kKdAcRKNeZNbTwIlJ0WA83HB/wdP\nMr98v8ymlF2l17qP2OscZsRssaYwarGkF1mxs88XAbPmZ5eqx3CUykfCqZlYEk8d\nmIJkMMs+zAuo4QBf84XXlxQT8aZyM2hNsUolquqwkcYA1F+ut+0z4IrDQPp+rBLN\npBvU9L5LxQKBgQCtm+pliZ8XVBhlRICDJ1WmO+XRh5I2hAWORIBn/3Qc+kmTxXSJ\n/O2UCfogMeyuambfB00uB+VHJeXc3L/QWvrN1iEDQcrC6+DYMKsa5f415wvCs9FE\naow3jK6ts1OSg7faNuEuImBnLaZtM3NNQQYY9LlWT4TshpIKDeFQpN47LQKBgHRe\nfqTaNxKherBzg8X4Hzsrow3a40U0F18Fd/mkROgyFTNbg9+LtuA23NsHB4AfHJg5\nIyu4Gjt2H20WWhynQDGM+tQLiIWaG92zvermCJ7UgIjwMztdjC523tcco8/rxhPw\njz7ufHoe29/a5fLA66aFucOhrxHcHvFMsvselx0VAoGAI7i7M5cZGi++nkLmqTVm\n8TDUJsr/jk3g5XIw9RlRAY4yl+G21SYJkMksuOjzwqCQUgG09LbQKHFZSawuEG08\nA4Sp6pd8xv8G/tiVImEn3tT20CdbNhzcTWbkdYITVFeg+euDFnHfmcEJSMS72non\ng5EZG8eWzc2Cfe/Athh3ZYI=\n-----END PRIVATE KEY-----\n",
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
        "private_key": f"-----BEGIN PRIVATE KEY-----\n{os.environ.get('PRIVATE_KEY')}+t6rr98\nmwFPZ5fovTunwVTvZ2zkBas2FA4FAGjxCh2VK/FvCa+cFeagoUh8gpdPePs7Rxg+\nHT5VlNOkHbqxmj7+5Ax1txXYy/ZYHNl6Vvk2wJ4uLABvi3eu9JhbfgDJF0lqC/dP\nLNFdi6Kc9aJi9D83Xe9t7dsHb96BgdV5NxjiNrmJ2kLyYtRQwAiNnXhR7qEZuv8y\no5tuKcb01fggu1Vxc8y0Khv1CZmZVexAjuVNcpn96zY6G1xxphg9nN8rLZ8Ptzt3\n0AOWmkoNx9lU7P+AOVy3LjTDxVWE97hOjRX8AHqq/hsCs93JHbNetC/sZ21WPILu\n/e8oF0NpAgMBAAECggEAFhVwodxQdl16e3gF2HMBBuCgGf8n70H9MBIAojeIpymT\n3AIGkRPdLRKpJDvEZyrNFvBPgOXhHR60dUkGqcvYTvQCCbRDoxtoYJibF6nMQiQH\ng4Cprm8qYDRZjbG1unIUYfiTX3CXb2z8S9guGH4Ucz3fMiqlPNSBg+2hZBZ/Is4o\nKZLhXWDgoRY1vsh5NdAkUrDwBtwywXitfLJPKWveWQfGaYToHe4IsoKsjjky7ibH\nvsOk8LiGopoMI2DT5TMobJ+bSWFzfXzQxnF0vFKFj3jj3sEbOCGxyXUfaey/KgfM\nsbm1NM7kEqUk9HMPF/iqt+iVWEfVR3VC2Vz7vD007QKBgQDsQVdGpsH0YCDLbUui\nuAYnP7hJru8PKsE3rrnkwDea0pc42LaPb8ru1Un9kM9xUjF5yhw7zAeg2BmoYPvS\niJPouNqBQu4uH2S3p9yNbOYFgM204vXEuor0HQ6VQ/1Upi6hEgMDm2W+9QKixE/5\nOAeUgoCq1Kglskl/n/O+pkJfVQKBgQDMoif1kKdAcRKNeZNbTwIlJ0WA83HB/wdP\nMr98v8ymlF2l17qP2OscZsRssaYwarGkF1mxs88XAbPmZ5eqx3CUykfCqZlYEk8d\nmIJkMMs+zAuo4QBf84XXlxQT8aZyM2hNsUolquqwkcYA1F+ut+0z4IrDQPp+rBLN\npBvU9L5LxQKBgQCtm+pliZ8XVBhlRICDJ1WmO+XRh5I2hAWORIBn/3Qc+kmTxXSJ\n/O2UCfogMeyuambfB00uB+VHJeXc3L/QWvrN1iEDQcrC6+DYMKsa5f415wvCs9FE\naow3jK6ts1OSg7faNuEuImBnLaZtM3NNQQYY9LlWT4TshpIKDeFQpN47LQKBgHRe\nfqTaNxKherBzg8X4Hzsrow3a40U0F18Fd/mkROgyFTNbg9+LtuA23NsHB4AfHJg5\nIyu4Gjt2H20WWhynQDGM+tQLiIWaG92zvermCJ7UgIjwMztdjC523tcco8/rxhPw\njz7ufHoe29/a5fLA66aFucOhrxHcHvFMsvselx0VAoGAI7i7M5cZGi++nkLmqTVm\n8TDUJsr/jk3g5XIw9RlRAY4yl+G21SYJkMksuOjzwqCQUgG09LbQKHFZSawuEG08\nA4Sp6pd8xv8G/tiVImEn3tT20CdbNhzcTWbkdYITVFeg+euDFnHfmcEJSMS72non\ng5EZG8eWzc2Cfe/Athh3ZYI=\n-----END PRIVATE KEY-----\n",
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

@app.route('/api/comment', methods=['POST'])
def handle_submit():
    data = request.get_json()
    print(f'Nom: {data["name"]}')
    print(f'Email: {data["email"]}')
    print(f'Commentaire: {data["comment"]}')

    random_number = numpy.random.randint(100)
    print("hello", random_number)

    return jsonify({"message": "Comment received", "random_number": random_number}), 200


@app.route('/api/getData', methods=['GET'])
def get_data():
    # Récupérez les données de Firestore
    data_ref = db.collection('testimonials')
    data = data_ref.get()

    # Transformez les données en format JSON
    result = [item.to_dict() for item in data]

    return jsonify(result), 200

if __name__ == '__main__':
    app.run(debug=True)
