#!/usr/bin/env python3
# gunicorn_config.py - Gunicorn configuration for production deployment

import multiprocessing

# Bind to all interfaces on port 5000
bind = "0.0.0.0:5000"

# Number of worker processes
workers = multiprocessing.cpu_count() * 2 + 1

# Worker class
worker_class = "gevent"

# Timeout in seconds
timeout = 120

# Log level
loglevel = "info"

# Access log format
accesslog = "-"

# Error log
errorlog = "-"

# Preload application
preload_app = True

# Daemon mode
daemon = False
