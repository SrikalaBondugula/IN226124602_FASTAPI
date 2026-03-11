from fastapi import FastAPI
from pydantic import BaseModel,Field
from typing import Optional
app=FastAPI()
products_list=[{"id":1,"name":"wireless mouse","price":499,"category":"electronics","in_stock":True},
                   {"id":2,"name":"redmi 60W charger","price":2000,"category":"electronics","in_stock":True},
                   {"id":3,"name":"realme wired earphone","price":600,"category":"electronics","in_stock":False},
                   {"id":4,"name":"useb hub","price":799,"category":"electronic","in_stock":True}]
#1
@app.get("/products")
def get_products():
    global products_list
    products_list.extend([{"id":5,"name":"Laptop Stand","price":2000,"category":"electronics","in_stock":True},
                   {"id":6,"name":"Mechanical Keyboard","price":1000,"category":"electronics","in_stock":True},
                   {"id":7,"name":"Webcam","price":5000,"category":"electronics","in_stock":True}])
    return {"products":products_list,
            "Total":len(products_list)}
#2
@app.get("/products/category/{category_name}")
def get_category(category_name:str):
    global products_list
    result_list=[]
    for product in products_list:
        if product["category"]==category_name.lower():
            result_list.append(product)
    if len(result_list)<=0:
        return {"error":"No products found in this category"}
    else:
        return {"result":result_list}
#3
@app.get("/products/instock")
def get_instock_products():
    global products_list
    result_list=[p for p in products_list if p["in_stock"]==True]
    if len(result_list)<=0:
        return{"error":"no products  found"}
    return{"in_stock_products":result_list,
           "count":len(result_list)}
#4
@app.get("/store/summary")
def get_store_summary():
    global products_list
    total_products_count=len(products_list)
    in_stock_count=0
    out_of_stock=0
    unique_category=[]
    for product in products_list:
        if product["in_stock"]==True:
            in_stock_count+=1
        else:
            out_of_stock+=1
        if product["category"] not in unique_category:
            unique_category.append(product["category"])
    return{"store_name":"My E-commerce store",
           "Total_products":total_products_count,
           "in_stock":in_stock_count,
           "out_of_stock":out_of_stock,
           "categories":unique_category}
#5
@app.get("/products/search/{keyword}")
def get_item_by_search(keyword:str):
    global products_list
    results=[p for p in products_list if keyword.lower() in p["name"]]
    if len(results)<=0:
        return{"message":"no products matched your search"}
    return{"keyword":keyword,
           "results":results,
           "total_matches":len(results)}
#bonus
@app.get("/products/deals")
def get_product_deals():
     cheapest_product = min(products_list, key=lambda p: p["price"]) 
     expensive_product = max(products_list, key=lambda p: p["price"]) 
     return { "best_deal": cheapest_product, "premium_pick": expensive_product}
#Filter by minimum price
@app.get("/products/filter")
def get_products_within_price(min_price:int,max_price:int=None):
    result=[]
    for product in products_list:
        if max_price is None:
            if product["price"]>=min_price:
                result.append(product)
        else:
            if max_price>=product["price"]>=min_price:
                result.append(product)
    return result
#get only the price of a product
@app.get("/products/{product_id}/price")
def get_product_name_price(product_id:int):
    found=False
    for products in products_list:
        if products["id"]==product_id:
           found=True
           name=products["name"]
           price=products["price"]
           break
    if found:
     return{
           "name":name,
           "price":price
          }
    else:
        return{
            "error":"Product not found"
        }
#Accept Customer Feedback
class Feedback(BaseModel):
    customer_name:str= Field(min_length=2,max_length=100)
    product_id:int=Field(gt=0)
    rating:int=Field(ge=1,le=5)
    comment:Optional[str]=Field(None,max_length=300)
@app.post("/feedback")
def post_feedback(feedback:Feedback):
    feedback_list=[]
    feedback_list.append(feedback)
    return{
        "message":"feedback submitted successfully",
        "feedback":feedback,
        "total_feedback":len(feedback_list)
    }
#Build a Product summary dashboard
@app.get("/products/summary/")
def get_product_summary():
    stock_count=0
    out_of_stock_count=0
    max=0
    cheap=float("inf")
    categories=[]
    for product in products_list:
        if product["in_stock"]==True:
            stock_count+=1
        else:
            out_of_stock_count+=1
        if product["price"]>max:
            max=product["price"]
            name=product["name"]
        if product["price"]<cheap:
            cheap=product["price"]
            c_name=product["name"]
        if product["category"] not in categories:
            categories.append(product["category"])
    return{
        "total_products":len(products_list),
        "in_stock_count":stock_count,
        "out_of_stock_count":out_of_stock_count,
        "most_expensive":{
            "name":name,
            "price":max
        },
        "cheapest":{
            "name":c_name,
            "price":cheap
        },
        "categories":categories
    }
class OrderItem(BaseModel):
    product_id:int=Field(gt=0)
    quantity:int=Field(gt=1,le=50)
class BulkOrder(BaseModel):
    company_name:str=Field(min_length=2)
    contact_email:str=Field(min_length=5)
    item:list[OrderItem]=Field(min_length=1)
@app.post("/orders/bulk")
def post_orders(order:BulkOrder):
    confirmed_order=[]
    failed_orders=[]
    total_amount=0
    for item in order.item:
        product=None
        for products in products_list:
            if products["id"]==item.product_id:
                product=products
    if product==None:
        failed_orders.append({"product_id":item.product_id,
                              "reason":"product not found"})
    elif product["in_stock"]==False:
        failed_orders.append({"product_id":item.product_id,
                              "reason": f"{product['name']} is out of stock"})
    else:
        subtotal=product["price"]*item.quantity
        total_amount+=subtotal
        confirmed_order.append({"product":product["name"],
                                "qty":item.quantity,
                                "subtotal":subtotal})
    return {"company": order.company_name, 
            "confirmed": confirmed_order,
            "failed": failed_orders,
            "grand_total": total_amount}

    
    

            



    
