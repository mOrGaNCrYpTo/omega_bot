# # app.py

# import os
# from dotenv import load_dotenv
# from config import *

# # Load environment variables from .env file
# load_dotenv()

# # Override configuration settings from .env file
# DATABASE["username"] = os.getenv("DATABASE_USERNAME", DATABASE["username"])
# DATABASE["password"] = os.getenv("DATABASE_PASSWORD", DATABASE["password"])

# # Use the final configuration settings
# print("DEBUG:", DEBUG)
# print("DATABASE:", DATABASE)