# FROM MYSQL WORKBENCH
#
#  Query 4: Frequently Bought items
#                 SELECT p.product_category_name, COUNT(oi.order_id) AS order_count
#                 FROM olist_order_items_dataset oi
#                 JOIN olist_products_dataset p ON oi.product_id = p.product_id
#                 GROUP BY p.product_category_name
#                 ORDER BY order_count DESC;
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
