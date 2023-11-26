import pymongo
from pymongo import MongoClient

client = pymongo.MongoClient("mongodb+srv://INF2003:wJL8pGXxgGQzqhaP@inf2003.xqigi2t.mongodb.net/")
db = client["INF2003"]

payment_collection = db["order_payments"]
reviews_collection = db["order_reviews"]
orders_collection = db["order_items"]
sellers_collection = db["sellers"]
products_collection = db["products"]
translated_collection = db["translated_category"]

# Create indexes
orders_collection.create_index('seller_id')
products_collection.create_index('product_id')

# # Most commonly used payment methods
pipeline = [
    {"$group": {
        "_id": "$payment_type", 
        "count": {"$sum": 1}
    }},
    {"$sort": {"count": -1}}
]

most_common_payments = payment_collection.aggregate(pipeline)

# # Print the results
# for payment_method in most_common_payments:
#     print(f"Payment Method: {payment_method['_id']}, Count: {payment_method['count']}")

################################################################################################

# Average customer reviews score on products
pipeline = [
    {
        '$lookup': {
            'from': 'order_items', 
            'localField': 'order_id', 
            'foreignField': 'order_id', 
            'as': 'order_items'  
        }
    },
    {'$unwind': '$order_items'}, 
    {
        '$group': {
            '_id': '$order_items.product_id',
            'average_score': {'$avg': '$review_score'}
        }
    },
    {
        '$project': {
            'product_id': '$_id',
            'average_score': {'$ifNull': ['$average_score', "No reviews"]},
            '_id': 0
        }
    },

    {'$limit': 10}

]


# # Execute the aggregation pipeline on the 'reviews_collection'
# average_scores = reviews_collection.aggregate(pipeline)

# # Print the results
# for score in average_scores:
#     if isinstance(score['average_score'], str):
#         print(f"Product ID: {score['product_id']}, Average Review Score: {score['average_score']}")
#     else:
#         print(f"Product ID: {score['product_id']}, Average Review Score: {score['average_score']:.2f}")

#############################################################################################################

# Categories with most sellers
pipeline = [
    {
        '$project': {
            'seller_id': 1,
            'product_id': 1
        }
    },
    {
        '$lookup': {
            'from': 'products',
            'localField': 'product_id',
            'foreignField': 'product_id',
            'as': 'product_info'
        }
    },
    {'$unwind': '$product_info'},
    {
        '$group': {
            '_id': '$product_info.product_category_name',
            'unique_sellers': {'$addToSet': '$seller_id'}
        }
    },
    {
        '$project': {
            'number_of_sellers': {'$size': '$unique_sellers'}
        }
    },
    {'$sort': {'number_of_sellers': -1}}
]

# # Execute the aggregation pipeline
# category_seller_counts = orders_collection.aggregate(pipeline)

# # Print the results
# for category in category_seller_counts:
#     print(f"{category['_id']}, {category['number_of_sellers']}")

#######################################################################################################


# AVERAGE CUSTOMER REVIEWS SCORE FOR PRODUCT CATEGORY
pipeline = [
    {
        '$lookup': {
            'from': 'order_items',
            'localField': 'order_id',
            'foreignField': 'order_id',
            'as': 'order_items'
        }
    },
    {'$unwind': '$order_items'},  
    {
       
        '$lookup': {
            'from': 'products',
            'localField': 'order_items.product_id',
            'foreignField': 'product_id',
            'as': 'product_info'
        }
    },
    {'$unwind': '$product_info'},  
    {
      
        '$lookup': {
            'from': 'translated_category',
            'localField': 'product_info.product_category_name',
            'foreignField': 'product_category_name',
            'as': 'category_translation'
        }
    },
    {'$unwind': '$category_translation'},  
    {
      
        '$group': {
            '_id': '$category_translation.product_category_name_english',
            'average_review_score': {'$avg': '$review_score'}
        }
    },
    {
       
        '$sort': {'average_review_score': -1}
    },
    {
  
        '$project': {
            'category_name_english': '$_id',
            'average_review_score': {'$round': ['$average_review_score', 4]},
            '_id': 0
        }
    },
    {'$limit': 10} 
]

# # Execute the aggregation pipeline
# category_review_scores = reviews_collection.aggregate(pipeline)

# # Print the results
# for category in category_review_scores:
#     print(f"{category['category_name_english']}, {category['average_review_score']}")
