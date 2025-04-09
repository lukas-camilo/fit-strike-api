class ProductRepository:
    def __init__(self):
        self.products = {}

    def create(self, product):
        self.products[product.product_id] = product

    def get(self, product_id):
        return self.products.get(product_id)

    def update(self, product_id, updated_product):
        if product_id in self.products:
            self.products[product_id] = updated_product

    def delete(self, product_id):
        if product_id in self.products:
            del self.products[product_id]

    def list_all(self):
        return list(self.products.values())