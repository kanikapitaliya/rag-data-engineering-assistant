SELECT
customer_id,
SUM(transaction_amount) AS total_revenue
FROM sales_transactions
GROUP BY customer_id
ORDER BY total_revenue DESC;
