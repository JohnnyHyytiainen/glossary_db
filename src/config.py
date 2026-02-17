# Kod: Engelska
# Kommentarer: Svenska
# För att ladda in .env säkert (med Pydantic).
from pydantic_settings import BaseSettings, SettingsConfigDict


# Klass för att definiera vilka variabler som KRÄVS ifrån .env
class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_HOST: str
    DB_PORT: str

    # Pydantic läser automatiskt in .env filen
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True)

    @property
    def DATABASE_URL(self) -> str:
        """Building connection string automatically"""
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
# Skapa en instans som jag kan importera i andra filer
settings = Settings()