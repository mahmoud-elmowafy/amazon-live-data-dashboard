import os
import requests
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()

API_KEY = os.getenv("EASYPARSER_API_KEY")

BASE_URL = "https://realtime.easyparser.com/v1/request"

ASIN = "B0HDB6MTYJ"

params = {
    "api_key": API_KEY,
    "platform": "AMZ",
    "operation": "DETAIL",
    "asin": ASIN,
    "domain": ".com",
}

response = requests.get(
    BASE_URL,
    params=params,
    timeout=30
)

response.raise_for_status()

data = response.json()

print("Request Info:")
print(data["request_info"])

print("\nProduct Title:")
print(data["result"]["detail"]["title"])

print("\nPrice:")
print(data["result"]["detail"]["buybox_winner"]["price"]["value"])

print("\nRating:")
print(data["result"]["detail"]["rating"])

print("\nRatings Count:")
print(data["result"]["detail"]["ratings_total"])