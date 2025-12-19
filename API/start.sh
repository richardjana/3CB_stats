#!/usr/bin/env bash
set -e

# Start Streamlit on an internal port
streamlit run streamlit_app.py \
  --server.port 8501 \
  --server.address 127.0.0.1 \
  --server.baseUrlPath dashboard &

# Start Flask as the public server
gunicorn flask_app:app \
  --bind 0.0.0.0:$PORT