import requests
import os

key = os.environ.get("IMGBB_KEY")


def upload_image(image):
    payload = { 'key': key }
    r = requests.post('https://api.imgbb.com/1/upload', params=payload, data={'image': image})
    result = r.json()
    
    url = result['data']['url']
    delete_url = result['data']['delete_url']
    url_thumb = result['data']['thumb']['url']
    url_medium = result['data']['medium']['url']
    
    return (url, url_thumb, url_medium, delete_url)
