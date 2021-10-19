from dotenv import load_dotenv
load_dotenv()
from recipes2 import app

# Setting up for multiple configs
# from recipes2 import create_app
# app = create_app()
# # Allow working with SQLAlchemy from terminal
# app.app_context().push()

if __name__ == "__main__":
    app.run(debug=False)