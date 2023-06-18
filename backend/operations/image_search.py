from towhee import pipe, ops
from config import MILVUS_HOST, MILVUS_PORT, MILVUS_COLLECTION, MONGO_URI, MONGO_DB, MONGO_COLLECTION, THRESHOLD, TOP_K, DEVICE

def do_image_search(img_path):
    image_search_pipe = (
        pipe.input('query')
            .map('query', 'img', ops.image_decode.cv2_rgb())
            .map('img', 'emb', ops.image_text_embedding.clip(model_name='clip_vit_base_patch32', modality='image', device=DEVICE))
            .map('emb', 'emb', ops.towhee.np_normalize())
            .map('emb', 'ret',  ops.ann_search.milvus_client(
                host=MILVUS_HOST, port=MILVUS_PORT, limit=TOP_K, collection_name=MILVUS_COLLECTION, output_fields=['path']
            ))
            .flat_map('ret', 'ret', lambda x: [i for i in x if i[1] <= THRESHOLD])
            .map('ret', 'ret_id', lambda x: x[0])
            .map('ret', 'ret_img', lambda x: x[2])
            .map('ret_id', 'sku', ops.storage.mongo_search(
                uri=MONGO_URI, database=MONGO_DB, collection=MONGO_COLLECTION, schema=['id'], exclude=['_id']
            ))
            .output('ret_img', 'sku')
    )

    return image_search_pipe(img_path).to_list()