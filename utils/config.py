from dotenv import load_dotenv
import os

# Force reload the .env file
dotenv_path = os.path.join(os.path.dirname(__file__), "../.env")
load_dotenv(dotenv_path, override=True)  # Use override=True to reload variables

# Read values
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

# Print values
print(f"DEBUG USERNAME: {USERNAME}")
print(f"DEBUG PASSWORD: {PASSWORD}")