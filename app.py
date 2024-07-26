import instaloader
import os
from flask import Flask, render_template, request, send_from_directory

app = Flask(__name__)

def download_instagram_reel(url, output_path):
    if not url.endswith('/'):
        url += '/'

    L = instaloader.Instaloader(dirname_pattern=output_path, filename_pattern='{shortcode}')

    try:
        shortcode = url.split("/")[-2]
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        L.download_post(post, target=output_path)
        reel_file = os.path.join(output_path, f"{post.shortcode}.mp4")
        if os.path.exists(reel_file):
            return reel_file
        else:
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        output_directory = 'downloads'
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        reel_file = download_instagram_reel(url, output_directory)
        if reel_file:
            filename = os.path.basename(reel_file)
            return render_template('index.html', filename=filename)
        else:
            return render_template('index.html', error="Failed to download the Instagram reel.")
    return render_template('index.html')

@app.route('/downloads/<filename>')
def download_file(filename):
    return send_from_directory('downloads', filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 3000)))