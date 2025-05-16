# from flask import Flask
# from flask_cors import CORS
# from routes.audio_routes import audio_bp
# from routes.video_routes import video_bp
# from routes.image_routes import image_bp
# from routes.writing_routes import writing_bp

# app = Flask(__name__)
# CORS(app)

# app.register_blueprint(audio_bp, url_prefix="/audio")
# app.register_blueprint(video_bp, url_prefix="/video")
# app.register_blueprint(image_bp, url_prefix="/image")
# app.register_blueprint(writing_bp, url_prefix="/writing")

# # if __name__ == '__main__':
# #     app.run(debug=True)
# if __name__ == "__main__":
#     app.run(debug=True, host="0.0.0.0", port=5001) 

from flask import Flask
from flask_cors import CORS
from routes.audio_routes import audio_bp
from routes.video_routes import video_bp
from routes.image_routes import image_bp
from routes.writing_routes import writing_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(audio_bp, url_prefix="/audio")
app.register_blueprint(video_bp, url_prefix="/video")
app.register_blueprint(image_bp, url_prefix="/image")
app.register_blueprint(writing_bp, url_prefix="/writing") # Register writing blueprint

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000) # Make sure port is 5001, and host is accessible