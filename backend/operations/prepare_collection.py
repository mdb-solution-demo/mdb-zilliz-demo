import csv

import pandas as pd
from towhee import pipe, ops

from config import MILVUS_HOST, MILVUS_PORT, MILVUS_COLLECTION, MONGO_URI, MONGO_DB, MONGO_COLLECTION, THRESHOLD, DEVICE


def prepare_collection(csv_path, root_path, num):
    img_data = pd.read_csv(csv_path, usecols=range(10))[:num]
    paths = img_data.id.apply(lambda x: root_path + str(x) + '.jpg').to_list()

    with open(csv_path, encoding='utf-8') as file:
        dreader = csv.DictReader(file)
        style_data = list(dreader)
    skus = style_data[:num]

    init_pipe = (
        pipe.input( 'path', 'sku')
            .map('sku', 'id', lambda x: x['id'])
    )

    sku_pipe = (
        init_pipe.map('sku', 'insert_id', ops.mongodb.mongo_insert(uri=MONGO_URI, database=MONGO_DB, collection=MONGO_COLLECTION))
    )

    img_pipe = (
        init_pipe.map('path', 'img', ops.image_decode.cv2_rgb())
            .map('img', 'emb', ops.image_text_embedding.clip(model_name='clip_vit_base_patch32', modality='image', device=DEVICE))
            .map('emb', 'emb', ops.towhee.np_normalize())
            .map(('id', 'path', 'emb'), 'pk', ops.ann_insert.milvus_client(
                host=MILVUS_HOST, port=MILVUS_PORT, collection_name=MILVUS_COLLECTION
            ))
    )

    insert_pipe = (
        img_pipe.concat(sku_pipe).output()
    )

    inputs = [(path, sku) for path, sku in zip(paths, skus)]
    print(f'Preparing collection, {len(inputs)} images to insert...')
    insert_pipe.batch(inputs)
