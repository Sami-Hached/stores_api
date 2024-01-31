import os

os.system("dotenv run uvicorn src.presentation.api.v1.main:app --reload")
