import os
import random
from flask import Flask, render_template
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
app = Flask(__name__)



# Load environment variables from the .env file
load_dotenv()

# Fetch Azure Storage connection settings from environment variables
AZURE_CONNECTION_STRING = os.getenv('AZURE_CONNECTION_STRING')
CONTAINER_NAME = os.getenv('CONTAINER_NAME')

print(CONTAINER_NAME)

# Check if environment variables are defined
if not AZURE_CONNECTION_STRING or not CONTAINER_NAME:
    raise ValueError("Azure connection string or container name not set in environment variables.")

# Initialize BlobServiceClient
blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
container_client = blob_service_client.get_container_client(CONTAINER_NAME)


# def get_files_list():
#     """Retrieve a list of images and videos from the Azure container."""
#     blob_list = container_client.list_blobs()
#     images = []
#     videos = []

#     # Separate files into images and videos
#     for blob in blob_list:
#         if blob.name.endswith(('.png', '.jpg', '.jpeg')):
#             images.append(blob.name)
#         elif blob.name.endswith(('.mp4', '.mov')):
#             videos.append(blob.name)

#     return images, videos

from azure.storage.blob import BlobServiceClient

def get_files_list():
    # Create a BlobServiceClient using your connection string
    blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
    container_client = blob_service_client.get_container_client(CONTAINER_NAME)

    images = []
    videos = []

    # List blobs in the container
    blob_list = container_client.list_blobs()

    for blob in blob_list:
        # Check the blob's content type to categorize files
        if blob.content_settings.content_type.startswith('image/'):
            images.append(blob.name)
        elif blob.content_settings.content_type.startswith('video/'):
            videos.append(blob.name)

    print("Files found:", images, videos)  # Debugging line to see found files
    return images, videos





@app.route('/')
def index():
    print(CONTAINER_NAME)
    print("Index route is being accessed")  # Debugging line to check if the route is hit
    images, videos = get_files_list()



      # Check if images or videos were found
    print("Images found:", images)
    print("Videos found:", videos)

    # Select random image and video
    random_image = random.choice(images) if images else None
    random_video = random.choice(videos) if videos else None

    image_url = f"https://{blob_service_client.account_name}.blob.core.windows.net/{CONTAINER_NAME}/{random_image}" if random_image else None
    video_url = f"https://{blob_service_client.account_name}.blob.core.windows.net/{CONTAINER_NAME}/{random_video}" if random_video else None
      # Debugging: Print the image URL to the console
    print(image_url)  # Add this line to check the URL

    return render_template('index5.html', image_url=image_url, video_url=video_url)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
