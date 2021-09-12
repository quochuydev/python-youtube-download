from pytube import YouTube
from flask import Flask, request, jsonify, redirect, send_file, send_from_directory
from flask_cors import CORS, cross_origin
from slugify import slugify

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/getInfo", methods=['POST'])
@cross_origin()
def getInfo():
	link = request.json['url']
	yt = YouTube(link)
	my_stream = yt.streams.filter(file_extension="mp4", mime_type="video/mp4", progressive=True)

	tags = []
	for stream in my_stream:
		print(f"tags: {stream.itag} resolution: {stream.resolution}")
		tags.append({ "id": stream.itag, "itag": stream.itag, "resolution": stream.resolution })

	return jsonify(tags)

@app.route("/download", methods=['POST'])
@cross_origin()
def download():
	link = request.json['url']
	itag = request.json['itag']

	yt = YouTube(link)
	video = yt.streams.get_by_itag(itag)

	filename = slugify(yt.title) + '-{itag}' + '.mp4'
	filename = filename.format(itag=itag)
	
	result = video.download(filename=filename)
	print(result)
	return 'http://localhost:5000/files/' + filename

@app.route('/files/<path:filename>')
def downloadFile(filename):
	path = "./" + filename
	return send_from_directory(directory='', path=path, as_attachment=True)