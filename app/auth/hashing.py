from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha é igual a senha criptografada

    Args:
        plain_password (str): Senha a ser verificada
        hashed_password (str): Senha criptografada

    Returns:
        bool: Se a senha é igual a senha criptografada
    """
    return pwd_context.verify(plain_password, hashed_password)


def password_hash(password: str) -> str:
    """Criptografa a senha

    Args:
        password (str): Senha a ser criptografada

    Returns:
        str: Senha criptografada
    """
    return pwd_context.hash(password)
