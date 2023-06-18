import os

############### Milvus Configuration ###############
MILVUS_HOST = os.getenv('MILVUS_HOST', '127.0.0.1')
MILVUS_PORT = os.getenv('MILVUS_PORT', '19530')
TOP_K = int(os.getenv('TOP_K', '5'))
MILVUS_COLLECTION = os.getenv('COLLECTION_NAME', 'fashion')
INDEX_TYPE = os.getenv('INDEX_TYPE', 'IVF_FLAT')
METRIC_TYPE = os.getenv('METRIC_TYPE', 'L2')
VECTOR_DIMENSION = int(os.getenv('VECTOR_DIMENSION', '512'))
THRESHOLD = float(os.getenv('THRESHOLD', '0.5'))

############### MongoDB Configuration ###############
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
MONGO_DB = os.getenv('MONGO_DB', 'fashion')
MONGO_COLLECTION = os.getenv('MONGO_COLLECTION', 'fashion')

############### Device Configuration ###############
DEVICE = os.getenv('DEVICE', 'cpu')

############### Data Path ###############
UPLOAD_PATH = os.getenv('UPLOAD_PATH', 'tmp/search-images')

############### Number of log files ###############
LOGS_NUM = int(os.getenv('logs_num', '0'))
