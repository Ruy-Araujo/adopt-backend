import os
from decouple import config

# Set local environment variables
try:
    os.environ['SECRET_KEY'] = config("SECRET_KEY")
    os.environ['ALGORITHM'] = config("ALGORITHM")
except:
    raise ValueError("Local environment variables not loaded")
