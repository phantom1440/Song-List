from flask import Flask, render_template, url_for, request, flash, redirect
import sqlite3
from werkzeug.utils import secure_filename
import os 
import urllib
from song_api import get_token, search_artist, get_album_name, get_album_image, artist

con = sqlite3.connect('songs.sqlite',  check_same_thread=False)
cursor = con.cursor()

app = Flask(__name__)

app.config['SECRET_KEY'] = '2134wedfqerq2rPP:)(())'
image_path = 'static/images'
app.config['UPLOAD_FOLDER'] = image_path

@app.route('/')
def home():
    return redirect(url_for('songs'))

@app.route('/add_song', methods=['GET', 'POST'])
def add_song():

    if request.method == 'POST':
        title = request.form['title']
        artist = request.form['artist']
        photo = request.files['photo']

        filename = secure_filename(photo.filename)
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        query = "INSERT INTO songs(title, artist, photo) VALUES(?,?,?)"

        cursor.execute(query, (title, artist, filename))
        con.commit()
        
        return redirect(url_for('songs'))

    return render_template('add.html')

@app.route('/songs', methods=['GET'])
def songs():

    if request.method == 'GET':
        query = "SELECT * FROM songs"
        cursor.execute(query)
        songs = cursor.fetchall()

    return render_template('songs.html', songs=songs)

    # token = get_token()

    # artist_id = search_artist(token, 'Taylor Swift')

    # album_name = get_album_name(token, artist_id)
    # album_image = get_album_image(token, artist_id)
    # artist_name = artist(token,artist_id)

    # return render_template('songs.html', album_name=album_name, album_image=album_image, artist_name=artist_name, artist_id=artist_name)


@app.route('/delete/<int:ids>', methods=['GET', 'POST'])
def delete(ids):

    query = "DELETE FROM songs WHERE id = ?"
    cursor.execute(query, (ids,))
    con.commit()
    return redirect(url_for('songs'))

@app.route('/update/<int:ids>', methods=['GET', 'POST'])
def update(ids):
    
    query = "SELECT * FROM songs WHERE id = ?"
    cursor.execute(query, (ids,))

    results = cursor.fetchall()

    for result in results:
        return render_template('update.html', idd=result[0], title=result[1], artist=result[2], photo=result[3])

@app.route('/update/edit', methods=['GET', 'POST'])
def edit():

    if request.method == 'POST':
        title = request.form['title']
        artist = request.form['artist']
        ids = request.form['idd']

        query = "UPDATE songs SET title=?, artist=? WHERE id=?"

        cursor.execute(query, (title, artist, ids))
        con.commit()

        return redirect(url_for('songs'))

@app.route('/search', methods=['GET', 'POST'])
def search():

    if request.method == 'POST':

        search = request.form['search']
        searched = '%' + search + '%'

        if search == 'return':
            return redirect(url_for('songs'))
        
        else:
            query = "SELECT * FROM songs WHERE title LIKE ? OR artist LIKE ?"
            cursor.execute(query, (searched, searched))
            songs = cursor.fetchall()

            if songs:
                return render_template('songs.html', songs=songs)
            else:
                flash("No songs found")
                return redirect(url_for('songs'))
        
if __name__ == '__main__':
    app.run(debug=True)