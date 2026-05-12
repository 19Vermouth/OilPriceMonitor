import os
from dataclasses import dataclass


@dataclass
class StorageConfig:
    endpoint: str = os.getenv("MINIO_ENDPOINT", "localhost:9000")
    access_key: str = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
    secret_key: str = os.getenv("MINIO_SECRET_KEY", "minioadmin")
    bucket: str = "geip"
    region: str = "us-east-1"


@dataclass
class LakeConfig:
    bronze_path: str = "s3://geip/bronze"
    silver_path: str = "s3://geip/silver"
    gold_path: str = "s3://geip/gold"


config = StorageConfig()
lake = LakeConfig()
