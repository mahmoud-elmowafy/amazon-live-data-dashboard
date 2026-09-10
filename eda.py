import pandas as pd

# =========================
# Load Clean Data
# =========================

input_path = "data/amazon_search_clean.csv"

df = pd.read_csv(input_path)


# =========================
# Basic Information
# =========================

print("=" * 60)
print("AMAZON WIRELESS EARBUDS - DATA ANALYSIS")
print("=" * 60)

print("\nDataset Shape:")
print(f"Rows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")


# =========================
# Missing Values
# =========================

print("\n" + "=" * 60)
print("MISSING VALUES")
print("=" * 60)

missing = df.isnull().sum()

print(missing[missing > 0])


# =========================
# Price Analysis
# =========================

print("\n" + "=" * 60)
print("PRICE ANALYSIS")
print("=" * 60)

print(f"Average Price: ${df['price'].mean():.2f}")
print(f"Minimum Price: ${df['price'].min():.2f}")
print(f"Maximum Price: ${df['price'].max():.2f}")
print(f"Median Price: ${df['price'].median():.2f}")


# =========================
# Rating Analysis
# =========================

print("\n" + "=" * 60)
print("RATING ANALYSIS")
print("=" * 60)

print(f"Average Rating: {df['rating'].mean():.2f}")
print(f"Minimum Rating: {df['rating'].min():.2f}")
print(f"Maximum Rating: {df['rating'].max():.2f}")


# =========================
# Top Rated Products
# =========================

print("\n" + "=" * 60)
print("TOP 5 RATED PRODUCTS")
print("=" * 60)

top_rated = (
    df[df["ratings_count"].notna()]
    .sort_values(
        by=["rating", "ratings_count"],
        ascending=[False, False]
    )
    .head(5)
)

for _, row in top_rated.iterrows():
    print(
        f"\n{row['title'][:80]}"
        f"\nRating: {row['rating']}"
        f" | Ratings: {int(row['ratings_count'])}"
        f" | Price: ${row['price'] if pd.notna(row['price']) else 'N/A'}"
    )


# =========================
# Most Reviewed Products
# =========================

print("\n" + "=" * 60)
print("TOP 5 PRODUCTS BY RATINGS COUNT")
print("=" * 60)

most_reviewed = (
    df[df["ratings_count"].notna()]
    .sort_values(
        by="ratings_count",
        ascending=False
    )
    .head(5)
)

for _, row in most_reviewed.iterrows():
    print(
        f"\n{row['title'][:80]}"
        f"\nRatings: {int(row['ratings_count'])}"
        f" | Rating: {row['rating']}"
        f" | Price: ${row['price'] if pd.notna(row['price']) else 'N/A'}"
    )


# =========================
# Cheapest Products
# =========================

print("\n" + "=" * 60)
print("TOP 5 CHEAPEST PRODUCTS")
print("=" * 60)

cheapest = (
    df[df["price"].notna()]
    .sort_values(
        by="price",
        ascending=True
    )
    .head(5)
)

for _, row in cheapest.iterrows():
    print(
        f"\n{row['title'][:80]}"
        f"\nPrice: ${row['price']:.2f}"
        f" | Rating: {row['rating']}"
    )


# =========================
# Most Expensive Products
# =========================

print("\n" + "=" * 60)
print("TOP 5 MOST EXPENSIVE PRODUCTS")
print("=" * 60)

most_expensive = (
    df[df["price"].notna()]
    .sort_values(
        by="price",
        ascending=False
    )
    .head(5)
)

for _, row in most_expensive.iterrows():
    print(
        f"\n{row['title'][:80]}"
        f"\nPrice: ${row['price']:.2f}"
        f" | Rating: {row['rating']}"
    )


# =========================
# Price Category Analysis
# =========================

print("\n" + "=" * 60)
print("PRICE CATEGORY DISTRIBUTION")
print("=" * 60)

price_categories = (
    df["price_category"]
    .value_counts()
)

print(price_categories)


# =========================
# Rating Category Analysis
# =========================

