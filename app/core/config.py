"""Módulo de configuración global de la aplicación RIETI.

Define las variables de entorno requeridas para la conexión a la base de datos MySQL,
la autenticación federada con AWS Cognito y la configuración del servidor FastAPI.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    """Configuración centralizada de la aplicación y carga de variables de entorno.

    Attributes:
        PROJECT_NAME (str): Nombre del proyecto o título de la API.
        MYSQL_DB_HOST (str): Host o dirección IP del servidor MySQL.
        MYSQL_DB_PASSWORD (str): Contraseña para el usuario de la base de datos.
        MYSQL_DB_NAME (str): Nombre de la base de datos MySQL.
        MYSQL_DB_USER (str): Nombre de usuario de la base de datos.
        MYSQL_DB_PORT (str): Puerto de conexión del servidor MySQL.
        AWS_COGNITO_REGION (str): Región de AWS donde se aloja el User Pool de Cognito.
        COGNITO_USER_POOL_ID (str): Identificador único del User Pool de AWS Cognito.
        ANDROID_APP_CLIENT_ID (str): Client ID de la aplicación Android en Cognito.
        ALLOWED_ORIGINS (list[str]): Orígenes permitidos para peticiones CORS.
        S3_BUCKET_NAME (str): Nombre de la bucket s3 donde se almacenan las evidencias
    """

    PROJECT_NAME: str = "RIETI API"

    MYSQL_DB_HOST: str
    MYSQL_DB_PASSWORD: str
    MYSQL_DB_NAME: str
    MYSQL_DB_USER: str
    MYSQL_DB_PORT: str

    AWS_COGNITO_REGION: str
    COGNITO_USER_POOL_ID: str
    ANDROID_APP_CLIENT_ID: str

    S3_BUCKET_NAME: str

    ALLOWED_ORIGINS: list[str] = ['*']

    model_config = SettingsConfigDict(
        env_file=os.getenv("ENV_FILE", ".env"),
        extra="ignore"
    )

settings = Settings()