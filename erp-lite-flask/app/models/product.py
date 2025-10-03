# models/product.py

# Simulação de um "banco de dados" simples em memória
# Em um projeto real, você usaria um ORM como SQLAlchemy.
PRODUCTS = {}
next_id = 1

class Product:
    def __init__(self, name, price, description):
        global next_id
        self.id = next_id
        self.name = name
        self.price = price
        self.description = description
        next_id += 1

    @staticmethod
    def all():
        return list(PRODUCTS.values())

    @staticmethod
    def get(product_id):
        return PRODUCTS.get(product_id)

    def save(self):
        PRODUCTS[self.id] = self

    def update(self, name, price, description):
        self.name = name
        self.price = price
        self.description = description
        self.save()

    def delete(self):
        if self.id in PRODUCTS:
            del PRODUCTS[self.id]