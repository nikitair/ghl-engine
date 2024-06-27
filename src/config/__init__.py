import os
import time

from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = os.getcwd()
HOST = os.getenv("HOST", "")
PORT = int(os.getenv("PORT", 0))
