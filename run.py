import uvicorn

from dotenv import load_dotenv
load_dotenv()

if __name__ == '__main__':
    uvicorn.run("app:app", reload=True)
