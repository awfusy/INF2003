from pymongo import MongoClient


client = MongoClient("mongodb+srv://INF2003:wJL8pGXxgGQzqhaP@inf2003.xqigi2t.mongodb.net/")
db = client["INF2003"]  # Replace with your database name
products_collection = db["products"]
orders_collection = db["orders"]
order_items_collection = db["order_items"]
customers_collection = db["customers"]
order_reviews_collection = db["order_reviews"]
geolocation_collection = db["geolocation"]
order_payment_collection = db["order_payments"]
translated_english_collection = db["translated_category"]
# create index for faster searching
orders_collection.create_index("order_id")
order_items_collection.create_index("order_id")
products_collection.create_index("product_id")
order_reviews_collection.create_index("review_id")
geolocation_collection.create_index("geolocation_zip_code_prefix")
customers_collection.create_index("customer_id")
order_payment_collection.create_index("order_id")
translated_english_collection.create_index("product_category_name")
# Perform aggregation to find the most purchased product
#2.1
revenue_by_cat_pipeline = [
{"$lookup": {"from": "products","localField": "product_id","foreignField": "product_id","as": "product"}},
{"$unwind": "$product"},
{"$lookup": {"from": "translated_category","localField": "product.product_category_name",
             "foreignField": "product_category_name","as": "translated_category"}},
{"$unwind": "$translated_category"},
{"$lookup": {"from": "orders","localField": "order_id","foreignField": "order_id","as": "order"}},
{
"$unwind": "$order"},
{"$match": {"order.order_status": "delivered",}},
{"$group": {"_id": "$translated_category.product_category_name_english","Num_orders": {"$addToSet": "$order.order_id"},
            "Revenue": {"$sum": "$price"}}},
{"$project": {"_id": 0,"product_category_name": "$_id","Num_orders": {"$size": "$Num_orders"},"Revenue": 1}},
{"$sort": {"Revenue": -1}}
]
order_items_collection.aggregate(revenue_by_cat_pipeline)
# result =
#
# for doc in result:
#     print(doc)
# 2.2
star_5 = [
    {"$match": {"review_score": 5}},
    {"$lookup": {"from": "order_items", "localField": "order_id", "foreignField": "order_id", "as": "order_items"}},
    {"$unwind": "$order_items"},
    {"$lookup": {"from": "products", "localField": "order_items.product_id", "foreignField": "product_id", "as": "product"}},
    {"$unwind": "$product"},
    {"$lookup": {"from": "translated_category", "localField": "product.product_category_name", "foreignField": "product_category_name", "as": "translated_category"}},
    {"$unwind": "$translated_category"},
    {"$group": {"_id": "$translated_category.product_category_name_english", "count": {"$sum": 1}}},
    {"$sort": {"count": -1}},
    {"$limit": 10}
]
# reuslt = order_reviews_collection.aggregate(star_5)
#
# for r in reuslt:
#     print(r)
#2.3
most_popular_cat_by_Geo_pipeline = [
    {
        "$lookup": {
            "from": "orders",
            "localField": "order_id",
            "foreignField": "order_id",
            "as": "order"
        }
    },
    {
        "$unwind": "$order"
    },
    {
        "$lookup": {
            "from": "customers",
            "localField": "order.customer_id",
            "foreignField": "customer_id",
            "as": "customer"
        }
    },
    {
        "$unwind": "$customer"
    },
    {
        "$lookup": {
            "from": "products",
            "localField": "product_id",
            "foreignField": "product_id",
            "as": "product"
        }
    },
    {
        "$unwind": "$product"
    },
    {
        "$lookup": {
            "from": "translated_category",
            "localField": "product.product_category_name",
            "foreignField": "product_category_name",
            "as": "translated_category"
        }
    },
    {
        "$unwind": "$translated_category"
    },
    {
        "$match": {
            "order.order_status": "delivered"
        }
    },
    {
        "$group": {
            "_id": {
                "customer_state": "$customer.customer_state",
                "product_category_name": "$translated_category.product_category_name_english"
            },
            "QuantitySold": {"$sum": 1}
        }
    },
    {
        "$sort": {"QuantitySold": -1}
    },
    {
        "$group": {
            "_id": "$_id.customer_state",
            "HighestSoldCategory": {"$first": "$_id.product_category_name"},
            "QuantitySold": {"$first": "$QuantitySold"}
        }
    },
    {
        "$sort": {"QuantitySold": -1}
    }
]
# Execute Aggregation Pipeline
# result = list(order_items_collection.aggregate(most_popular_cat_by_Geo_pipeline))
#
# # Print Result
# for r in result:
#     print(r)
#======================================================================================================#
# 2.4
frequent_bought_category_pipeline = [
    {
        "$lookup": {
            "from": "order_items",
            "localField": "order_id",
            "foreignField": "order_id",
            "as": "order_order_items"
        }
    },
    {
        "$unwind": "$order_order_items"
    },
    {
        "$lookup": {
            "from": "products",
            "localField": "order_order_items.product_id",
            "foreignField": "product_id",
            "as": "order_item_products"
        }
    },
    {
        "$unwind": "$order_item_products"
    },
    {
        "$lookup": {
            "from": "translated_category",
            "localField": "order_item_products.product_category_name",
            "foreignField": "product_category_name",
            "as": "translated_category"
        }
    },
    {
        "$unwind": "$translated_category"
    },
    {
        "$group": {
            "_id": "$translated_category.product_category_name_english",
            "purchaseCount": {"$sum": 1}
        }
    },
    {
        "$sort": {"purchaseCount": -1}
    }
]
# Execute the aggregation pipeline
result = orders_collection.aggregate(frequent_bought_category_pipeline)
# Print the result
for r in result:
    print(r)