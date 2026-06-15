from app import db

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(255), nullable=True) 
    price = db.Column(db.Float, nullable=False)      
    stock = db.Column(db.Integer, nullable=False)     
    description = db.Column(db.Text, nullable=True)   

    def __repr__(self):
        return f"<Product {self.name}>"
