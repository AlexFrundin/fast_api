from fastapi import APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse, FileResponse
# from starlette.responses import FileResponse

from app.utils_video import gen_frames


video = APIRouter(prefix='/video',
                  tags=['video'],
                  responses={404: {'description': 'Not found'}})

video.mount('/templates', StaticFiles(directory='templates'), name='templates')


@video.get('/')
async def get_html():
    return FileResponse('templates/index.html')


@video.get('/stream')
async def get_stream():
    return StreamingResponse(gen_frames(),
                             media_type="multipart/x-mixed-replace;boundary=frame")