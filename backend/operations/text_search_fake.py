from towhee import pipe, ops
from config import MILVUS_HOST, MILVUS_PORT, MILVUS_COLLECTION, MONGO_URI, MONGO_DB, MONGO_COLLECTION, THRESHOLD, DEVICE


def do_text_search(img_path, topk):
    milvus_search_pipe = (
        pipe.input('query')
            .map('query', 'emb', ops.image_text_embedding.clip(model_name='clip_vit_base_patch32', modality='text', device=DEVICE))
            .map('emb', 'emb', ops.towhee.np_normalize())
            .map('emb', 'ret',  ops.ann_search.milvus_client(
                host=MILVUS_HOST, port=MILVUS_PORT, limit=topk, collection_name=MILVUS_COLLECTION, output_fields=['path']
            ))
            .flat_map('ret', 'ret', lambda x: x)
            .map('ret', 'ret_id', lambda x: x[0])
            .map('ret', 'ret_img', lambda x: x[2])
            .map('ret_id', 'sku', ops.storage.mongo_search(
                uri=MONGO_URI, database=MONGO_DB, collection=MONGO_COLLECTION, schema=['id'], exclude=['_id']
            ))
            .map('sku', 'sku', ops.towhee.filter(lambda x: x['score'] > THRESHOLD)))
    atlas_search_pipe = (
         pipe.input('query')
            .map('query', 'emb', ops.image_text_embedding.clip(model_name='clip_vit_base_patch32', modality='text', device=DEVICE))
            .map('emb', 'emb', ops.towhee.np_normalize())
            .map('emb', 'ret',  ops.ann_search.milvus_client(
                host=MILVUS_HOST, port=MILVUS_PORT, limit=topk, collection_name=MILVUS_COLLECTION, output_fields=['path']
            ))
            .flat_map('ret', 'ret', lambda x: x)
            .map('ret', 'ret_id', lambda x: x[0])
            .map('ret', 'ret_img', lambda x: x[2])
            .map('ret_id', 'sku', ops.storage.mongo_search(
                uri=MONGO_URI, database=MONGO_DB, collection=MONGO_COLLECTION, schema=['id'], exclude=['_id']
            ))
            )

    text_search_pipe = atlas_search_pipe.concat(milvus_search).output('ret')
    return text_search_pipe(img_path).to_list()