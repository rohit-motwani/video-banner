from flask import Flask, render_template, request, redirect, url_for, send_file
import os
from moviepy.editor import VideoFileClip, CompositeVideoClip, ImageClip

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/create_banner')
def create_banner():
    return render_template('create_banner.html')

@app.route('/add_banner_to_video')
def add_banner_to_video():
    return render_template('add_banner_to_video.html')

@app.route('/submit_banner', methods=['POST'])
def submit_banner():
    phone_number = request.form['phone_number']
    address = request.form['address']
    city = request.form['city']

    # Redirect to show_details and pass user-entered details as query parameters
    return redirect(url_for('show_details', phone_number=phone_number, address=address, city=city))

@app.route('/submit_video', methods=['POST'])
def submit_video():
    video_file = request.files['video']
    banner_image = request.files['banner_image']
    
    video_file_path = os.path.join('uploads', video_file.filename)
    banner_image_path = os.path.join('uploads', banner_image.filename)
    output_file_path = os.path.join('uploads', 'video_with_banner.mp4')

    video_file.save(video_file_path)
    banner_image.save(banner_image_path)

    add_banner(video_file_path, banner_image_path, output_file_path)

    return send_file(output_file_path, as_attachment=True)

@app.route('/details')
def show_details():
    phone_number = request.args.get('phone_number')
    address = request.args.get('address')
    city = request.args.get('city')

    # Render bhatias_mobile.html with user-entered details
    return render_template('bhatia_mobile.html', phone_number=phone_number, address=address, city=city)

def add_banner(video_file, banner_image, output_file):
    # Load video clip
    video = VideoFileClip(video_file)

    # Load banner image
    banner = ImageClip(banner_image)

    # Resize banner image to fit the width of the video (or to fit proportionally)
    banner = banner.resize(width=video.size[0] // 2)

    # Set the duration of the banner to match the video's duration
    banner = banner.set_duration(video.duration)

    # Calculate position for the banner at the middle bottom
    banner_position = (
        (video.size[0] - banner.size[0]) // 2,  # Center horizontally
        video.size[1] - banner.size[1] - 20  # 20 pixels up from the bottom
    )

    # Set the position of the banner
    banner = banner.set_position(banner_position)

    # Ensure the original video dimensions are kept intact by setting the size
    video = video.resize(video.size)

    # Composite the video and the banner together
    video_with_banner = CompositeVideoClip([video, banner])

    # Write the video to a file
    video_with_banner.write_videofile(output_file, codec='libx264', fps=video.fps, preset='ultrafast')

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    app.run(debug=True)
