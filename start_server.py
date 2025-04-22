#!/usr/bin/env python3
# start_server.py - Script to start the IRI® Legal Agent server

import os
import subprocess
import sys
import time

def check_dependencies():
    """Check if all required dependencies are installed."""
    try:
        import flask
        import gunicorn
        import gevent
        import requests
        import dotenv
        return True
    except ImportError as e:
        print(f"Missing dependency: {e}")
        print("Please run: pip3 install --user flask gunicorn gevent requests python-dotenv")
        return False

def create_directories():
    """Create necessary directories if they don't exist."""
    directories = ['screenshots', 'uploads', 'static', 'templates']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")

def start_server():
    """Start the Gunicorn server with the enhanced app."""
    print("Starting IRI® Legal Agent server...")
    
    # Check if the enhanced_app.py file exists
    if not os.path.exists('enhanced_app.py'):
        print("Error: enhanced_app.py not found!")
        return False
    
    # Check if the gunicorn_config.py file exists
    if not os.path.exists('gunicorn_config.py'):
        print("Error: gunicorn_config.py not found!")
        return False
    
    try:
        # Start the server using Gunicorn
        cmd = ["gunicorn", "--config", "gunicorn_config.py", "wsgi:app"]
        process = subprocess.Popen(cmd)
        
        # Wait a moment to ensure the server starts
        time.sleep(2)
        
        # Check if the process is still running
        if process.poll() is None:
            print("Server started successfully!")
            print("The IRI® Legal Agent is now running on http://0.0.0.0:5000")
            print("Press Ctrl+C to stop the server.")
            
            # Keep the script running
            try:
                process.wait()
            except KeyboardInterrupt:
                print("\nStopping server...")
                process.terminate()
                process.wait()
                print("Server stopped.")
            
            return True
        else:
            print("Error: Server failed to start!")
            return False
    
    except Exception as e:
        print(f"Error starting server: {e}")
        return False

if __name__ == "__main__":
    print("IRI® Legal Agent - Server Starter")
    print("=================================")
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Create necessary directories
    create_directories()
    
    # Start the server
    if not start_server():
        sys.exit(1)
