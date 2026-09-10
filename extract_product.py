import os
import requests
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime


# =========================
# Load environment variables
# =========================
load_dotenv()

API_KEY = os.getenv("EASYPARSER_API_KEY")
BASE_URL = "https://realtime.easyparser.com/v1/request"


# =========================
# Amazon Product
# =========================
ASIN = "B0HDB6MTYJ"


# =========================
# API Parameters
# =========================
params = {
    "api_key": API_KEY,
    "platform": "AMZ",
    "operation": "DETAIL",
    "asin": ASIN,
    "domain": ".com",
}


# =========================
# Send API Request
# =========================
response = requests.get(
    BASE_URL,
    params=params,
    timeout=30
)

response.raise_for_status()

data = response.json()
detail = data["result"]["detail"]


# =========================
# Extract Prices
# =========================
prices = detail.get("buybox_winner", {}).get("prices", [])

regular_price = None

for price_item in prices:
    if price_item.get("type") == "Regular Price":
        regular_price = price_item.get("value")
        break


# =========================
# Extract Availability
# =========================
availability = detail.get(
    "buybox_winner",
    {}
).get(
    "availability",
    {}
)


# =========================
# Build Product Record
# =========================
product = {
    "asin": ASIN,
    "title": detail.get("title"),
    "brand": detail.get("brand"),

    "price": detail.get(
        "buybox_winner",
        {}
    ).get(
        "price",
        {}
    ).get(
        "value"
    ),

    "regular_price": regular_price,

    "rating": detail.get("rating"),

    "ratings_count": detail.get(
        "ratings_total",
        detail.get("rating_count")
    ),

    "availability": availability.get("raw"),

    "stock_quantity": availability.get("stock_data"),

    "collected_at": datetime.now().isoformat()
}


# =========================
# Convert to DataFrame
# =========================
df = pd.DataFrame([product])


# =========================
# Save Dataset
# =========================
output_path = "data/amazon_products.csv"

df.to_csv(
    output_path,
    index=False,
    encoding="utf-8-sig"
)


# =========================
# Display Results
# =========================
print("Data extracted successfully!")
print()
print(df.to_string(index=False))
print()
print(f"Saved to: {output_path}")