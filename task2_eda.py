import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Create output folder for Task 2 charts and reports
output_folder = "../reports/task2"
chart_folder = "../reports/task2/charts"

os.makedirs(chart_folder, exist_ok=True)

# Load cleaned dataset from Task 1
df = pd.read_csv("../data/cleaned_orders.csv")

# Prepare date fields
df["order_date"] = pd.to_datetime(df["order_date"])
df["order_month"] = df["order_date"].dt.to_period("M").astype(str)

# Set chart style
sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (10, 6)

# 1. Monthly revenue trend
monthly_revenue = df.groupby("order_month")["revenue_inr"].sum().reset_index()

plt.plot(monthly_revenue["order_month"], monthly_revenue["revenue_inr"],
         marker="o", color="#0F766E")
plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue (INR)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f"{chart_folder}/monthly_revenue.png")
plt.close()

# 2. Revenue by category
category_revenue = (
    df.groupby("category")["revenue_inr"]
    .sum()
    .sort_values(ascending=False)
)

category_revenue.plot(kind="bar", color="#2563EB")
plt.title("Revenue by Product Category")
plt.xlabel("Category")
plt.ylabel("Revenue (INR)")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig(f"{chart_folder}/revenue_by_category.png")
plt.close()

# 3. Top 10 products by revenue
top_products = (
    df.groupby("product_name")["revenue_inr"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

top_products.sort_values().plot(kind="barh", color="#7C3AED")
plt.title("Top 10 Products by Revenue")
plt.xlabel("Revenue (INR)")
plt.ylabel("Product")
plt.tight_layout()
plt.savefig(f"{chart_folder}/top_products.png")
plt.close()

# 4. Revenue by region
region_revenue = (
    df.groupby("region")["revenue_inr"]
    .sum()
    .sort_values(ascending=False)
)

region_revenue.plot(kind="bar", color="#EA580C")
plt.title("Revenue by Region")
plt.xlabel("Region")
plt.ylabel("Revenue (INR)")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(f"{chart_folder}/revenue_by_region.png")
plt.close()

# 5. Revenue by acquisition channel
channel_revenue = (
    df.groupby("acquisition_channel")["revenue_inr"]
    .sum()
    .sort_values(ascending=False)
)

channel_revenue.plot(kind="bar", color="#DC2626")
plt.title("Revenue by Acquisition Channel")
plt.xlabel("Acquisition Channel")
plt.ylabel("Revenue (INR)")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig(f"{chart_folder}/revenue_by_channel.png")
plt.close()

# 6. Correlation heatmap
numeric_columns = [
    "customer_age", "unit_price_inr", "quantity",
    "discount_pct", "shipping_fee_inr", "rating",
    "delivery_days", "revenue_inr"
]

plt.figure(figsize=(10, 7))
sns.heatmap(df[numeric_columns].corr(), annot=True, cmap="YlGnBu", fmt=".2f")
plt.title("Correlation Heatmap")
plt.tight_layout()
plt.savefig(f"{chart_folder}/correlation_heatmap.png")
plt.close()

# Summary statistics
total_revenue = df["revenue_inr"].sum()
average_order_value = df["revenue_inr"].mean()
total_orders = len(df)
delivered_orders = (df["order_status"] == "Delivered").sum()
return_rate = (df["order_status"] == "Returned").mean() * 100

summary = f"""
TASK 2 - EDA SUMMARY

Total Orders: {total_orders}
Total Revenue: INR {total_revenue:,.2f}
Average Order Value: INR {average_order_value:,.2f}
Delivered Orders: {delivered_orders}
Return Rate: {return_rate:.2f}%

Top Product by Revenue: {top_products.index[0]}
Top Category by Revenue: {category_revenue.index[0]}
Top Region by Revenue: {region_revenue.index[0]}
Top Acquisition Channel: {channel_revenue.index[0]}
"""

with open(f"{output_folder}/eda_summary.txt", "w") as file:
    file.write(summary)

print(summary)
print("Charts and EDA summary were saved successfully.")