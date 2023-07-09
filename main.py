from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient

app = FastAPI()

# MongoDB connection
client = MongoClient("mongodb+srv://akshay:AkshayG5723@nodeexpressprojects.utkubig.mongodb.net/?retryWrites=true&w=majority")
db = client["ecommerce"]
products_collection = db["products"]
orders_collection = db["orders"]


class Product(BaseModel):
    name: str
    price: float
    quantity: int

class OrderItem(BaseModel):
    product_id: str
    bought_quantity: int

class UserAddress(BaseModel):
    city: str
    country: str
    zip_code: str

class Order(BaseModel):
    timestamp: str
    items: list[OrderItem]
    total_amount: float
    user_address: UserAddress

# list all available products
@app.get("/products")
def get_products():
    products = products_collection.find()
    return [product for product in products]

# create a new order
@app.post("/orders")
def create_order(order: Order):
    # if products exist and have sufficient quantity
    for item in order.items:
        product = products_collection.find_one({"_id": item.product_id})
        if not product or product["quantity"] < item.bought_quantity:
            raise HTTPException(status_code=400, detail="Invalid product or insufficient quantity")


    for item in order.items:
        products_collection.update_one({"_id": item.product_id}, {"$inc": {"quantity": -item.bought_quantity}})
    order_id = orders_collection.insert_one(order.dict(by_alias=True)).inserted_id
    return {"order_id": str(order_id)}

# fetch all orders
@app.get("/orders")
def get_orders(limit: int = 10, offset: int = 0):
    orders = orders_collection.find().limit(limit).skip(offset)
    return [order for order in orders]

#  fetch a single order by Order ID
@app.get("/orders/{order_id}")
def get_order(order_id: str):
    order = orders_collection.find_one({"_id": order_id})
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

# update a product's available quantity
@app.put("/products/{product_id}")
def update_product(product_id: str, quantity: int):
    products_collection.update_one({"_id": product_id}, {"$set": {"quantity": quantity}})
    return {"message": "Product quantity updated"}

# Dummy products
dummy_products = [
    {
        "_id": "1",
        "name": "TV",
        "price": 55000,
        "quantity": 10
    },
    {
        "_id": "2",
        "name": "Camera",
        "price": 10000,
        "quantity": 15
    },
    {
        "_id": "3",
        "name": "Laptop",
        "price": 50000,
        "quantity": 12
    },
    {
        "_id": "4",
        "name": "Microwave",
        "price": 4000,
        "quantity": 7
    },
    {
        "_id": "5",
        "name": "Speakers",
        "price": 1000,
        "quantity": 25
    },
    {
        "_id": "6",
        "name": "Smartphones",
        "price": 7000,
        "quantity": 5
    },
    {
        "_id": "7",
        "name": "Headphones",
        "price": 4000,
        "quantity": 28
    },
    {
        "_id": "8",
        "name": "Tablet",
        "price": 17000,
        "quantity": 22
    },
    {
        "_id": "9",
        "name": "Printer",
        "price": 4000,
        "quantity": 28
    },
    {
        "_id": "10",
        "name": "Smartwatch",
        "price": 6000,
        "quantity": 19
    }
]


# for product in dummy_products:
#     products_collection.insert_one(product)
