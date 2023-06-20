import uvicorn
import os
import argparse
import logging
from urllib.request import urlretrieve
from typing import Dict, Any

from fastapi import FastAPI, File, UploadFile
from fastapi.param_functions import Form
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from config import UPLOAD_PATH, DEVICE
from log import LOGGER
from operations.image_search import do_image_search
from operations.text_search import do_text_search
from operations.set_collection import set_collection
from operations.prepare_collection import prepare_collection

from fastapi.middleware.cors import CORSMiddleware

if not os.path.exists(UPLOAD_PATH):
    os.makedirs(UPLOAD_PATH)
    LOGGER.info(f"make the dir: {UPLOAD_PATH}")

IMAGR_ROOT = None
HOST = None
PORT = None
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


def path_to_url(path):
    return path.replace(IMAGR_ROOT, '{}:{}/images/'.format(HOST, PORT))


@app.post('/img/search')
async def image_search(image: UploadFile, topk: int):
    try:
        content = await image.read()
        img_path = os.path.join(UPLOAD_PATH, image.filename)
        with open(img_path, "wb+") as f:
            f.write(content)
        res = do_image_search(img_path, topk)
        for i in range(len(res)):
            res[i][0] = path_to_url(res[i][0])
        LOGGER.info(f"Successfully retrieved {len(res)} similar images!")
        return res
    except Exception as e:
        LOGGER.error(e)
        return {'status': False, 'msg': e}, 400


@app.post('/path/search')
async def path_search(path: str, topk: int):
    try:
        res = do_image_search(path, topk)
        for i in range(len(res)):
            res[i][0] = path_to_url(res[i][0])
        LOGGER.info(f"Successfully retrieved {len(res)} similar images!")
        return res
    except Exception as e:
        LOGGER.error(e)
        return {'status': False, 'msg': e}, 400


@app.post('/text/search')
async def text_search(text: str, topk: int):
    try:
        res = do_text_search(text, topk)
        for i in range(len(res)):
            res[i][0] = path_to_url(res[i][0])
        LOGGER.info(f"Successfully retrieved {len(res)} similar images!")
        return res
    except Exception as e:
        LOGGER.error(e)
        return {'status': False, 'msg': e}, 400


@app.get('/data')
def get_img(image_path):
    # Get the image file
    try:
        LOGGER.info(f"Successfully load image: {image_path}")
        return FileResponse(image_path)
    except Exception as e:
        LOGGER.error(f"Get image error: {e}")
        return {'status': False, 'msg': e}, 400


def parse_arguments():
    parser = argparse.ArgumentParser(description='Script description.')
    parser.add_argument('--host', type=str, default='127.0.0.1', help='Host IP address')
    parser.add_argument('--port', type=int, default=5000, help='Port number')
    parser.add_argument('--root', type=str, default=None, help='Root path for loading images.')
    parser.add_argument('--csv', type=str, required=False, default=None, help='path to sku data.')
    parser.add_argument('--num', type=int, required=False, default=100, help='Number of insert images.')
    parser.add_argument('--purge', action='store_true', help='whether to clear existing collection.')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel(logging.WARNING)
    args = parse_arguments()
    set_collection(args.purge)
    if args.csv and args.root:
        prepare_collection(args.csv, args.root, args.num)
    app.mount("/images", StaticFiles(directory=args.root), name="images")
    IMAGR_ROOT = args.root
    HOST = args.host
    PORT = args.port
    uvicorn.run(app=app, host=HOST, port=PORT)
