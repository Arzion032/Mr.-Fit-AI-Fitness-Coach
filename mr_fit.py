import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()

BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = os.environ.get("LANGFLOW_ID")
APPLICATION_TOKEN = os.environ.get("APP_TOKEN")
ADVICE_ENDPOINT = os.environ.get("ADVICE_ENDPOINT")
CALORIE_ENDPOINT = os.environ.get("CALORIE_ENDPOINT") 
    
def dict_to_string(obj, level=0):
    strings = []
    indent = "  " * level
    
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, (dict, list)):
                nested_string = dict_to_string(value, level + 1)
                strings.append(f"{indent}{key}:     {nested_string}")
            else:
                strings.append(f"{indent}{key}: {value}")
    elif isinstance(obj,list):
        for idx, item in enumerate(obj):
            nested_string = dict_to_string(item, level = 1)
            strings.append(f"{indent}Item {idx + 1}: {nested_string}")
    else:
        strings.append(f"{indent}{obj}")
        
    return ", ".join(strings)
        
                                

def advice_mr_fit(message: str, profile, name) -> dict:

    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{ADVICE_ENDPOINT}"
    
    tweaks = {
        "TextInput-cALOk": {
            "input_value":dict_to_string(profile)
            },
        "TextInput-yW8Vv": {
            "input_value": name
             }
        }
    
    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
        "tweaks":tweaks
    }

    headers = {"Authorization": "Bearer " + APPLICATION_TOKEN, "Content-Type": "application/json"}
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()["outputs"][0]["outputs"][0]["results"]["message"]["data"]["text"]


def big_boi_macro(profile, goals):
    TWEAKS = {
    "TextInput-mCv8a": {
        "input_value": ", ".join(goals)
    },
    "TextInput-UDBJa": {
        "input_value": dict_to_string(profile)
    },
    }
    return get_macros("", tweaks=TWEAKS)

#
def get_macros(message: str,
            tweaks,
            output_type: str = "chat",
            input_type: str = "chat"):
 
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{CALORIE_ENDPOINT}"

    payload = {
        "input_value": message,
        "output_type": output_type,
        "input_type": input_type,
        "tweaks": tweaks
    }

    headers = {"Authorization": "Bearer " + APPLICATION_TOKEN, "Content-Type": "application/json"}
    response = requests.post(api_url, json=payload, headers=headers)
    print(response.json())
    return json.loads(response.json()["outputs"][0]["outputs"][0]["results"]["text"]["data"]["text"])
 
                               