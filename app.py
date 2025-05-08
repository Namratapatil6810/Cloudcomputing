from flask import Flask, render_template
from google.cloud import bigquery

app = Flask(__name__)
client = bigquery.Client()

# Query 1: Top 5 Products
QUERY_1 = """
SELECT 
  p.name AS product_name,
  p.category,
  ROUND(SUM(oi.sale_price), 2) AS total_revenue
FROM 
  `namratapatil.thelook.order_items` AS oi
JOIN 
  `namratapatil.thelook.products` AS p
  ON oi.product_id = p.id
WHERE 
  DATE(oi.created_at) BETWEEN '2024-01-01' AND '2024-03-31'
GROUP BY 
  p.name, p.category
ORDER BY 
  total_revenue DESC
LIMIT 5;
"""

# Query 2: VIP Customers
QUERY_2 = """
WITH customer_orders AS (
  SELECT 
    oi.user_id,
    oi.order_id,
    SUM(oi.sale_price) AS order_total
  FROM 
    `namratapatil.thelook.order_items` AS oi
  GROUP BY 
    oi.user_id, oi.order_id
)
SELECT 
  u.id AS user_id,
  u.first_name,
  u.last_name,
  COUNT(co.order_id) AS total_orders,
  ROUND(AVG(co.order_total), 2) AS avg_order_value
FROM 
  customer_orders AS co
JOIN 
  `namratapatil.thelook.users` AS u
  ON co.user_id = u.id
GROUP BY 
  u.id, u.first_name, u.last_name
HAVING 
  COUNT(co.order_id) > 3 
  AND AVG(co.order_total) > 100;
"""

def query_to_dict_list(query):
    """Executes a BigQuery query and returns results as a list of dicts"""
    query_job = client.query(query)
    result = query_job.result()
    return [dict(row.items()) for row in result]

@app.route("/")
def index():
    product_data = query_to_dict_list(QUERY_1)
    customer_data = query_to_dict_list(QUERY_2)

    return render_template("index.html", products=product_data, customers=customer_data)

if __name__ == "__main__":
    app.run(debug=True)

