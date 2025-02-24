from dotenv import load_dotenv
import os

load_dotenv()

print(type(os.getenv('ASTRA_ENDPONT')))