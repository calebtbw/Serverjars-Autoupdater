#!/usr/bin/python3.8

import os
import wget
import json
import time
import hashlib
import requests


def post_to_slack(message):
    webhook_url = "some-webhook-url-here"

    encoded_data = json.dumps({'text': message}).encode('utf-8')
    response = requests.post(
        webhook_url,
        data=encoded_data
    )
    # print(str(response.status_code))

jar_name = "BungeeCord"
filepath = "/home/minecraft/multicraft/jar/bungeecord-latest.jar"
dl_url = "https://serverjars.com/api/fetchJar/bungeecord"
ver_url = "https://serverjars.com/api/fetchLatest/bungeecord"

response = requests.get(ver_url).content
currentHash = hashlib.sha224(response).hexdigest()

ver_response = requests.get(ver_url)
data = ver_response.json()
version = data["response"]["version"]

# post_to_slack(f"Fetching latest {jar_name} jar...")
time.sleep(10)

if not os.path.exists(filepath):
    wget.download(dl_url, filepath)
    post_to_slack(f"{jar_name} {version} has been downloaded!")

while True:
    try:
        response = requests.get(ver_url).content
        currentHash = hashlib.sha224(response).hexdigest()

        time.sleep(7200)

        response = requests.get(ver_url).content
        newHash = hashlib.sha224(response).hexdigest()

        if newHash == currentHash:
            # post_to_slack(f"No updates for {jar_name}.")
            continue

        else:
            if os.path.exists(filepath):
                os.remove(filepath)
                # post_to_slack(f"Removing old {jar_name} jar...")

                wget.download(dl_url, filepath)
                post_to_slack(f"{jar_name} has been updated to {version}!")
            
            response = requests.get(ver_url).content
            currentHash = hashlib.sha224(response).hexdigest()

            time.sleep(7200)
            continue

    except Exception as e:
        post_to_slack(f"Error occured in {os.path.basename(__file__)}!")