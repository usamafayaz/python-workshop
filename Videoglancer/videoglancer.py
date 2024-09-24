import base64
import os
import re
import shutil


from flask import Flask, request, jsonify, send_file
import cv2
from pytubefix import YouTube
from fpdf import FPDF
from PIL import Image
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/convert_in_pdf": {"origins": "*"}})

def sanitize_filename(file_name):
    return re.sub(r'[<>:"/\\|?*]', '_', file_name)

def extract_frames(video_path, output_folder, minutes):
    video_capture = cv2.VideoCapture(video_path)
    frame_rate = int(video_capture.get(cv2.CAP_PROP_FPS))

    total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))

    frame_interval = int((frame_rate * 60) * int(minutes))

    if frame_interval == 0:
        frame_interval = 1

    for i in range(0, total_frames, frame_interval):
        video_capture.set(cv2.CAP_PROP_POS_FRAMES, i)
        success, image = video_capture.read()

        if success:
            frame_path = os.path.join(output_folder, f'frame_{i}.jpg')
            cv2.imwrite(frame_path, image)
    video_capture.release()


def create_pdf_from_frames(output_folder):
    pdf = FPDF(format='A4')

    for root, _, files in os.walk(output_folder):
        image_files = [file for file in files if file.endswith('.jpg')]
        image_files.sort()

        for image_file in image_files:
            image_path = os.path.join(root, image_file)

            with Image.open(image_path) as img:
                img_width, img_height = img.size

            pdf_width, pdf_height = pdf.w, pdf.h
            scale = min(pdf_width / img_width, pdf_height / img_height)
            new_width = img_width * scale
            new_height = img_height * scale

            center_x = (pdf_width - new_width) / 2
            center_y = (pdf_height - new_height) / 2

            pdf.add_page()
            pdf.image(image_path, x=center_x, y=center_y, w=new_width, h=new_height)

    pdf_file_name = f'{output_folder}_frames.pdf'
    pdf.output(pdf_file_name)
    return pdf_file_name


@app.route('/convert_in_pdf', methods=['GET'])
def convert_in_pdf():
    youtube_url = request.args.get('youtube_url')
    minutes = "1"
    video_folder = None

    try:
        yt = YouTube(youtube_url)
        duration_seconds = yt.length
        if duration_seconds > 7200:  # 7200 seconds = 120 minutes
            return jsonify({'warning': 'The video is too long. Please select a shorter one.'})
        sanitized_video_id = sanitize_filename(yt.video_id)
        video_folder = f'video_{sanitized_video_id}'
        os.makedirs(video_folder, exist_ok=True)
        video = yt.streams.filter(progressive=True, file_extension='mp4', resolution='360p').first()
        if not video:
            video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        if video:
            video_extension = video.mime_type.split('/')[-1]
            video_file_name = f'video.{video_extension}'
            video.download(output_path=video_folder, filename=video_file_name)
        else:
            return jsonify({'message': 'No downloadable video found'})

        extract_frames(os.path.join(video_folder, video_file_name), video_folder, minutes)
        pdf_file = create_pdf_from_frames(video_folder)

        with open(pdf_file, "rb") as f:
            pdf_base64 = base64.b64encode(f.read()).decode('utf-8')

        os.remove(pdf_file)
        shutil.rmtree(video_folder)

        return jsonify({'pdf': pdf_base64})
    except Exception as e:
        shutil.rmtree(video_folder)
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=False)