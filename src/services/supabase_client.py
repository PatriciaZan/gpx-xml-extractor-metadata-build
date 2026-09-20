import os
import logging
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

if not SUPABASE_URL:
    raise ValueError("SUPABASE_URL not found in environment variables.")

if not SUPABASE_KEY:
    raise ValueError("SUPABASE_SERVICE_KEY not found in environment variables.")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

logger.info("Supabase client created successfully.")
