# from flask import Flask, render_template, redirect, url_for
import requests
import json
from dotenv import load_dotenv
import os
import base64

# app = Flask(__name__)

load_dotenv()

auth_url = 'https://accounts.spotify.com/authorize'

track_url = 'https://api.spotify.com/v1/tracks/'
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

def get_token():

    auth_string = client_id + ':' + client_secret
    auth_bytes = auth_string.encode('UTF-8')
    auth_base64 = str(base64.b64encode(auth_bytes), 'UTF-8')

    token_url = 'https://accounts.spotify.com/api/token'

    headers = {
        'Authorization': 'Basic ' + auth_base64,
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {'grant_type':'client_credentials'}
    result = requests.post(token_url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result['access_token']
    return token


def get_auth_header(token):
    return {'Authorization': 'Bearer ' + token}


def search_artist(token, artist_name):
    url = 'http://api.spotify.com/v1/search' 
    headers = get_auth_header(token)
    query = f'?q={artist_name}&type=artist&limit=1'

    query_url = url + query
    result = requests.get(query_url, headers=headers)
    json_result = json.loads(result.content)['artists']['items']
    return json_result[0]['id']

def artist(token, artist_id):
    url = 'https://api.spotify.com/v1/artists'
    headers = get_auth_header(token)
    query = f'/{artist_id}'

    query_url = url + query
    result = requests.get(query_url, headers=headers)
    json_result = json.loads(result.content)
    return json_result['name']

def get_album_name(token, artist_id):
    url = 'https://api.spotify.com/v1/artists'
    headers = get_auth_header(token)
    query = f'/{artist_id}/albums'

    query_url = url + query
    result = requests.get(query_url, headers=headers)
    json_results = json.loads(result.content)['items']

    albums_names = []

    for i in range(len(json_results)):
        
        rs = json_results[i]
        albums_names.append(rs['name'])

    return albums_names

def get_album_image(token, artist_id):
    url = 'https://api.spotify.com/v1/artists'
    headers = get_auth_header(token)
    query = f'/{artist_id}/albums'

    query_url = url + query
    result = requests.get(query_url, headers=headers)
    json_results = json.loads(result.content)['items']

    albums_image = []

    for i in range(len(json_results)):
        
        rs = json_results[i]
        albums_image.append(rs['images'])

    return albums_image

token = get_token()

# name = input("Enter Name: ")

artist_id = search_artist(token, 'Taylor Swift')


album_name = get_album_name(token, artist_id)
album_image = get_album_image(token, artist_id)

# for album in range(len(album_name)):
#     album_img = album_image[album][0]
#     print(f'{album_name[album]} {album_img}')
#     print()


# app.route('/')
# def index():
#     album_name = get_album_name(token, artist_id)
#     album_image = get_album_image(token, artist_id)

#     return render_template('index.html', album_name=album_name, album_image=album_image)



# if __name__ == '__main__':
#     app.run(debug=True)
