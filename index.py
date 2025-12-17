

import base64
import requests
from dotenv import load_dotenv
import os
import json
import boto3

load_dotenv('.env')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
ACCESS_KEY = os.getenv('ACCESS_KEY')
ACCESS_SECRET = os.getenv('ACCESS_SECRET')
REGION_NAME = os.getenv('REGION_NAME')
#    acreating a tocken function

def access_token():
    try:
        if not CLIENT_ID or not CLIENT_SECRET:
            raise ValueError("CLIENT_ID or CLIENT_SECRET not found in environment variables")
        # combining client id and client secret
        credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
        # encoding the credentials to base64
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        response = requests.post(
            'https://accounts.spotify.com/api/token',
            headers={"Authorization": f"Basic {encoded_credentials}"},
            data={"grant_type": "client_credentials"})
        
        if response.status_code != 200:
            print(f"Spotify API Error (Status {response.status_code}): {response.text}")
            response.raise_for_status()
        
        # print("Token generated successfully")
        return response.json()['access_token']
    except Exception as e:
        print("Failed to generate token:", e)
        return None
# print(access_token())        



# latest release date: 2024-06-01

def get_new_release():
    try:      
       token = access_token()
       header = {"Authorization": f"Bearer {token}"}
       param = {'limit':50}
       response = requests.get('https://api.spotify.com/v1/browse/new-releases', headers=header,params=param) 

       if response.status_code == 200:
        data=response.json()
        release=[]
        albums=data['albums']['items']
        for i in albums:
           a={
              'album_name':i['name'],
              'release_date':i['release_date'],
              'artist_name': i['artists'][0]['name'],
              'album_type': i['album_type'],
              'total_tracks': i['total_tracks'],
              'spotify_url': i['external_urls']['spotify'],
              'album_image': i['images'][0]['url'] if i['images'] else None
           }
           release.append(a)
        # Save to JSON file
        with open('spotify_releases.json', 'w') as f:
            json.dump(release, f, indent=2)
        print("JSON data saved to spotify_releases.json")
    except Exception as e:
        print("Failed to get new releases:", e)  

    try:
        BUCKET_NAME ="kinu.bucket"
        OBJECT_NAME ="spotify_releases.json"
        FILE_NAME =r"D:\ABHI\Spotify\Spotify-Data\spotify_releases.json"

    
        S3_CLIENT = boto3.client(service_name='s3',
                 region_name=REGION_NAME,
                 aws_access_key_id=ACCESS_KEY,
                 aws_secret_access_key=ACCESS_SECRET)
        S3_CLIENT.upload_file(FILE_NAME, BUCKET_NAME, OBJECT_NAME)
        print("File uploaded successfully")
    except Exception as e:
        print(f"Error occurred: {e}")    
        
get_new_release()

