#!/usr/bin/env bash
# Author: Thoxvi <Thoxvi@Gmail.com>
# $1: App package name

cd /app
gunicorn \
    -k gevent \
    --workers=8 \
    --worker-connections 32 \
    -b 0.0.0.0:80 \
    flask_app:app
