#!/bin/bash

# Activate the virtual environment
source /

# Export necessary environment variables
export FLASK_APP=application.py
export FLASK_ENV=production

# Start the app using gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 application:application
