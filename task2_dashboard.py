import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load cleaned data
df = pd.read_csv("../data/cleaned_orders.csv")
df["order_date"] = pd.to_datetime(df["order_date"])
df["order_month"] = df["order_date"].dt.to_period("M").astype(str)

# KPI calculations
total_orders = len(df)
total_revenue = df["revenue_inr"].sum()
average_order_value = df["revenue_inr"].mean()
return_rate = (df["order_status"] == "Returned").mean() * 100

# Chart data
monthly_revenue = df.groupby("order_month")["revenue_inr"].sum()
category_revenue = df.groupby("category")["revenue_inr"].sum().sort_values()
region_revenue = df.groupby("region")["revenue_inr"].sum().sort_values()
channel_revenue = df.groupby("acquisition_channel")["revenue_inr"].sum().sort_values()

# Dashboard layout
sns.set_theme(style="whitegrid")
fig, axes = plt.subplots(2, 2, figsize=(16, 10))
fig.subplots_adjust(top=0.72, hspace=0.45, wspace=0.30)

# Title
fig.suptitle("E-Commerce Sales Dashboard - Task 2",
             fontsize=22, fontweight="bold", color="#0F766E")

# KPI cards
card_style = dict(
    boxstyle="round,pad=0.7",
    facecolor="#D1FAE5",
    edgecolor="#0F766E"
)

fig.text(0.13, 0.84, f"Total Orders\n{total_orders:,}",
         ha="center", va="center", fontsize=14, fontweight="bold",
         bbox=card_style)

fig.text(0.38, 0.84, f"Total Revenue\nINR {total_revenue:,.0f}",
         ha="center", va="center", fontsize=14, fontweight="bold",
         bbox=card_style)

fig.text(0.63, 0.84, f"Average Order Value\nINR {average_order_value:,.0f}",
         ha="center", va="center", fontsize=14, fontweight="bold",
         bbox=card_style)

fig.text(0.82, 0.84, f"Return Rate\n{return_rate:.1f}%",
         ha="center", va="center", fontsize=14, fontweight="bold",
         bbox=card_style)

# Chart 1: Monthly revenue
axes[0, 0].plot(monthly_revenue.index, monthly_revenue.values,
                marker="o", color="#0F766E")
axes[0, 0].set_title("Monthly Revenue Trend")
axes[0, 0].set_xlabel("Month")
axes[0, 0].set_ylabel("Revenue (INR)")
axes[0, 0].tick_params(axis="x", rotation=45)

# Chart 2: Category revenue
axes[0, 1].barh(category_revenue.index, category_revenue.values,
                color="#2563EB")
axes[0, 1].set_title("Revenue by Category")
axes[0, 1].set_xlabel("Revenue (INR)")

# Chart 3: Region revenue
axes[1, 0].bar(region_revenue.index, region_revenue.values,
               color="#EA580C")
axes[1, 0].set_title("Revenue by Region")
axes[1, 0].set_xlabel("Region")
axes[1, 0].set_ylabel("Revenue (INR)")

# Chart 4: Acquisition channel revenue
axes[1, 1].barh(channel_revenue.index, channel_revenue.values,
                color="#7C3AED")
axes[1, 1].set_title("Revenue by Acquisition Channel")
axes[1, 1].set_xlabel("Revenue (INR)")

# Save dashboard image
plt.savefig("../reports/task2/task2_static_dashboard.png",
            dpi=300, bbox_inches="tight")

print("Task 2 dashboard created successfully.")