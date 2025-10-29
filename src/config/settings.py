import os
from dotenv import load_dotenv

load_dotenv()

class Settings():

    GROQ_API_KEY= os.getenv("GROQ_API_KEY")

    MODEL_NAME= "llama-3.1-8b-instant"

    TEMPERATURE= 0.9;  #higher the temp more is the creativity of model

    MAX_RETRIES= 3 #max number of retries if the request fails


settings = Settings()