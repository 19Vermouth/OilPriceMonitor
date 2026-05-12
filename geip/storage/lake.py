import os
import json
from datetime import datetime, timezone
from typing import Any

import pandas as pd
from deltalake.writer import write_deltalake
from deltalake.table import DeltaTable

from geip.storage.config import config, lake


class LakeManager:
    def __init__(self):
        self._table_paths: dict[str, str] = {}
        self._ensure_bucket()

    def _ensure_bucket(self):
        try:
            import boto3
            s3 = boto3.client(
                "s3",
                endpoint_url=f"http://{config.endpoint}",
                aws_access_key_id=config.access_key,
                aws_secret_access_key=config.secret_key,
            )
            try:
                s3.head_bucket(Bucket=config.bucket)
            except:
                s3.create_bucket(Bucket=config.bucket)
        except ImportError:
            pass

    def _get_table_path(self, layer: str, table: str) -> str:
        key = f"{layer}/{table}"
        if key not in self._table_paths:
            self._table_paths[key] = f"data/{layer}/{table}"
        return self._table_paths[key]

    def write_bronze(self, table: str, data: list[dict[str, Any]]):
        if not data:
            return
        df = pd.DataFrame(data)
        df["_ingested_at"] = datetime.now(timezone.utc).isoformat()
        path = self._get_table_path("bronze", table)
        write_deltalake(path, df, mode="append", partition_by=["_ingested_at"])

    def write_silver(self, table: str, data: list[dict[str, Any]]):
        if not data:
            return
        df = pd.DataFrame(data)
        df["_processed_at"] = datetime.now(timezone.utc).isoformat()
        path = self._get_table_path("silver", table)
        write_deltalake(path, df, mode="overwrite")

    def read_table(self, layer: str, table: str, limit: int = 100) -> pd.DataFrame:
        path = self._get_table_path(layer, table)
        try:
            dt = DeltaTable(path)
            return dt.to_pandas().head(limit)
        except Exception:
            return pd.DataFrame()

    def get_latest(self, layer: str, table: str) -> pd.DataFrame:
        path = self._get_table_path(layer, table)
        try:
            dt = DeltaTable(path)
            return dt.to_pandas().tail(10)
        except Exception:
            return pd.DataFrame()


lake_manager = LakeManager()
