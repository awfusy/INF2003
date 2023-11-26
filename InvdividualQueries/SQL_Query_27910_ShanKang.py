import paramiko
import mysql.connector	
from mysql.connector import connect, Error
import sshtunnel
import time

# SSH Configuration
ssh_host = '35.212.230.135'
ssh_port = 22
ssh_user = 'dev'
ssh_password = 'Inf2003dev'

# MySQL Configuration
mysql_host = 'localhost'  # or the IP address of your MySQL server
mysql_port = 3306
mysql_user = 'sqluser'
mysql_password = 'Inf2003user'
mysql_database = 'olist_db'

# Establish SSH connection
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())


ssh_client.connect(ssh_host, ssh_port, ssh_user, ssh_password)
print("SSH Connection Established")

# Establish MySQL connection through SSH tunnel
tunnel = sshtunnel.SSHTunnelForwarder(
        (ssh_host, ssh_port),
        ssh_username=ssh_user,
        ssh_password=ssh_password,
        remote_bind_address=(mysql_host, mysql_port),
)
tunnel.start()
print("SSH Tunnel Established")

connection = mysql.connector.connect(
        user=mysql_user,
        host=mysql_host,
        port=tunnel.local_bind_port,
        password=mysql_password,
        database=mysql_database,
        use_pure=True,  
                
)
print("MySQL Connection Established")

# MySQL query 2
query_2 = "SELECT p.product_category_name, COUNT(DISTINCT oi.order_id) AS Num_orders, SUM(oi.price) AS Revenue \
FROM olist_order_items_dataset oi \
JOIN olist_products_dataset p ON oi.product_id = p.product_id \
JOIN olist_orders_dataset o ON oi.order_id = o.order_id \
WHERE o.order_status <> 'canceled' AND o.order_delivered_customer_date IS NOT NULL \
GROUP BY p.product_category_name \
ORDER BY Revenue DESC; \
"

query_7 = "SELECT AVG(TIMESTAMPDIFF(SECOND, order_purchase_timestamp , order_approved_at))/3600 AS average_processing_time, \
AVG(TIMESTAMPDIFF(SECOND, order_delivered_carrier_date, order_delivered_customer_date))/3600 AS average_shipping_time \
FROM olist_db.olist_orders_dataset \
WHERE order_status = 'delivered'; \
"

query_9 = "SELECT P.product_category_name, AVG(R.review_score) AS average \
FROM olist_db.olist_order_reviews_dataset R \
JOIN olist_db.olist_order_items_dataset I on R.order_id = I.order_id \
JOIN olist_db.olist_products_dataset P on I.product_id = P.product_id \
GROUP BY P.product_category_name \
ORDER BY average DESC; \
"

query_10 = "SELECT P.product_category_name, COUNT(DISTINCT S.seller_id) \
FROM olist_db.olist_products_dataset P \
JOIN olist_db.olist_order_items_dataset I ON P.product_id = I.product_id \
JOIN olist_db.olist_sellers_dataset S ON I.seller_id = S.seller_id \
GROUP BY product_category_name \
ORDER BY COUNT(DISTINCT S.seller_id) DESC \
LIMIT 10; \
"

cursor = connection.cursor()
cursor.execute(query_2)
result = cursor.fetchall()
for r in result:
    print(r)

cursor.close()
connection.close()
ssh_client.close()
