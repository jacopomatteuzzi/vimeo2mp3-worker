from flask import Flask, request, jsonify, send_file
import yt_dlp
import os

app = Flask(__name__)

@app.route('/vimeo2mp3', methods=['POST'])
def vimeo2mp3():
    data = request.json
    url = data.get('url')
    if not url:
        return jsonify({'error': 'Missing url'}), 400

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '/tmp/%(id)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = f"/tmp/{info['id']}.mp3"
            if os.path.exists(filename):
                return send_file(filename, mimetype='audio/mpeg', as_attachment=True, download_name=f"{info['id']}.mp3")
            else:
                return jsonify({'error': 'File not found'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080) 