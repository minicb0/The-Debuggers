import os

from dotenv import load_dotenv

load_dotenv()

env = os.environ

MONGODB_SETTINGS = {
    "db": env["DATABASE"],
    "host": env["MONGODB_HOST"],
    "port": int(env["MONGODB_PORT"]),
    "username": env["MONGODB_USERNAME"],
    "password": env["MONGODB_PASSWORD"],
}

DEBUG = env["DEBUG"] == "True"
PORT = int(env["APP_PORT"])
