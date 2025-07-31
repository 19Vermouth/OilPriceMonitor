from dotenv import load_dotenv
import os
load_dotenv
print("DEBUG: Current working directory:", os.getcwd())
print("DEBUG: Files in directory:", os.listdir())
load_dotenv()  # Add this line before accessing env vars

print("DEBUG: ALPHAVANTAGE_API_KEY exists?", "ALPHAVANTAGE_API_KEY" in os.environ)