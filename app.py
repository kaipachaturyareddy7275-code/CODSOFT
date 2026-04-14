from flask import Flask, render_template, request
import os
from model import generate_caption
from gtts import gTTS

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    caption = None
    image_path = None
    audio_path = None

    if request.method == "POST":

        # IMAGE
        if "image" in request.files and request.files["image"].filename != "":
            file = request.files["image"]
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)

            try:
                caption = generate_caption(filepath)
            except Exception as e:
                print("ERROR:", e)
                caption = "Could not generate caption"

            image_path = filepath

        # 🔊 Voice
        if caption:
            try:
                tts = gTTS(text=caption, lang="en")
                audio_path = "static/output.mp3"
                tts.save(audio_path)
            except:
                audio_path = None

    return render_template(
        "index.html",
        caption=caption,
        image_path=image_path,
        audio_path=audio_path
    )

if __name__ == "__main__":
    app.run(debug=True)