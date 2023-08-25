# Ask NERVE?

## Overview
POC to demonstrate integration of LLM to ask questions on NERVE without touching any datasets by ChatGPT

## Requirements
Python 3.5.2+

## Usage
To run the server, please execute the following from the root directory:

```
pip3 install -r requirements.txt
streamlit run streamlit_app.py
```




## Running with Docker

To run the server on a Docker container, please execute the following from the root directory:

```bash
# building the image
docker build -t mti-speech-generator .

# starting up a container
docker run -p 8501:8501 --env DATABRICKS_TOKEN="" --env OPENAI_TOKEN="" --env DATABRICKS_SQL_HOSTNAME="" --env DATABRICKS_SQL_HTTP_PATH="" mti-speech-generator 
```

## TODO
Remove SSL urllib3.disable_warnings() for accounts.cloud.databricks.com, as their SSL certificate is not available in Ubuntu/Python