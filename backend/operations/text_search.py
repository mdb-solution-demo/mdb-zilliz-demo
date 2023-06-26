from towhee import pipe, ops
from typing import Union

import pymongo
from config import MILVUS_HOST, MILVUS_PORT, MILVUS_COLLECTION, MONGO_URI, MONGO_DB, MONGO_COLLECTION, THRESHOLD, DEVICE


def do_text_search(img_path, topk):
    text_search_pipe = (
        pipe.input('query')
            .map('query', 'emb', ops.image_text_embedding.clip(model_name='clip_vit_base_patch32', modality='text', device=DEVICE))
            .map('emb', 'emb', ops.towhee.np_normalize())
            .map('emb', 'ret',  ops.ann_search.milvus_client(
                host=MILVUS_HOST, port=MILVUS_PORT, limit=topk, collection_name=MILVUS_COLLECTION, output_fields=['path']
            ))
            .flat_map('ret', 'ret', lambda x: x)
            .map('ret', 'ret_id', lambda x: x[0])
 #           .map('ret', 'ret_img', lambda x: x[2])
            .window_all('ret_id', 'sku', ops.storage.mongo_search(
               uri=MONGO_URI, database=MONGO_DB, collection=MONGO_COLLECTION, schema=['id'], exclude=['_id']
            ))
 #           .map('sku', 'ret_img', lambda x: x[0])
            .output('sku')
    )


    list = []
   
    if  len(text_search_pipe(img_path).to_list()) > 0 : 

        list = text_search_pipe(img_path).to_list()
        list = list[0]
        if len(list) >0 : 
            list = list[0]
          
    return list

#   return text_search_pipe(img_path).to_list()

def do_text_search2(img_path, topk, morequery):
    print("Execute do_text_search2")
    text_search_pipe = (
        pipe.input('query')
            .map('query', 'emb', ops.image_text_embedding.clip(model_name='clip_vit_base_patch32', modality='text', device=DEVICE))
            .map('emb', 'emb', ops.towhee.np_normalize())
            .map('emb', 'ret',  ops.ann_search.milvus_client(
                host=MILVUS_HOST, port=MILVUS_PORT, limit=topk, collection_name=MILVUS_COLLECTION, output_fields=['path']
            ))
            .flat_map('ret', 'ret', lambda x: x)
            .map('ret', 'ret_id', lambda x: x[0])
 #           .map('ret', 'ret_img', lambda x: x[2])
            .window_all('ret_id', 'sku', ops.mongodb.mongo_search(
               uri=MONGO_URI, database=MONGO_DB, collection=MONGO_COLLECTION, moreQuery=morequery, schema=['id'], exclude=['_id']
            ))
 #           .map('sku', 'ret_img', lambda x: x[0])
            .output('sku')
    )

    print("queryMore:"+morequery)
    list = []
   
    if  len(text_search_pipe(img_path).to_list()) > 0 : 

        list = text_search_pipe(img_path).to_list()
        list = list[0]
        if len(list) >0 : 
            list = list[0]
          
    return list