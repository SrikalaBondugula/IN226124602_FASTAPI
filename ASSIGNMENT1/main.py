from fastapi import FastAPI
app=FastAPI()
products_list=[{"id":1,"name":"redmi 12pro 5g phone","price":20000,"category":"electronics","in_stock":True},
                   {"id":2,"name":"redmi 60W charger","price":2000,"category":"electronics","in_stock":True},
                   {"id":3,"name":"realme wired earphone","price":600,"category":"electronics","in_stock":False},
                   {"id":4,"name":"lackme","price":200,"category":"beauty","in_stock":True}]
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
