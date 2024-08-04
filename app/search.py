from app.model import Shipping_data, db

def search_products(product_id=None, date_created=None):
    query = db.session.query(Shipping_data)
    
    if product_id:
        query = query.filter(Shipping_data.id == product_id)
    elif date_created:
        #perform a "LIKE" query in SQL, which is useful for pattern matching in string fields
        query = query.filter(Shipping_data.date_created.like(f"%{date_created}%"))
    
    return query.all()
