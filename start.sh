#!/bin/bash

# Set environment variables if needed
export FLASK_APP=main.py
export FLASK_ENV=production  # or 'development' if you're in a development environment

# Start the application using Waitress
exec python app.py