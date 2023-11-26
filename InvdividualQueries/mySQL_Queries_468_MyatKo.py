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
#  Query 4: Frequently Bought items
#                 SELECT
#                   p.product_category_name AS product_category_name,
#                   COUNT(oi.order_id) AS order_count
#                   FROM olist_db.olist_order_items_dataset oi
#                   JOIN olist_db.olist_products_dataset p ON oi.product_id = p.product_id
#                   GROUP BY
#                   p.product_category_name
#                   ORDER BY
#                   order_count DESC;
#
#
# # Query 6: Payment Type Distribution
#                 SELECT payment_type, COUNT(order_id) AS payment_count
#                 FROM olist_order_payments_dataset
#                 GROUP BY payment_type
#                 ORDER BY payment_count DESC;
#
#
# # Query 8: Average delivery time and freight fee
#                 SELECT
#                     ROUND(AVG(average_delivery_time),2) AS overall_average_delivery_time,
#                     ROUND(AVG(average_delivery_fee),2) AS overall_average_delivery_fee
#                 FROM (
#                     SELECT
#                         OI.order_id,
#                         AVG(TIMESTAMPDIFF(SECOND, O.order_delivered_carrier_date, O.order_delivered_customer_date) / 3600) AS average_delivery_time,
#                         AVG(OI.freight_value) AS average_delivery_fee
#                     FROM olist_order_items_dataset OI
#                     JOIN olist_orders_dataset O ON OI.order_id = O.order_id
#                     WHERE O.order_status = 'delivered'
#                     GROUP BY OI.order_id
#                 ) AS subquery;
#             """
