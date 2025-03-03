import json
from openai import OpenAI

def conn_openai(key_file='key.json'):
    try:
        with open(key_file) as f:
            key_data = json.load(f)
            api_key = key_data['api_key']
            print("API key loaded successfully")
    except FileNotFoundError:
        raise Exception(f"{key_file} not found. Please create it from key.json.example")
    except KeyError:
        raise Exception(f"Invalid {key_file} format. Should contain 'api_key' field")

    client = OpenAI(api_key=api_key)
    return client