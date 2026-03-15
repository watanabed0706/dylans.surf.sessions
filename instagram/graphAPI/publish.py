import os
import sys
from dotenv import load_dotenv
import time
import requests

# --- Configuration ---
load_dotenv()
ACCESS_TOKEN = os.environ['IG_ACCESS_TOKEN']
IG_USER_ID = os.environ['IG_USER_ID']
NGROK_URL = sys.argv[1]
MEDIA_DIR = "../to_upload"
ENDPOINT_BASE = "https://graph.instagram.com/v25.0/"

def video_container(mp4_url):
    url = f"{ENDPOINT_BASE}{IG_USER_ID}/media"
    payload = {
        "media_type":"VIDEO",
        "video_url":mp4_url,
        "is_carousel_item":"TRUE",
        "access_token":ACCESS_TOKEN
    }
    r = requests.post(url, data=payload)
    return r.json().get('id')

def image_container(jpg_url):
    url = f"{ENDPOINT_BASE}{IG_USER_ID}/media"
    payload = {
        "image_url":jpg_url,
        "is_carousel_item":"TRUE",
        "access_token":ACCESS_TOKEN
        }
    r = requests.post(url, data=payload)
    return r.json().get('id')

def carousel_container(id_list):
    url = f"{ENDPOINT_BASE}{IG_USER_ID}/media"
    payload = {
        "media_type":"CAROUSEL",
        "caption":"This is an Automated Post.",
        "children":",".join([str(id) for id in id_list]),
        "access_token":ACCESS_TOKEN
    }
    r = requests.post(url, data=payload)
    return r.json().get('id')

def publish_media(creation_id):
    url = f"{ENDPOINT_BASE}{IG_USER_ID}/media_publish"
    payload = {
		"creation_id": f"{creation_id}",
		"access_token": ACCESS_TOKEN
	}

    status_url = f"{ENDPOINT_BASE}{creation_id}"
    
    while True:
        status = requests.get(status_url, params=params).json().get('status_code')
        if ('IN_PROGRESS' != status):
            print(f"Done Processing; Status: {status}")
            break
        print(f"Status: {status}... waiting 30s")
        time.sleep(30)

    return (requests.post(url, data=payload).json().get('id'))



# Main 

container_IDs = []
mp4_list = []

for filename in sorted(os.listdir(MEDIA_DIR)):
    file_path = f"{NGROK_URL}/{filename}"
    ext = filename.lower().split('.')[-1]
    
    if ext in ['png', 'jpg', 'jpeg']:
        cid = image_container(file_path)
        container_IDs.append(cid)
        
    elif ext == 'mp4':
        cid = video_container(file_path)
        mp4_list.append(cid)
        container_IDs.append(cid)
    
    if (cid != None):
        print(f"{filename} Media Container Created!  ID:{cid}")
    else:
        print(f"something went WRONG with {filename}")

params = {"fields": "status_code", "access_token": ACCESS_TOKEN}

while True:
    status_list = []
    for mp4 in mp4_list:
        url = f"{ENDPOINT_BASE}{mp4}"
        status_list.append(requests.get(url, params=params).json().get('status_code'))

    if ('IN_PROGRESS' not in status_list):
        print("Videos No longer Processing")
        print("Moving on to Carousel...")
        break
    print(f"Video status: {status_list}... waiting 30s")
    time.sleep(30)

carousel = carousel_container(container_IDs)
print(f"Carousel ID is: {carousel}")
pub = publish_media(carousel)
if (pub == None):
    print("Unsuccessful Carousel Publish")
else:
    print(f"Carousel Published with ID: {pub}")


