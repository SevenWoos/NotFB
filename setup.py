from extensions import db
from app import create_app  

app = create_app()

# Create all tables defined in models
with app.app_context():
    db.create_all()  
