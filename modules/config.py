import numpy as np
import os
from dotenv import load_dotenv, find_dotenv

def load_configurations():
    """
    Charge uniquement les variables du fichier .env si celui-ci est présent.
    Si le fichier .env n'existe pas, charge toutes les variables d'environnement du système.
    """
    dotenv_path = find_dotenv('.env')

    if dotenv_path:
        # Le fichier .env existe, charger uniquement ses variables
        load_dotenv(dotenv_path)
        # Retourne les variables chargées depuis le .env
        return {key: os.environ[key] for key in os.environ if key in open(dotenv_path).read()}
    else:
        # Le fichier .env n'existe pas, retourne toutes les variables d'environnement du système
        return dict(os.environ)

### CREDENTIALS ###
def firebase_credentials():
    '''
    Load configuration from .env file or from OS environment variables
    '''
    
    # List of required keys in lowercase
    keys_list = [
        'project_id', 'private_key_id', 'private_key', 'client_email',
        'client_id', 'auth_uri', 'token_uri', 'auth_provider_x509_cert_url',
        'client_x509_cert_url'
    ]
    
    cred_dict = {}
    env_variables = load_configurations()

    # Check if all required keys exist and have a non-empty value
    try:
        for key in keys_list:
            value = env_variables.get(key.upper())
            if not value:
                raise ValueError(f'Missing or empty value for key: {key.upper()}')
            cred_dict[key] = value

        # Add prefix and suffix for the private_key
        cred_dict['private_key'] = cred_dict["private_key"].replace("/breakline/", "\n")
    except ValueError as e:
        print(f'Configuration error: {e}')
        cred_dict = {}  # Reset cred_dict if any key is missing or empty

    return cred_dict
