from flask import Flask, request, jsonify
from PIL import Image
import requests
from io import BytesIO
import base64
from flask_cors import CORS
import instaloader
import json

# Initialize Instaloader
L = instaloader.Instaloader()

app = Flask(__name__)
CORS(app, resources={r"/image-to-base64": {"origins": "*"}, r"/profile-info": {"origins": "*"}})


@app.route('/image-to-base64', methods=['POST'])
def image_to_base64():
    data = request.json
    image_url = data.get('url')
    if not image_url:
        return jsonify({"error": "URL is required"}), 400
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        image = Image.open(BytesIO(response.content))
        buffered = BytesIO()
        image.save(buffered, format=image.format)
        img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
        img_data_url = f"data:image/{image.format.lower()};base64,{img_str}"
        return jsonify({"image_data_url": img_data_url})
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 400
    except IOError as e:
        return jsonify({"error": str(e)}), 500


def get_profile_info(username):
    try:
        profile = instaloader.Profile.from_username(L.context, username)
        print('Full Name:', profile.full_name)
        print('Number of Posts:', profile.mediacount)
        return {
            "username": profile.username,
            "full_name": profile.full_name,
            "followers": profile.followers,
            "following": profile.followees,
            "posts": profile.mediacount,
            "bio": profile.biography,
            "profile_pic_url": profile.profile_pic_url,
            "external_url": profile.external_url,
            "is_private": profile.is_private
        }
    except Exception as e:
        print(f"Error fetching profile for {username}: {str(e)}")
        return None


@app.route('/profile-info', methods=['GET'])
def profile_info():
    username = request.args.get('username')
    if not username:
        return jsonify({"error": "Username is required"}), 400

    profile_data = get_profile_info(username)
    if profile_data:
        return jsonify(profile_data)
    else:
        return jsonify({"error": "Failed to fetch profile information"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)