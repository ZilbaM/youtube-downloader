from flask import Flask, request, render_template, flash, redirect, url_for
from pytube import YouTube, Playlist
import ffmpeg
import os

app = Flask(__name__)
app.config['STATIC_FOLDER'] = 'static'
app.secret_key = 'my_secret_key'

def download(yt: YouTube):
    stream = yt.streams.filter(only_audio=True).first()
    stream.download(ouput_path='downloads')
    audio_file = stream.default_filename
    wav_file = audio_file.replace('.mp4', '.wav')
    ffmpeg.input(f'downloads/{audio_file}').output(f'downloads/{wav_file}').run()
    os.remove(f'downloads/{audio_file}')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        youtube_url = request.form['youtube_url']
        yt = YouTube(youtube_url)
        download(yt)
        flash('Audio downloaded and converted to WAV!')
        return redirect(url_for('index'))
    return render_template('./index.html')

@app.route('/playlist', methods=['GET', 'POST'])
def playlist():
    if request.method == 'POST':
        youtube_url = request.form['youtube_url']
        playlist = Playlist(youtube_url)
        for video in playlist.videos:
            yt = YouTube(video.watch_url)
            download(yt)
        flash('All audio files in the playlist downloaded and converted to WAV!')
        return redirect(url_for('playlist'))
    return render_template('./playlist.html')

if __name__ == '__main__':
    app.run(debug=True)