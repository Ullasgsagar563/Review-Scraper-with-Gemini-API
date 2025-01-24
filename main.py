# Description: This file is the main entry point for the FastAPI application. It creates a FastAPI app and includes the router defined in the routes.py file. It also configures logging and loads environment variables using the python-dotenv library. Finally, it starts the FastAPI app using the uvicorn server.
from fastapi import FastAPI
from routes import router
import uvicorn
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Load environment variables
load_dotenv()

# Create a FastAPI app
app = FastAPI(title="Review Scraper API")
app.include_router(router)
from fastapi.middleware.cors import CORSMiddleware



# Define the main entry point
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)