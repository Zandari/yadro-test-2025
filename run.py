from app import create_app
from config import Config


if __name__ == "__main__":
    with create_app(Config) as app:
        app.run(debug=Config.DEBUG, host='0.0.0.0')
