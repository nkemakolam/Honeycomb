import os
import random
from flask import Flask, render_template

app = Flask(__name__)

# Path to media directory
MEDIA_FOLDER = os.path.join(app.static_folder, 'media')

# Allowed file extensions
ALLOWED_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.mp4', '.avi'}

def get_media_files():
    """Retrieve all media files from the media folder."""
    files = []
    for filename in os.listdir(MEDIA_FOLDER):
        if os.path.splitext(filename)[1].lower() in ALLOWED_EXTENSIONS:
            files.append(filename)
    return files

@app.route('/')
def slideshow():
    # Get all media files and shuffle them
    media_files = get_media_files()
    random.shuffle(media_files)
    return render_template('slideshow.html', media_files=media_files)

if __name__ == '__main__':
    app.run(host='local', port=5000)

