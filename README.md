
# Async Image Downloader

Async Image Downloader is a set of Scripts for concurrent download of  images using the Google Search Engine API, leverages Clean Architecture Design principles for reliability , modularity and maintainability.



## Features

- Image Operations eg. Resizing ...
- Asynchronous Execution
- Dockerized Environment 
- PostgreSQL

## Deployment

To deploy this project run 

1. Clone This Repository 

 ```bash
  git clone https://github.com/realBagher/Async_image_downloader.git
```
2. Setup Environment Variables ( ``` .env ``` file ) in the Root Directory of the project

```
# Google Custom Search API 
API_KEY = _some_value_
SEARCH_ENGINE_ID = _some_value_

# DataBase PostgreSQL KEYS
POSTGRES_USER=_some_value_
POSTGRES_PASSWORD=_some_value_
POSTGRES_DB=_some_value_
POSTGRES_HOST=_some_value_
POSTGRES_PORT=_some_value_

```

3. if you are running this on your local machine:  



```
python -m venv you_enviroment_name
.\venv you_enviroment_name

pip install -r requirments.txt 

```

4. if using Docker 
Build the docker image and run services using 

```

docker-compose up --build

```





## Usage/Examples

#### Run this if running on you local machine 

```python 
python src\main.py 
```
and fill the console based on the prompts request 


#### Run this if using Docker 

fill the required varibales based on the prompts request 

```python 
docker exec -it <container_id> bash
```
after that run the following commands
```python 

cd src
python main.py 

```

you can find you container id based by using ``` docker ps ``` command 