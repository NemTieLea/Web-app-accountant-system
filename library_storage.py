import json
import os

LIBRARY_FILE = "lib.json"


def load_state():
    if not os.path.isfile(LIBRARY_FILE):
        return {
            "caly_stan": 0,
            "historia": [],
            "slownik_produktow": {
                "Rower": 10,
                "Srubokret": 13,
                "Opony": 22,
                "Detki": 6,
                "Hulajnoga": 8,
                "Pompka": 20,
            },
            "cena_produktow": {
                "Rower": 980,
                "Srubokret": 30,
                "Opony": 60,
                "Detki": 29,
                "Hulajnoga": 1400,
                "Pompka": 55,
            }
        }

    try:
        with open(LIBRARY_FILE, 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"Error loading {LIBRARY_FILE}. Initializing with default state.")
        data = {
            "caly_stan": 0,
            "historia": [],
            "slownik_produktow": {
                "Rower": 10,
                "Srubokret": 13,
                "Opony": 22,
                "Detki": 6,
                "Hulajnoga": 8,
                "Pompka": 20,
            },
            "cena_produktow": {
                "Rower": 980,
                "Srubokret": 30,
                "Opony": 60,
                "Detki": 29,
                "Hulajnoga": 1400,
                "Pompka": 55,
            }
        }

    return data


def save_state(state):
    with open(LIBRARY_FILE, 'w') as file:
        json.dump(state, file, indent=4)
