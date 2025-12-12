
import base64
import requests
from dotenv import load_dotenv
import os

load_dotenv('.env')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
#    acreating a tocken function

def access_token():
    try:
       # combining client id and client secret
        credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
       # encoding the credentials to base64
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        response=requests.post(
          'https://accounts.spotify.com/api/token',
           headers={"Authorization":f"Basic {encoded_credentials}"},
           data={"grant_type":"client_credentials"})
        # print(response.json())
        # print(response.json()['access_token'])

        print("Token generated successfully")
        return response.json()['access_token']
    except Exception as e:
        print("Failed to generate token:", e)
print(access_token())        



# latest release date: 2024-06-01

def get_new_release():
    try:      
       token = access_token()
       header = {"Authorization": f"Bearer {token}"}
       param = {'limit':50}
       response = requests.get('https://api.spotify.com/v1/browse/new-releases', headers=header,params=param) 

       if response.status_code == 200:
        #   print(response.json())
        data=response.json()
        release=[]
        albums=data['albums']['items']
        for i in albums:
           a={
              'album_name':i['name'],
              'release_date':i['release_date'],
           }
           print(a)
    except Exception as e:
        print("Failed to get new releases:", e)  

get_new_release()