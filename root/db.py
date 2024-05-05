import os


def build_url(data: dict) -> str:
    """
    Builds url for database connection.

    Args:
        data: database connection data.

    Returns:
        str: url for database connection.
    """

    engine = data.get("engine")
    name = data.get("name")
    user = data.get("user")
    password = data.get("password")
    host = data.get("host")
    port = data.get("port")

    auth: str = (
        f"{user}:{password}"
        if user is not None and password is not None
        else user if user is not None else None
    )
    location: str = (
        f"{host}:{port}"
        if host is not None and port is not None
        else host if host is not None else None
    )
    credentials: str = (
        f"{auth}@{location}"
        if auth is not None and location is not None
        else location if location is not None else None
    )

    return (
        f"{engine}://{credentials}/{name}"
        if credentials is not None
        else f"{engine}:///{name}"
    )


DB_URL = build_url(
    {
        "engine": os.getenv("DB_ENGINE"),
        "name": os.getenv("DB_NAME"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "host": os.getenv("DB_HOST"),
        "port": os.getenv("DB_PORT"),
    }
)
