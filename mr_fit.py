import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()

BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "29e1dce7-c2c4-405b-a755-805125c964cd"
APPLICATION_TOKEN = os.environ.get("APP_TOKEN")
ADVICE_ENDPOINT = "prompt" 
CALORIE_ENDPOINT = "BigBoi" 

def advice_mr_fit(message: str, profile) -> dict:

    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{ADVICE_ENDPOINT}"
    
    tweaks = {
        "TextInput-cALOk": {
            "input_value":profile
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
        "input_value": goals
    },
    "TextInput-UDBJa": {
        "input_value": profile
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
    }

    headers = {"Authorization": "Bearer " + APPLICATION_TOKEN, "Content-Type": "application/json"}
    response = requests.post(api_url, json=payload, headers=headers)
    return json.loads(response.json()["outputs"][0]["outputs"][0]["results"]["text"]["data"]["text"])
 
                               