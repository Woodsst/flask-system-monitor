from pydantic import BaseSettings, Field


class Postgres(BaseSettings):
    """postgres settings"""
    password: str = Field("123")
    host: str = Field("localhost")
    port: int = Field(5432)
    name: str = Field("clients")
    username: str = Field("wood")

    class Config:
        env_prefix = "DB_"


class App(BaseSettings):
    """application settings"""
    host: str = Field("localhost")
    port: int = Field(5000)

    class Config:
        env_prefix = "APP_"


class Settings(BaseSettings):
    """all settings"""
    storage: Postgres = Postgres()
    app: App = App()


settings = Settings()
