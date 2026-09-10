import pandas as pd
import ast

# =========================
# File Paths
# =========================

input_path = "data/amazon_search_results.csv"
output_path = "data/amazon_search_clean.csv"


# =========================
# Load Data
# =========================

df = pd.read_csv(input_path)


# =========================
# Helper Function
# Convert Dictionary Text
# =========================

def parse_dict(value):
    if pd.isna(value):
        return {}

    try:
        return ast.literal_eval(str(value))
    except (ValueError, SyntaxError):
        return {}


# =========================
# Clean Price
# =========================

def extract_price(value):
    data = parse_dict(value)

    if isinstance(data, dict):
        price = data.get("value")

        try:
            return float(price)
        except (ValueError, TypeError):
            return None

    return None


df["price"] = df["price"].apply(extract_price)


# =========================
# Clean Bought Activity
# =========================

def extract_bought(value):
    data = parse_dict(value)

    if isinstance(data, dict):
        bought = data.get("value")

        try:
            return float(bought)
        except (ValueError, TypeError):
            return None

    return None


df["bought_last_month"] = df["bought_activity"].apply(extract_bought)

df.drop(
    columns=["bought_activity"],
    inplace=True
)


# =========================
# Clean Color Options
# =========================

def extract_colors(value):
    data = parse_dict(value)

    if isinstance(data, dict):
        colors = data.get("total_count")

        try:
            return int(colors)
        except (ValueError, TypeError):
            return 0

    return 0


df["color_options_count"] = df["color_options"].apply(extract_colors)

df.drop(
    columns=["color_options"],
    inplace=True
)


# =========================
# Clean Numeric Columns
# =========================

df["price"] = pd.to_numeric(
    df["price"],
    errors="coerce"
)

df["rating"] = pd.to_numeric(
    df["rating"],
    errors="coerce"
)

df["ratings_count"] = pd.to_numeric(
    df["ratings_count"],
    errors="coerce"
)

df["position"] = pd.to_numeric(
    df["position"],
    errors="coerce"
)

df["bought_last_month"] = pd.to_numeric(
    df["bought_last_month"],
    errors="coerce"
)

df["color_options_count"] = pd.to_numeric(
    df["color_options_count"],
    errors="coerce"
)


# =========================
# Convert Boolean Columns
# =========================

df["is_sponsored"] = df["is_sponsored"].astype(bool)


# =========================
# Remove Duplicate ASINs
# =========================

df.drop_duplicates(
    subset=["asin"],
    keep="first",
    inplace=True
)


# =========================
# Sort by Search Position
# =========================

df.sort_values(
    by="position",
    inplace=True
)


# =========================
# Reset Index
# =========================

df.reset_index(
    drop=True,
    inplace=True
)


# =========================
# Add Analysis Columns
# =========================

# Price category
def price_category(price):
    if pd.isna(price):
        return "Unknown"
    elif price < 20:
        return "Budget"
    elif price < 50:
        return "Mid-Range"
    else:
        return "Premium"


df["price_category"] = df["price"].apply(
    price_category
)


# Rating category
def rating_category(rating):
    if pd.isna(rating):
        return "Unknown"
    elif rating >= 4.5:
        return "Excellent"
    elif rating >= 4.0:
        return "Good"
    else:
        return "Average"


df["rating_category"] = df["rating"].apply(
    rating_category
)


# =========================
# Final Column Order
# =========================

columns = [
    "asin",
    "title",
    "price",
    "rating",
    "ratings_count",
    "position",
    "is_sponsored",
    "prime",
    "bought_last_month",
    "color_options_count",
    "price_category",
    "rating_category"
]

df = df[columns]


# =========================
# Save Clean CSV
# =========================

df.to_csv(
    output_path,
    index=False,
    encoding="utf-8-sig"
)


# =========================
# Display Results
# =========================

print("========================================")
print("DATA CLEANING COMPLETED")
print("========================================")
print()

print(df.to_string(index=False))

print()
print("========================================")
print(f"Total unique products: {len(df)}")
print(f"Products with price: {df['price'].notna().sum()}")
print(f"Products with rating: {df['rating'].notna().sum()}")
print(f"Sponsored products: {df['is_sponsored'].sum()}")
print(f"Organic products: {(~df['is_sponsored']).sum()}")
print("========================================")
print()
print(f"Saved to: {output_path}")