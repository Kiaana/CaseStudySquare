from app import app, db
from app.config import Config


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=Config.PORT)