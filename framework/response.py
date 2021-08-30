from starlette.responses import Response, JSONResponse, FileResponse, RedirectResponse, StreamingResponse


def html(content: str, status: int = 200) -> Response:
    return Response(content=content, status_code=status, media_type='text/html')

def text(content: str, status: int = 200) -> Response:
    return Response(content=content, status_code=status, media_type='text/plain')

def json(content: str, status: int = 200) -> Response:
    return JSONResponse(content=content, status_code=status)

def redirect(url: str, status: int = 200) -> Response:
    return RedirectResponse(url=url, status_code=status)

def file(path: str, filename: str = None, media_type: str = None) -> Response:
    return FileResponse(path=path, media_type=media_type, filename=filename)

def streaming(content: str, status: int = 200) -> Response:
    return StreamingResponse(content=content, status_code=status)