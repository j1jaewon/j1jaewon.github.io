import os
import uuid
from flask import Flask, request, render_template, jsonify
from checker import verify

app = Flask(__name__)
UPLOAD_DIR = "/tmp/attendance_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/verify", methods=["POST"])
def run_verify():
    tag_file = request.files.get("tag_file")
    attendance_file = request.files.get("attendance_file")

    if not tag_file or not attendance_file:
        return jsonify({"error": "두 파일 모두 업로드해주세요."}), 400

    uid = uuid.uuid4().hex
    tag_path = os.path.join(UPLOAD_DIR, f"{uid}_tag.xls")
    att_path = os.path.join(UPLOAD_DIR, f"{uid}_att.xls")
    tag_file.save(tag_path)
    attendance_file.save(att_path)

    try:
        results = verify(tag_path, att_path)
        return jsonify({"results": results})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        for p in [tag_path, att_path]:
            try:
                os.remove(p)
            except Exception:
                pass


if __name__ == "__main__":
    app.run(debug=True, port=5050)
