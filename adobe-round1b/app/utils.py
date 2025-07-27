import json
from datetime import datetime

def load_input(input_path):
    with open(input_path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_output(output_path, data):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def get_timestamp():
    return datetime.now().isoformat()
