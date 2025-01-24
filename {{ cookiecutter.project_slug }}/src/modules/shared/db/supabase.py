import json
import os
from datetime import datetime
from typing import Any, Dict, Generator, List, Optional, Type
from uuid import UUID

from dotenv import load_dotenv
from sqlmodel import SQLModel
from supabase import AClient, create_client

from modules.shared.db.base import DatabaseService


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, UUID):
            return str(obj)
        return super().default(obj)


load_dotenv()

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
service_role: str = os.getenv("SUPABASE_SERVICE_KEY")
supabase: AClient = None
supabase_admin: AClient = None
if url and key:
    supabase = create_client(url, key)
if url and service_role:
    supabase_admin = create_client(url, service_role)

class SupabaseDB(DatabaseService):
    def __init__(self, url: str, key: str):
        self.client: AClient = create_client(url, key)

    def init_db(self) -> None:
        # Supabase DB is managed externally
        pass

    def get_session(self) -> Generator[AClient, None, None]:
        yield self.client

    def schema(self) -> str:
        # Will implement later
        pass

    def all_records(self, model: Type[SQLModel]) -> List[SQLModel]:
        response = self.client.table(model.__name__.lower()).select("*").execute()
        data: List[dict] = response.data
        return model._cast_data(data)

    def query_records(
        self,
        model: Type[SQLModel],
        search_value: Optional[str] = None,
        sorting_field: Optional[str] = None,
        sort_direction: str = "asc",
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        as_dict: bool = False,
        fields: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        table = self.client.table(model.__tablename__)

        if fields:
            query = table.select(",".join(fields))
        else:
            query = table.select("*")

        if search_value:
            string_fields = [
                k for k, v in model.__fields__.items() if v.annotation is str
            ]

            if string_fields:
                conditions = [
                    f"{field}.ilike.*{search_value}*" for field in string_fields
                ]
                or_condition = ",".join(conditions)
                query = query.or_(or_condition)

        if sorting_field and sorting_field in model.__fields__:
            query = query.order(sorting_field, desc=(sort_direction.lower() == "desc"))

        if offset is not None:
            if limit is not None:
                query = query.range(offset, offset + limit - 1)
            else:
                query = query.range(offset, offset + 1000)  # Default limit

        try:
            response = query.execute()
            if as_dict:
                return response.data
            return [model(**record) for record in response.data]
        except Exception as e:
            raise Exception(f"Error querying records: {str(e)}")

    def get_record(
        self, model: Type[SQLModel], id: Any, alt_key: str = None
    ) -> Optional[SQLModel]:
        key = alt_key if alt_key else "id"
        try:
            response = (
                self.client.table(model.__tablename__).select("*").eq(key, id).execute()
            )
            if response.data:
                return model(**response.data[0])
            return None
        except Exception as e:
            raise Exception(f"Error fetching record: {str(e)}")

    def update_record(
        self, model: Type[SQLModel], id: Any, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        try:
            response = (
                self.client.table(model.__tablename__)
                .update(data)
                .eq("id", id)
                .execute()
            )
            if response.data:
                return response.data[0]
            raise Exception(f"Record with id {id} not found")
        except Exception as e:
            raise Exception(f"Error updating record: {str(e)}")

    def delete_record(self, model: Type[SQLModel], id: Any) -> None:
        try:
            self.client.table(model.__tablename__).delete().eq("id", id).execute()
        except Exception as e:
            raise Exception(f"Error deleting record: {str(e)}")

    def upsert_record(self, model: Type[SQLModel], data: Dict[str, Any]) -> SQLModel:
        try:
            if "id" in data and data["id"]:
                record = model.get(data["id"])
                if record:
                    for key, value in data.items():
                        setattr(record, key, value)
                else:
                    record = model(**data)
            else:
                record = model(**data)
            # json_data = json.loads(json.dumps(filtered_data, cls=CustomJSONEncoder))
            json_data = json.loads(
                json.dumps(record.model_dump(), cls=CustomJSONEncoder)
            )
            response = (
                self.client.table(model.__tablename__).upsert(json_data).execute()
            )
            if response.data:
                return model(**response.data[0])
            raise Exception("Error upserting record")
        except Exception as e:
            raise Exception(f"Error upserting record: {str(e)}")

    def bulk_insert(
        self, model: Type[SQLModel], data: List[Dict[str, Any]]
    ) -> List[SQLModel]:
        try:
            response = self.client.table(model.__tablename__).insert(data).execute()
            return [model(**record) for record in response.data]
        except Exception as e:
            raise Exception(f"Error bulk inserting records: {str(e)}")

    def bulk_update(
        self, model: Type[SQLModel], data: List[Dict[str, Any]]
    ) -> List[SQLModel]:
        try:
            response = self.client.table(model.__tablename__).upsert(data).execute()
            return [model(**record) for record in response.data]
        except Exception as e:
            raise Exception(f"Error bulk updating records: {str(e)}")

    def count_records(self, model: Type[SQLModel]) -> int:
        try:
            response = (
                self.client.table(model.__tablename__)
                .select("*", count="exact")
                .execute()
            )
            return response.count
        except Exception as e:
            raise Exception(f"Error counting records: {str(e)}")
