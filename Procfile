# Railway Procfile - runs both bot and API server

# Start API server and bot together
web: cd bot && uvicorn bella_bot.api_server:app --host 0.0.0.0 --port $PORT & python -m bella_bot
