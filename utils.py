import hashlib
import json

def sha256(data):
    if isinstance(data, dict):
        data = json.dumps(data, sort_keys=True)
    elif not isinstance(data, str):
        data = str(data)
    return hashlib.sha256(data.encode()).hexdigest()

def pretty_json(data):
    return json.dumps(data, indent=4, sort_keys=True)