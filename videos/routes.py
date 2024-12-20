from datetime import datetime
import os
from typing import BinaryIO
import uuid

from fastapi import APIRouter, HTTPException, Request, status, Depends
from fastapi.responses import StreamingResponse, Response
from starlette._compat import md5_hexdigest
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_db
from movies.models import Record, Episode
from settings import MEDIA_DIR

router = APIRouter(prefix="/api/records")


# TODO: must by async
def send_bytes_range_requests(
    file_obj: BinaryIO, start: int, end: int, chunk_size: int = 8*1024
):
    with file_obj as f:
        f.seek(start)
        while (pos := f.tell()) <= end:
            read_size = min(chunk_size, end + 1 - pos)
            yield f.read(read_size)


def _get_range_header(range_header: str, file_size: int) -> tuple[int, int]:
    def _invalid_range():
        return HTTPException(
            status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE,
            detail=f"Invalid request range (Range:{range_header!r})",
        )

    try:
        h = range_header.replace("bytes=", "").split("-")
        start = int(h[0]) if h[0] != "" else 0
        end = int(h[1]) if h[1] != "" else file_size - 1
    except ValueError:
        raise _invalid_range()

    if start > end or start < 0 or end > file_size - 1:
        raise _invalid_range()
    return start, end


def range_requests_response(
    request: Request, file_path: str, content_type: str
):
    """Returns StreamingResponse using Range Requests of a given file"""

    file_size = os.stat(file_path).st_size
    range_header = request.headers.get("range")

    """Compose etag from last_modified and file_size"""
    last_modified = datetime.fromtimestamp(os.stat(file_path).st_mtime).strftime("%a, %d %b %Y %H:%M:%S")
    etag_base = str(last_modified) + "-" + str(file_size)
    etag = f'"{md5_hexdigest(etag_base.encode(), usedforsecurity=False)}"'

    """Check if the browser sent etag matches the videos etag"""
    request_if_non_match_etag = request.headers.get("if-none-match")

    """if there is a match return 304 unmodified instead of 206 response without video file"""
    if request_if_non_match_etag == etag:
        headers = {
            "cache-control": "public, max-age=86400, stale-while-revalidate=2592000",
            "etag" : etag,
            "last-modified":str(last_modified),
        }
        status_code = status.HTTP_304_NOT_MODIFIED
        return Response(None, status_code=status_code, headers=headers)

    headers = {
        "etag" : etag,
        "content-type": content_type,
        "accept-ranges": "bytes",
        "content-encoding": "identity",
        "content-length": str(file_size),
        "access-control-expose-headers": (
            "content-type, accept-ranges, content-length, "
            "content-range, content-encoding"
        ),
    }
    start = 0
    end = file_size - 1
    status_code = status.HTTP_200_OK


    if range_header is not None:
        start, end = _get_range_header(range_header, file_size)
        size = end - start + 1
        headers["content-length"] = str(size)
        headers["content-range"] = f"bytes {start}-{end}/{file_size}"
        status_code = status.HTTP_206_PARTIAL_CONTENT

    return StreamingResponse(
        send_bytes_range_requests(open(file_path, mode="rb"), start, end),
        headers=headers,
        status_code=status_code,
    )


@router.get("/{item_id}/stream")
async def get_video(
        item_id: uuid.UUID,
        request: Request, 
        db: AsyncSession = Depends(get_db),
):
    record = await Record.by_id(item_id, db)
    episode = await Episode.by_id(record.episode_id, db)
    if not episode.released:
        raise HTTPException(status_code=404)

    return range_requests_response(
        request, file_path=MEDIA_DIR / record.filename,
        content_type="video/mp4"
    )
