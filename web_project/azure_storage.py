import os
from storages.backends.azure_storage import AzureStorage


class AzureMediaStorage(AzureStorage):
    account_name = os.getenv('storage444ie')
    account_key = os.getenv('5SG8H2Yc9hfL9FcAYsGb+nJzVZ5zsy7Zl4dkCVI3gCYQGI6jBwf1r+oyiXcdE6QePjoS89mzi4bR+AStI7BXmw==')
    azure_container = 'media'
    expiration_secs = None


class AzureStaticStorage(AzureStorage):
    account_name = os.getenv('storage444ie')
    account_key = os.getenv('5SG8H2Yc9hfL9FcAYsGb+nJzVZ5zsy7Zl4dkCVI3gCYQGI6jBwf1r+oyiXcdE6QePjoS89mzi4bR+AStI7BXmw==')
    azure_container = 'static'
    expiration_secs = None
