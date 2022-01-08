from flask_frozen import Freezer
from app import create_app, cookbook


app = create_app()
freezer = Freezer(app)

if __name__ == '__main__':
    freezer.freeze()