# Project Setup Instructions

This guide provides instructions to set up the development environment for this project. 

## Prerequisites

- Python 3.11
- `pip` (for Python package management)
- Docker

## 1. Clone the Repository

First, clone this repository to your local machine:

```bash
git clone https://github.com/hys89/myrepo.git
cd myrepo
```

## 2. Setup the Virtual Environment

Setup the Python virtual environment `.venv` by executing the `setup_venv.bat` in the root folder.

## 3. Automatic Speech Recognition (ASR) AI model

**To start up the API server locally (via `asr_api.py`):**

1. In a terminal, activate the virtual environment `.venv`
2. Run `python ./asr/asr_api.py`
3. In a separate terminal, test that the API is working by running the following command. Replace `<path_to_file>` with the actual path to the mp3 file. `curl -F "file=@<path_to_file>" http://localhost:8001/asr`

**To start up the API server locally (via Docker):**
1. Open a terminal and ensure that current working directory is `myrepo`
2. Build the docker image using `docker build -f asr/Dockerfile -t asr-api .`
3. Run using `docker run -d -p 8001:8001 asr-api`
4. Test that the API is working by running the following command. Replace `<path_to_file>` with the actual path to the mp3 file. `curl -F "file=@<path_to_file>" http://localhost:8001/asr`

**To transcribe the 4,076 common-voice mp3 files under `cv-valid-dev` folder:**
1. Activate the virtual environment `.venv`
2. Start up the ASR API server locally.
3. Run `python ./asr/cv-decode.py`
4. Results will be saved into the same file `cv-valid-dev.csv`

## 3. Web application for end users to search on cv-valid-dev.csv

**<u>Elasticsearch Backend</u>**
1. In a terminal, cd to the `elastic-backend` folder.
2. Run `docker compose -f docker-compose.yml up` to setup a 2-node Elasticsearch cluster.
3. In another terminal, activate the virtual environment `.venv`
4. Run `python cv-index.py` to index `cs-valid-dev.csv` into Elasticsearch.

**<u>Search UI Frontend</u>**
1. In a terminal, cd to the `search-ui` folder.
2. Run `docker compose -f docker-compose.yml up` to start up the Search UI frontend.
3. Wait for the server to be started.
4. Visit http://localhost:3000/ to view the UI.

**<u>AWS Deployment</u>**
1. URL: [http://ec2-13-229-106-122.ap-southeast-1.compute.amazonaws.com:3000/](http://ec2-13-229-106-122.ap-southeast-1.compute.amazonaws.com:3000/)