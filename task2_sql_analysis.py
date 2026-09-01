import os
import sqlite3
import pandas as pd

# Create output folder
output_folder = "../reports/task2"
os.makedirs(output_folder, exist_ok=True)

# Load cleaned dataset
df = pd.read_csv("../data/cleaned_orders.csv")

# Create a temporary SQLite database
connection = sqlite3.connect(":memory:")
df.to_sql("orders", connection, index=False, if_exists="replace")

# SQL business questions
queries = {
    "1. Monthly Revenue": """
        SELECT order_month,
               ROUND(SUM(revenue_inr), 2) AS total_revenue
        FROM orders
        GROUP BY order_month
        ORDER BY order_month;
    """,

    "2. Top 5 Products by Revenue": """
        SELECT product_name,
               ROUND(SUM(revenue_inr), 2) AS total_revenue
        FROM orders
        GROUP BY product_name
        ORDER BY total_revenue DESC
        LIMIT 5;
    """,

    "3. Revenue by Region": """
        SELECT region,
               ROUND(SUM(revenue_inr), 2) AS total_revenue
        FROM orders
        GROUP BY region
        ORDER BY total_revenue DESC;
    """,

    "4. Revenue by Acquisition Channel": """
        SELECT acquisition_channel,
               ROUND(SUM(revenue_inr), 2) AS total_revenue,
               COUNT(*) AS total_orders
        FROM orders
        GROUP BY acquisition_channel
        ORDER BY total_revenue DESC;
    """,

    "5. Return Rate by Category": """
        SELECT category,
               COUNT(*) AS total_orders,
               SUM(CASE WHEN order_status = 'Returned' THEN 1 ELSE 0 END) AS returned_orders,
               ROUND(
                   SUM(CASE WHEN order_status = 'Returned' THEN 1 ELSE 0 END)
                   * 100.0 / COUNT(*), 2
               ) AS return_rate_percent
        FROM orders
        GROUP BY category
        ORDER BY return_rate_percent DESC;
    """,

    "6. Repeat Customers": """
        SELECT customer_id,
               COUNT(*) AS total_orders,
               ROUND(SUM(revenue_inr), 2) AS lifetime_revenue
        FROM orders
        GROUP BY customer_id
        HAVING COUNT(*) > 1
        ORDER BY lifetime_revenue DESC
        LIMIT 10;
    """
}

# Save SQL queries and results
sql_file = f"{output_folder}/task2_sql_queries.sql"
result_file = f"{output_folder}/sql_query_results.txt"

with open(sql_file, "w") as sql_output, open(result_file, "w") as result_output:
    for title, query in queries.items():
        result = pd.read_sql_query(query, connection)

        sql_output.write(f"-- {title}\n{query}\n\n")
        result_output.write(f"\n{'=' * 60}\n{title}\n{'=' * 60}\n")
        result_output.write(query)
        result_output.write("\nRESULT:\n")
        result_output.write(result.to_string(index=False))
        result_output.write("\n\n")

        print(title)
        print(result)
        print()

connection.close()

print("SQL queries and results were saved successfully.")