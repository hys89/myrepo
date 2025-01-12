# Project Setup Instructions

This guide provides instructions to set up the development environment for this project. 

## Prerequisites

- Python 3.11
- `pip` (for Python package management)

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
1. Open a terminal and ensure that current working directory is `myrepo`.
2. Build the docker image using `docker build -f asr/Dockerfile -t asr-api .`
3. Run using `docker run -d -p 8001:8001 asr-api`
4. Test that the API is working by running the following command. Replace `<path_to_file>` with the actual path to the mp3 file. `curl -F "file=@<path_to_file>" http://localhost:8001/asr`

**To transcribe the 4,076 common-voice mp3 files under `cv-valid-dev` folder:**
1. Activate the virtual environment `.venv`
2. Start up the ASR API server locally.
3. Run `python ./asr/cv-decode.py`

