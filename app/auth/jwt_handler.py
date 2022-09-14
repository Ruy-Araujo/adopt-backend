import time
import jwt
from decouple import config
import os


JWT = os.getenv("SECRET_KEY")
JWT_ALGORITHM = os.getenv("ALGORITHM")


def token_response(token: str):
    """Retorna os tokens gerados

    Args:
        token (str): Token de acesso

    Returns:
        JWT: Access Token
    """
    return {
        'access_token': token
    }


def signJWT(userID: str):
    """Função para autenticação do JWT

    Args:
            userID (str): ID do usuário

    Returns:
            JWT: Token de acesso
    """
    payload = {
        "userID": userID,
        "expiry": time.time() + 86400
    }
    token = jwt.encode(payload, JWT, algorithm=JWT_ALGORITHM)
    return token


def decodeJWT(token: str):
    """Função para decodificar o JWT

    Args:
            token (str): Token de acesso

    Returns:
            JWT: Token de acesso
    """
    try:
        decode_token = jwt.decode(token, JWT, algorithm=JWT_ALGORITHM)
        return decode_token if decode_token["expires"] >= time.time() else None
    except jwt.ExpiredSignatureError:
        return "Token expirado"
    except jwt.InvalidTokenError:
        return "Token inválido"
    except:
        return {}
