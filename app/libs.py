import json
from app.models import UserSchema
from fastapi import Body


def load_file(path):
    with open(path, "r") as f:
        return json.load(f)


def load_metadata() -> dict:
    """Carrega os metadados do arquivo metadata.json

    Returns:
        Dict: Metadados da documentação
    """
    return load_file('static/tags_metadata.json')
