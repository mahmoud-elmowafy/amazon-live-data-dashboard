import sqlite3
import pandas as pd

# =========================
# Database
# =========================

db_path = "data/amazon_analysis.db"

connection = sqlite3.connect(db_path)


def run_query(title, query):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)

    result = pd.read_sql_query(query, connection)

    print(result.to_string(index=False))

    return result


# =========================
# 1. Average Price
# =========================

run_query(
    "1. AVERAGE PRICE",
    """
    SELECT
        ROUND(AVG(price), 2) AS average_price
    FROM amazon_products
    WHERE price IS NOT NULL;
    """
)


# =========================
# 2. Cheapest Products
# =========================

run_query(
    "2. TOP 5 CHEAPEST PRODUCTS",
    """
    SELECT
        title,
        price,
        rating
    FROM amazon_products
    WHERE price IS NOT NULL
    ORDER BY price ASC
    LIMIT 5;
    """
)


# =========================
# 3. Most Expensive Products
# =========================

run_query(
    "3. TOP 5 MOST EXPENSIVE PRODUCTS",
    """
    SELECT
        title,
        price,
        rating
    FROM amazon_products
    WHERE price IS NOT NULL
    ORDER BY price DESC
    LIMIT 5;
    """
)


# =========================
# 4. Highest Rated Products
# =========================

run_query(
    "4. TOP 5 HIGHEST RATED PRODUCTS",
    """
    SELECT
        title,
        rating,
        ratings_count,
        price
    FROM amazon_products
    WHERE rating IS NOT NULL
    ORDER BY rating DESC, ratings_count DESC
    LIMIT 5;
    """
)


# =========================
# 5. Most Reviewed Products
# =========================

run_query(
    "5. TOP 5 MOST REVIEWED PRODUCTS",
    """
    SELECT
        title,
        ratings_count,
        rating,
        price
    FROM amazon_products
    WHERE ratings_count IS NOT NULL
    ORDER BY ratings_count DESC
    LIMIT 5;
    """
)


# =========================
# 6. Sponsored vs Organic
# =========================

run_query(
    "6. SPONSORED VS ORGANIC",
    """
    SELECT
        CASE
            WHEN is_sponsored = 1 THEN 'Sponsored'
            ELSE 'Organic'
        END AS product_type,

        COUNT(*) AS product_count,

        ROUND(AVG(price), 2) AS average_price,

        ROUND(AVG(rating), 2) AS average_rating

    FROM amazon_products

    GROUP BY is_sponsored;
    """
)


# =========================
# 7. Price Categories
# =========================

run_query(
    "7. PRICE CATEGORY PERFORMANCE",
    """
    SELECT
        price_category,

        COUNT(*) AS product_count,

        ROUND(AVG(price), 2) AS average_price,

        ROUND(AVG(rating), 2) AS average_rating

    FROM amazon_products

    GROUP BY price_category

    ORDER BY average_price;
    """
)


# =========================
# 8. Rating Categories
# =========================

run_query(
    "8. RATING CATEGORY DISTRIBUTION",
    """
    SELECT
        rating_category,

        COUNT(*) AS product_count

    FROM amazon_products

    GROUP BY rating_category

    ORDER BY product_count DESC;
    """
)


# =========================
# 9. Most Bought Products
# =========================

run_query(
    "9. TOP PRODUCTS BY BUYING ACTIVITY",
    """
    SELECT
        title,
        bought_last_month,
        price,
        rating

    FROM amazon_products

    WHERE bought_last_month IS NOT NULL

    ORDER BY bought_last_month DESC

    LIMIT 5;
    """
)


# =========================
# 10. Best Search Positions
# =========================

run_query(
    "10. TOP SEARCH POSITIONS",
    """
    SELECT
        position,
        title,
        price,
        rating,
        is_sponsored

    FROM amazon_products

    ORDER BY position ASC

    LIMIT 10;
    """
)


# =========================
# 11. Products with 4.5+ Rating
# =========================

run_query(
    "11. PRODUCTS WITH RATING 4.5+",
    """
    SELECT
        title,
        price,
        rating,
        ratings_count

    FROM amazon_products

    WHERE rating >= 4.5

    ORDER BY rating DESC, ratings_count DESC;
    """
)


# =========================
# 12. Products with 10K+ Buying Activity
# =========================

run_query(
    "12. PRODUCTS WITH 10K+ BUYING ACTIVITY",
    """
    SELECT
        title,
        price,
        rating,
        bought_last_month

    FROM amazon_products

    WHERE bought_last_month >= 10000

    ORDER BY rating DESC;
    """
)


# =========================
# 13. Best Value Products
# =========================

run_query(
    "13. BEST VALUE PRODUCTS",
    """
    SELECT
        title,
        price,
        rating,
        ratings_count

    FROM amazon_products

    WHERE price IS NOT NULL
      AND rating IS NOT NULL
      AND rating >= 4.5

    ORDER BY price ASC, rating DESC

    LIMIT 10;
    """
)


# =========================
# 14. Products with Many Reviews
# =========================

run_query(
    "14. PRODUCTS WITH 50K+ REVIEWS",
    """
    SELECT
        title,
        ratings_count,
        rating,
        price

    FROM amazon_products

    WHERE ratings_count >= 50000

    ORDER BY ratings_count DESC;
    """
)


# =========================
# 15. Overall Summary
# =========================

run_query(
    "15. OVERALL DATASET SUMMARY",
    """
    SELECT

        COUNT(*) AS total_products,

        ROUND(AVG(price), 2) AS average_price,

        ROUND(MIN(price), 2) AS minimum_price,

        ROUND(MAX(price), 2) AS maximum_price,

        ROUND(AVG(rating), 2) AS average_rating,

        ROUND(MIN(rating), 2) AS minimum_rating,

        ROUND(MAX(rating), 2) AS maximum_rating

    FROM amazon_products;
    """
)


# =========================
# Close Database
# =========================

connection.close()

print("\n" + "=" * 70)
print("SQL ANALYSIS COMPLETED SUCCESSFULLY")
print("=" * 70)