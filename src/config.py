from dotenv import load_dotenv # type: ignore
import requests # type: ignore
import html
import json
import os

load_dotenv()

ARTIFACTORY_URL = os.getenv('URL')
TOKEN  = os.getenv('TOKEN')

headers = {
    "X-JFrog-Art-Api": TOKEN,
    "Content-Type": "application/json",
}

spacing = 35

