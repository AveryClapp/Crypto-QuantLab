import os
from dotenv import load_dotenv
from supabase import create_client, Client
import pandas as pd


def setup_supabase():
    load_dotenv('./app/core/.env')
    url: str = os.getenv("SB_URL")
    key: str = os.getenv("SB_KEY")
    supabase: Client = create_client(url, key)