print("\n" + "=" * 60)
print("RATING CATEGORY DISTRIBUTION")
print("=" * 60)

rating_categories = (
    df["rating_category"]
    .value_counts()
)

print(rating_categories)


# =========================
# Sponsored vs Organic
# =========================

print("\n" + "=" * 60)
print("SPONSORED VS ORGANIC")
print("=" * 60)

sponsored_count = df["is_sponsored"].sum()
organic_count = (~df["is_sponsored"]).sum()

print(f"Sponsored Products: {sponsored_count}")
print(f"Organic Products: {organic_count}")


# =========================
# Average Price
# Sponsored vs Organic
# =========================

print("\n" + "=" * 60)
print("AVERAGE PRICE: SPONSORED VS ORGANIC")
print("=" * 60)

price_comparison = (
    df.groupby("is_sponsored")["price"]
    .mean()
)

print(
    price_comparison.rename(
        index={
            True: "Sponsored",
            False: "Organic"
        }
    )
)


# =========================
# Average Rating
# Sponsored vs Organic
# =========================

print("\n" + "=" * 60)
print("AVERAGE RATING: SPONSORED VS ORGANIC")
print("=" * 60)

rating_comparison = (
    df.groupby("is_sponsored")["rating"]
    .mean()
)

print(
    rating_comparison.rename(
        index={
            True: "Sponsored",
            False: "Organic"
        }
    )
)


# =========================
# Bought Activity
# =========================

print("\n" + "=" * 60)
print("BUYING ACTIVITY")
print("=" * 60)

bought = df[df["bought_last_month"].notna()]

if not bought.empty:

    print(
        f"Average bought activity: "
        f"{bought['bought_last_month'].mean():.0f}"
    )

    print(
        f"Maximum bought activity: "
        f"{bought['bought_last_month'].max():.0f}"
    )

    print("\nTop 5 by buying activity:")

    top_bought = (
        bought.sort_values(
            by="bought_last_month",
            ascending=False
        )
        .head(5)
    )

    for _, row in top_bought.iterrows():
        print(
            f"\n{row['title'][:80]}"
            f"\nBought: {int(row['bought_last_month'])}+"
            f" | Price: ${row['price'] if pd.notna(row['price']) else 'N/A'}"
        )

else:
    print("No buying activity data available.")


# =========================
# Position Analysis
# =========================

print("\n" + "=" * 60)
print("SEARCH POSITION ANALYSIS")
print("=" * 60)

position_data = df[df["position"].notna()]

print(
    f"Best Search Position: "
    f"{int(position_data['position'].min())}"
)

print(
    f"Worst Search Position: "
    f"{int(position_data['position'].max())}"
)


# =========================
# Correlation Analysis
# =========================

print("\n" + "=" * 60)
print("CORRELATION ANALYSIS")
print("=" * 60)

correlation_columns = [
    "price",
    "rating",
    "ratings_count",
    "position",
    "bought_last_month",
    "color_options_count"
]

correlation = df[correlation_columns].corr()

print(correlation.round(2))


# =========================
# Key Insights
# =========================

print("\n" + "=" * 60)
print("KEY INSIGHTS")
print("=" * 60)

print(
    f"\n1. Average product price is "
    f"${df['price'].mean():.2f}."
)

print(
    f"2. Average product rating is "
    f"{df['rating'].mean():.2f}/5."
)

print(
    f"3. There are "
    f"{sponsored_count} sponsored products "
    f"and {organic_count} organic products."
)

if not bought.empty:
    print(
        f"4. The highest buying activity is "
        f"{int(bought['bought_last_month'].max())}+ "
        f"units in the available data."
    )

print(
    f"5. The cheapest product costs "
    f"${df['price'].min():.2f}."
)

print(
    f"6. The most expensive product costs "
    f"${df['price'].max():.2f}."
)

print(
    f"7. The highest rating in the dataset is "
    f"{df['rating'].max():.1f}/5."
)

print("\n" + "=" * 60)
print("EDA COMPLETED SUCCESSFULLY")
print("=" * 60)