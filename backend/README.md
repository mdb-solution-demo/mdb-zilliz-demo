# zilliz-mongodb-demo

## Introduction 
This is a demo project that showcases the integration of Milvus and MongoDB for an e-commerce scenario. It supports searching for similar images within uploaded contents via image and text. The project is built with FastAPI to perform insert and search operations.

## Prerequisites
Before running the demo, make sure you have the following service started:
- Milvus: Install and configure Milvus, refer to [Milvus docs](https://milvus.io/docs/install_standalone-docker.md).
- MongoDB: Install and configure MongoDB, refer to [MongoDB docs](https://www.mongodb.com/docs/manual/administration/install-community/).


## Getting Started
To get started with the demo, follow the steps below:
1. Clone the repository and enter the project directory.
    ```bash
    git clone https://github.com/Chiiizzzy/zilliz-mongodb-demo.git
    ```

2. Install the required Python packages
    ```bash
    pip install -r requirements.txt.
    ```

3. Prepare the dataset, for reference, from [kaggle](https://www.kaggle.com/datasets/paramaggarwal/fashion-product-images-dataset?resource=download)

4. Config the service by modifying `config.py`.

5. Start the server
    ```bash
    python main.py --csv <path/to/csv> --root <root/path/of/images> --num <number_of_images> --purge
    ```
    Replace the values inside `<>`.
    - *csv*: str, the path to the csv.
    - *root*: str, the root path of the images.
    - *num*: int, the number of images to insert into Milvus and MongoDb collection.
    - *purge*: no value, once clarified, will clear existing collection.

## User Interface

### Image Search
**Endpoint:** `POST /img/seach`

This endpoint allows you to search for similar images based on an uploaded image.

**Request Parameters:**
 - `image` (file): The image file to search.
 - `topk` (int): The number of similar images to retrieve.

**Example Request:**

```bash
curl -X 'POST' \
    'http://localhost:5000/img/search' \
    -H 'accept: application/json' \
    -H 'Content-Type: multipart/form-data' \
    -F 'image=@example.jpg;type=image/jpeg' \
    -F 'topk=5'
```
Replace `example.jpg` with actual query image path.


### Text Search
**Endpoint:** `POST /text/seach`

This endpoint allows you to search for similar images based on a provided text query.

**Request Parameters:**
 - `text` (str): The text query to search.
 - `topk` (int): The number of similar texts to retrieve.

**Example Request:**      
```bash
curl -X 'POST' \
  'http://localhost:5000/text/search?text=example_text' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'topk=5'
```
Replace `example_text` with actual description.


### Path Search
**Endpoint:** `POST /path/seach`

This endpoint allows you to search for similar images based on the path to query image.

**Request Parameters:**
 - `path` (str): The path to the query image.
 - `topk` (int): The number of similar texts to retrieve.

**Example Request:**      
```bash
curl -X 'POST' \
  'http://localhost:5000/path/search?path=example/path.jpg' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'topk=5'
```

Replace `example/path.jpg` with actual path to query image.


### Interactive API documentation

To try the examples out, you can also go to `http://localhost:5000/docs`.
