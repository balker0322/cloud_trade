import os

BINANCE_CREDENTIALS = {
    'KEY': os.environ.get('BINANCE_KEY'),
    'SECRET': os.environ.get('BINANCE_SECRET'),
}

USER_LOGIN = {
    'USERNAME': os.environ.get('LOGIN_USERNAME'),
    'PASSWORD': os.environ.get('LOGIN_PASSWORD'),
}