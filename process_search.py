import json
import pandas as pd

# =========================
# Load Search Results
# =========================

input_path = "data/search_results.json"
output_path = "data/amazon_search_results.csv"

with open(input_path, "r", encoding="utf-8") as file:
    data = json.load(file)

# =========================
# Extract Products
# =========================

results = data["result"]["search_results"]

products = []

for item in results:
    products.append({
        "asin": item.get("asin"),
        "title": item.get("title"),
        "price": item.get("price"),
        "rating": item.get("rating"),
        "ratings_count": item.get("ratings_total"),
        "position": item.get("position"),
        "is_sponsored": item.get("is_sponsored"),
        "prime": item.get("prime"),
        "bought_activity": item.get("bought_activity"),
        "color_options": item.get("color_options"),
    })

# =========================
# Create DataFrame
# =========================

df = pd.DataFrame(products)

# =========================
# Save CSV
# =========================

df.to_csv(
    output_path,
    index=False,
    encoding="utf-8-sig"
)

print("Search results processed successfully!")
print()
print(df.to_string(index=False))
print()
print(f"Total products: {len(df)}")
print(f"Saved to: {output_path}")