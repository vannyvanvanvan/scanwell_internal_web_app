from ..app.model import db

def initialize_database():
    db.create_all()
    print("Database tables created successfully.")

if __name__ == "__main__":
    initialize_database()