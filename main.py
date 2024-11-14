#!/usr/bin/env python3

"""Cinemafan entrypoint."""


import uvicorn

from settings import HOST, PORT, RELOAD, WORKERS

if __name__ == '__main__':
    uvicorn.run(
        "app:app",
        host=HOST,
        port=PORT,
        reload=RELOAD,
        workers=WORKERS,
    )
