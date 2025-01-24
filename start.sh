#!/bin/bash

# Install Playwright dependencies on Linux
pip install playwright
python -m playwright install

# Start the FastAPI app using uvicorn
uvicorn main:app --host 0.0.0.0 --port $PORT --timeout-keep-alive 120
