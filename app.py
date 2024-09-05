from flask import Flask,request,jsonify
from flask_cors import CORS
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
from YoutubeTags import videotags,videotitle

app=Flask(__name__)

CORS(app)
def extract_video_id(youtube_url):
    """
    Extracts the video ID from a given YouTube URL.
    """
    query = urlparse(youtube_url)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    elif query.hostname in {'www.youtube.com', 'youtube.com', 'm.youtube.com'}:
        if query.path == '/watch':
            return parse_qs(query.query)['v'][0]
        elif query.path[:7] == '/embed/':
            return query.path.split('/')[2]
        elif query.path[:3] == '/v/':
            return query.path.split('/')[2]
    return None
@app.route("/")
def Home():
    return jsonify({"Message":"Welcome To Api","Success":True})

@app.route('/transcript',methods=['GET'])
def  get_transcript():
    video_url=request.args.get('url')
    language=request.args.get("ln")
    video_id = extract_video_id(video_url)
    # print(video_id)
    print(video_url)
    if video_id is None:
        return jsonify({"Message":"Invalid URL","Success":False})
    try:
        tagsOfVideo=videotags(video_url)
        titleOfVideo=videotitle(video_url)
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_data = ""
        for entry in transcript:
            transcript_data+=entry['text']+" "
        step=503
        length=len(transcript_data)
        zero=0
        print(len(transcript_data))
        finalTranscriptData=[]
        cnt=0
        transcriptStr=""
        transcript_data=transcript_data.replace('\n',' ')
        return jsonify([{"title":titleOfVideo,"tags":tagsOfVideo},{'transcriptText':transcript_data}]), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from youtube_transcript_api import YouTubeTranscriptApi
# from youtube_transcript_api.formatters import JSONFormatter
# from urllib.parse import urlparse, parse_qs

# app = Flask(__name__)
# CORS(app)

# def extract_video_id(youtube_url):
#     query = urlparse(youtube_url)
#     if query.hostname == 'youtu.be':
#         return query.path[1:]
#     elif query.hostname in {'www.youtube.com', 'youtube.com', 'm.youtube.com'}:
#         if query.path == '/watch':
#             return parse_qs(query.query)['v'][0]
#         elif query.path[:7] == '/embed/':
#             return query.path.split('/')[2]
#         elif query.path[:3] == '/v/':
#             return query.path.split('/')[2]
#     return None

# @app.route('/')
# def home():
#     return jsonify({"Message": "Welcome To Api", "Success": True})

# @app.route('/transcript', methods=['GET'])
# def get_transcript():
#     video_url = request.args.get('url')
#     requested_language = request.args.get('ln', 'en')  # Default to 'en' if not specified
#     video_id = extract_video_id(video_url)
    
#     if video_id is None:
#         return jsonify({"Message": "Invalid URL", "Success": False})

#     try:
#         # Fetch available languages for the video
#         transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
#         available_languages = [transcript.language_code for transcript in transcript_list]
        
#         # Try to get the transcript in the requested language first
#         if requested_language not in available_languages:
#             # Fall back to the first available language if the requested one is not available
#             requested_language = available_languages[0] if available_languages else 'en'
        
#         # Fetch the transcript in the determined language
#         transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[requested_language])
        
#         # Format the transcript text
#         formatted_transcript = []
#         for entry in transcript:
#             start_time = entry['start']
#             end_time = start_time + entry['duration']
#             formatted_transcript.append({
#                 'start_time': start_time,
#                 'end_time': end_time,
#                 'text': entry['text']
#             })
        
#         return jsonify({
#             'transcript': formatted_transcript,
#             'language': requested_language,
#             'availableLanguages': available_languages
#         }), 200

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=True)
