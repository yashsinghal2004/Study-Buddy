from langchain_groq import ChatGroq #for chatting with model
from src.config.settings import settings

def get_groq_client(): # need to use this 1 time and able to access llm as connected with config
    return ChatGroq(
        api_key= settings.GROQ_API_KEY,
        model= settings.MODEL_NAME,
        temperature= settings.TEMPERATURE, #till here mandatory parameters
        max_retries= settings.MAX_RETRIES,

    )

