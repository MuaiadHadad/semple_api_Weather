import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configurações da aplicação"""
    FLASK_APP = os.getenv('FLASK_APP', 'app.py')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    PORT = int(os.getenv('PORT', 5000))

    # URLs do IPMA
    IPMA_BASE_URL = "https://api.ipma.pt/open-data"
    IPMA_FORECAST_URL = f"{IPMA_BASE_URL}/forecast/meteorology/cities/daily"
