import os
import logfire
from config import Settings

logfire.configure(send_to_logfire='if-token-present')
from modules.shared.db.sqlmodel import SQLModelDB
from modules.shared.db.supabase import SupabaseDB


def get_db_service():
    db_type = Settings().db_service

    if db_type == "supabase":
        return SupabaseDB(url=Settings().supabase_url, key=Settings().supabase_key)
    else:
        sql = SQLModelDB(url=Settings().database_url)
        logfire.instrument_sqlalchemy(sql.engine)
        return sql


service = get_db_service()

__all__ = ["service"]