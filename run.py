import os

from dotenv import load_dotenv
import uvicorn

load_dotenv()

if __name__ == '__main__':
    HOST = os.getenv("HOST")
    PORT = int(os.getenv("PORT"))
    RELOAD = os.getenv("RELOAD") == "True"
    WORKERS = 1 if RELOAD else os.cpu_count() + 1

    uvicorn.run(
        "app:app",
        host=HOST,
        port=PORT,
        reload=RELOAD,
        workers=WORKERS,
    )
