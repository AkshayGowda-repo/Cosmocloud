# Cosmocloud

## Install the dependencies:
### Open Visual Studio Code.
- Download the project repository
- Create a new folder for your project and open it in VS Code.
### Initialize a New Python Virtual Environment
 ```
python3 -m venv venv
```
### Activate the virtual environment
```
 venv\Scripts\activate
```
### Install Required Packages
```
 pip install fastapi pymongo pydantic uvicorn
```
### To run the application
```
 uvicorn main:app --reload
```
####  Code includes all five APIs requirement as in the assignment:
```
1 API to list all available products: GET /products
2 API to create a new order: POST /orders
3 API to fetch all orders with pagination: GET /orders
4 API to fetch a single order by order ID: GET /orders/{order_id}
5 API to update a product's available quantity: PUT /products/{product_id}
```
