# # Query for: Which location provide the most revenue?
# import pymongo
# from prettytable import PrettyTable
# import time
# start_time = time.time()

# # Step 1: Connect to the MongoDB database
# client = pymongo.MongoClient("mongodb+srv://INF2003:wJL8pGXxgGQzqhaP@inf2003.xqigi2t.mongodb.net/")
# db = client["INF2003"]  # Replace with your database name
# customers_collection = db["customers"]
# orders_collection = db["orders"]
# order_items_collection = db["order_items"]

# # Create indexes
# customers_collection.create_index("customer_id")
# orders_collection.create_index("customer_id")
# order_items_collection.create_index("order_id")
# print(db.list_collection_names())

# # Step 2: Use the aggregation pipeline to join the collections
# pipeline = [
#     {
#         "$lookup": {
#             "from": "orders",
#             "localField": "customer_id",
#             "foreignField": "customer_id",
#             "as": "orders"
#         }
#     },
#     {
#         "$unwind": "$orders"
#     },
#     {
#         "$lookup": {
#             "from": "order_items",
#             "localField": "orders.order_id",
#             "foreignField": "order_id",
#             "as": "order_items"
#         }
#     },
#     {
#         "$unwind": "$order_items"
#     },
#     {
#         "$match": {
#             "orders.order_status": "delivered",
#             "orders.order_delivered_customer_date": {"$ne": None}
#         }
#     },
#     {
#         "$group": {
#             "_id": {
#                 "city": "$customer_city",
#                 "state": "$customer_state"
#             },
#             "total_revenue": {"$sum": "$order_items.price"}
#         }
#     },
#     {
#         "$sort": {"total_revenue": -1}
#     }
# ]


# # Step 3: Execute the aggregation pipeline
# result = list(customers_collection.aggregate(pipeline))

# # Step 4: Create a table to display the results
# table = PrettyTable(["City/State", "Total Revenue"])
# table.align["City/State"] = "l"  # Left-align the City/State column

# # Step 5: Populate the table with the results
# for item in result:
#     city_state = f"{item['_id']['city']}, {item['_id']['state']}"
#     total_revenue = item['total_revenue']
#     table.add_row([city_state, total_revenue])

# # Step 6: Display the table
# print(table)

# # Step 7: Display the city or state with the most revenue
# if result:
#     top_city_state = result[0]["_id"]
#     total_revenue = result[0]["total_revenue"]
#     print(f"The city or state with the most revenue is: {top_city_state}, Total Revenue: {total_revenue}")
# else:
#     print("No data found.")
# end_time = time.time()
# execution_time = end_time - start_time
# print(f"Execution time: {execution_time:.2f} seconds")








# # Query for: Average completion of processing time/ shipping time.
# from pymongo import MongoClient
# from prettytable import PrettyTable
# import time
# start_time = time.time()

# # Connect to the MongoDB database
# client = MongoClient("mongodb+srv://INF2003:wJL8pGXxgGQzqhaP@inf2003.xqigi2t.mongodb.net/")
# db = client["INF2003"]  # Replace with your database name
# orders_collection = db["orders"]

# pipeline = [
#     {
#         "$match": {
#             "order_status": "delivered"  # Filter by the desired order_status
#         },
#     },
#     {
#         "$project": {
#             "order_id": 1,
#             "customer_id": 1,
#             "processing_time": {
#                 "$divide": [
#                     {
#                         "$subtract": [
#                             {"$dateFromString": {"dateString": "$order_approved_at"}},
#                             {"$dateFromString": {"dateString": "$order_purchase_timestamp"}}
#                         ]
#                     },
#                     3600000  # Convert milliseconds to hours
#                 ]
#             },
#             "shipping_time": {
#                 "$divide": [
#                     {
#                         "$subtract": [
#                             {"$dateFromString": {"dateString": "$order_delivered_customer_date"}},
#                             {"$dateFromString": {"dateString": "$order_delivered_carrier_date"}}
#                         ]
#                     },
#                     3600000  # Convert milliseconds to hours
#                 ]
#             }
#         }
#     },
#     {
#         "$group": {
#             "_id": None,
#             "average_processing_time": {"$avg": "$processing_time"},
#             "average_shipping_time": {"$avg": "$shipping_time"}
#         }
#     }
# ]

# result = list(orders_collection.aggregate(pipeline))

# table = PrettyTable()
# table.field_names = ["Metric", "Average Time (in hours)"]

# if result:
#     avg_processing_time = result[0]["average_processing_time"]
#     avg_shipping_time = result[0]["average_shipping_time"]

#     table.add_row(["Average Processing Time", f"{avg_processing_time:.2f} hours"])
#     table.add_row(["Average Shipping Time", f"{avg_shipping_time:.2f} hours"])

#     print(table)
# else:
#     print("No data found.")

# end_time = time.time()
# execution_time = end_time - start_time
# print(f"Execution time: {execution_time:.2f} seconds")











# Query for: Average delivery time and freight fee
from pymongo import MongoClient
from prettytable import PrettyTable
import time
start_time = time.time()

# Connect to the MongoDB database
client = MongoClient("mongodb+srv://INF2003:wJL8pGXxgGQzqhaP@inf2003.xqigi2t.mongodb.net/")
db = client["INF2003"]  # Replace with your database name
order_items_collection = db["order_items"]
orders_collection = db["orders"]

# Create indexes on the relevant columns
order_items_collection.create_index("order_id")
orders_collection.create_index("order_id")
orders_collection.create_index("order_delivered_customer_date")
orders_collection.create_index("order_delivered_carrier_date")
order_items_collection.create_index("freight_value")

# Aggregation pipeline to calculate average delivery time and delivery fee
pipeline = [
    {
        "$lookup": {
            "from": "orders",
            "localField": "order_id",
            "foreignField": "order_id",
            "pipeline": [{"$match": {"order_status": "delivered"}}],
            "as": "order"
        }
    },
    {
        "$unwind": "$order"
    },
    {
        "$project": {
            "_id": 0,
            "order_id": "$order.order_id",
            "delivery_time_hours": {
                "$divide": [
                    {
                        "$subtract": [
                            {"$dateFromString": {"dateString": "$order.order_delivered_customer_date"}},
                            {"$dateFromString": {"dateString": "$order.order_delivered_carrier_date"}}
                        ]
                    },
                    3600000  # Convert milliseconds to hours
                ]
            },
            "delivery_fee": "$freight_value"
        }
    },
    {
        "$group": {
            "_id": "$order_id",
            "average_delivery_time": {"$avg": "$delivery_time_hours"},
            "average_delivery_fee": {"$avg": "$delivery_fee"}
        }
    },
    {
        "$group": {
            "_id": None,
            "distinct_order_ids": {"$addToSet": "$_id"},
            "average_delivery_time": {"$avg": "$average_delivery_time"},
            "average_delivery_fee": {"$avg": "$average_delivery_fee"}
        }
    }
]

result = list(order_items_collection.aggregate(pipeline))

# Create a table to display the results
table = PrettyTable()
table.field_names = ["Metric", "Average Value"]

if result:
    distinct_order_ids = result[0]["distinct_order_ids"]
    avg_delivery_time = result[0]["average_delivery_time"]
    avg_delivery_fee = result[0]["average_delivery_fee"]

    table.add_row(["Distinct Order IDs", len(distinct_order_ids)])
    table.add_row(["Average Delivery Time (hours)", f"{avg_delivery_time:.2f} hours"])
    table.add_row(["Average Freight Fee", f"${avg_delivery_fee:.2f}"])
    print(table)
else:
    print("No data found.")
end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time:.2f} seconds")
