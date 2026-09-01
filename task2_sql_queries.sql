-- 1. Monthly Revenue

        SELECT order_month,
               ROUND(SUM(revenue_inr), 2) AS total_revenue
        FROM orders
        GROUP BY order_month
        ORDER BY order_month;
    

-- 2. Top 5 Products by Revenue

        SELECT product_name,
               ROUND(SUM(revenue_inr), 2) AS total_revenue
        FROM orders
        GROUP BY product_name
        ORDER BY total_revenue DESC
        LIMIT 5;
    

-- 3. Revenue by Region

        SELECT region,
               ROUND(SUM(revenue_inr), 2) AS total_revenue
        FROM orders
        GROUP BY region
        ORDER BY total_revenue DESC;
    

-- 4. Revenue by Acquisition Channel

        SELECT acquisition_channel,
               ROUND(SUM(revenue_inr), 2) AS total_revenue,
               COUNT(*) AS total_orders
        FROM orders
        GROUP BY acquisition_channel
        ORDER BY total_revenue DESC;
    

-- 5. Return Rate by Category

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
    

-- 6. Repeat Customers

        SELECT customer_id,
               COUNT(*) AS total_orders,
               ROUND(SUM(revenue_inr), 2) AS lifetime_revenue
        FROM orders
        GROUP BY customer_id
        HAVING COUNT(*) > 1
        ORDER BY lifetime_revenue DESC
        LIMIT 10;
    

