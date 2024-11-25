import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_BASE_URL = os.getenv('OPENAI_BASE_URL')
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_PORT = os.getenv('MYSQL_PORT')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')

# 从单独的文件读取 prompt
PROMPT_FILE = Path("prompts/summary_prompt.txt")
SUMMARY_PROMPT = PROMPT_FILE.read_text(
    encoding='utf-8') if PROMPT_FILE.exists() else os.getenv('SUMMARY_PROMPT')

MD_FILES_PATH = os.getenv('MD_FILES_PATH')
