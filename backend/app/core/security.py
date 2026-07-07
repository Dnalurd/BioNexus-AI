"""Core security utilities including JWT, encryption, and password hashing."""
import secrets
from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from cryptography.fernet import Fernet
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class SecurityUtils:
    """Utility class for security operations."""

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using bcrypt.

        Args:
            password: Plain text password

        Returns:
            Hashed password
        """
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against a hash.

        Args:
            plain_password: Plain text password
            hashed_password: Hashed password from database

        Returns:
            True if password matches, False otherwise
        """
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def create_access_token(
        data: dict[str, Any], expires_delta: Optional[timedelta] = None
    ) -> str:
        """Create a JWT access token.

        Args:
            data: Payload data to encode
            expires_delta: Token expiration time delta

        Returns:
            Encoded JWT token
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(
                minutes=settings.access_token_expire_minutes
            )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.secret_key, algorithm=settings.algorithm
        )
        return encoded_jwt

    @staticmethod
    def create_refresh_token(data: dict[str, Any]) -> str:
        """Create a JWT refresh token.

        Args:
            data: Payload data to encode

        Returns:
            Encoded JWT refresh token
        """
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            days=settings.refresh_token_expire_days
        )
        to_encode.update({"exp": expire, "type": "refresh"})
        encoded_jwt = jwt.encode(
            to_encode, settings.secret_key, algorithm=settings.algorithm
        )
        return encoded_jwt

    @staticmethod
    def decode_token(token: str) -> dict[str, Any]:
        """Decode and validate a JWT token.

        Args:
            token: JWT token to decode

        Returns:
            Decoded token payload

        Raises:
            JWTError: If token is invalid or expired
        """
        try:
            payload = jwt.decode(
                token, settings.secret_key, algorithms=[settings.algorithm]
            )
            return payload
        except JWTError as e:
            raise JWTError("Invalid token") from e

    @staticmethod
    def encrypt_data(data: str) -> str:
        """Encrypt sensitive data using Fernet.

        Args:
            data: Plain text data to encrypt

        Returns:
            Encrypted data
        """
        cipher_suite = Fernet(settings.encryption_key.encode())
        encrypted = cipher_suite.encrypt(data.encode())
        return encrypted.decode()

    @staticmethod
    def decrypt_data(encrypted_data: str) -> str:
        """Decrypt sensitive data using Fernet.

        Args:
            encrypted_data: Encrypted data to decrypt

        Returns:
            Decrypted plain text data
        """
        cipher_suite = Fernet(settings.encryption_key.encode())
        decrypted = cipher_suite.decrypt(encrypted_data.encode())
        return decrypted.decode()

    @staticmethod
    def generate_secure_token(length: int = 32) -> str:
        """Generate a secure random token.

        Args:
            length: Token length in bytes

        Returns:
            Secure random token (hex encoded)
        """
        return secrets.token_hex(length)
