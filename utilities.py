import json

def read_json(file_path):
    with open(file_path, "r") as file:
        return json.load(file)

def save_json(data, file_path, indent=4):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=indent)
    print(f"Data saved to {file_path}")