import json

def save_game(path: str, data: dict):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_game(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)
