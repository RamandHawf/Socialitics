from flask import Flask, request, jsonify
from flask_cors import CORS
import instagrapi
import logging
import asyncio
app = Flask(__name__)
CORS(app)
# Configure logging
logging.basicConfig(filename='app.log', level=logging.DEBUG)
# Initialize the Instagrapi client
cl = instagrapi.Client()
def login_to_instagram():
    try:
        cl.login("architecturalmodelmaker_", "Liquid098@")
        logging.info("Logged in to Instagram account")
    except Exception as e:
        logging.error(f"Instagram login error: {str(e)}")
# Perform the Instagram login during app startup
login_to_instagram()
async def fetch_instagram_data(post_url,max_attempts=10):
    print("My name is khan")
    try:
        # Fetch Instagram media info
            # Fetch Instagram media info
            media_pk = cl.media_pk_from_url(post_url)
            meta_data = cl.insights_media(media_pk)
            media_info = cl.media_info(media_pk)
            # Extract relevant data
            comment_count = meta_data["comment_count"]
            likes_count = meta_data["like_count"]
            save_count = meta_data["save_count"]
            video_views = media_info.view_count
            media_type = meta_data["instagram_media_type"]
            if media_type == "IMAGE":
                return {
                    "media_id": media_info.id,
                    "Likes_count": likes_count,
                    "video_views": video_views,
                    "comments_count": comment_count,
                    "save_count": save_count,
                    "owner_username": media_info.user.username,
                    "media_type" : media_type
                }
            # Check if video_views is greater than 0
            if media_type == "VIDEO" :
                return {
                    "media_id": media_info.id,
                    "Likes_count": likes_count,
                    "video_views": video_views,
                    "comments_count": comment_count,
                    "save_count": save_count,
                    "owner_username": media_info.user.username,
                    "media_type" : media_type
                }
            # Increment the attempts counter
    except Exception as e:
        # Log the error
        logging.error(f"An error occurred: {str(e)}")
        return None
@app.route("/data", methods=["GET"])
async def get_instagram_data():
    try:
        post_url = request.args.get("post_url")
        # Log the request URL
        logging.info(f"Received request for post_url: {post_url}")
        # Fetch Instagram data asynchronously
        data = await fetch_instagram_data(post_url)
        print(data)
        if data:
            # Log success
            logging.info("Data retrieval successful")
            return jsonify(data)
        else:
            # Handle error gracefully
            return jsonify({"error": "Failed to fetch Instagram data"}), 500
    except Exception as e:
        # Log the error
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500
if __name__ == "__main__":
    app.run(port=9000, debug=True)