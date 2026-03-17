# This is the example schedule_meeting function from the Google Gemini page that I have wrapped with Flask for use with Postman

from flask import Flask, request, jsonify
from meeting import schedule_meeting

app = Flask(__name__)

meetings = {}

# PUT
@app.route("/meetings", methods=["PUT"])
def update_meeting():
    data = request.json
    meeting_id = data.get("id")
    if not meeting_id or meeting_id not in meetings:
        return jsonify({"error": "Meeting not found"}), 404

    meeting = schedule_meeting(
        attendees=data["attendees"],
        date=data["date"],
        time=data["time"],
        topic=data["topic"]
    )
    meetings[meeting_id] = meeting
    return jsonify({"id": meeting_id, "meeting": meeting})

# PATCH
@app.route("/meetings", methods=["PATCH"])
def patch_meeting():
    data = request.json
    meeting_id = data.get("id")
    if not meeting_id or meeting_id not in meetings:
        return jsonify({"error": "Meeting not found"}), 404

    meeting = meetings[meeting_id]
    for key in ["attendees", "date", "time", "topic"]:
        if key in data:
            meeting[key] = data[key]

    meetings[meeting_id] = meeting
    return jsonify({"id": meeting_id, "meeting": meeting})

# DELETE
@app.route("/meetings", methods=["DELETE"])
def delete_meeting():
    data = request.json
    meeting_id = data.get("id")
    if not meeting_id or meeting_id not in meetings:
        return jsonify({"error": "Meeting not found"}), 404

    deleted = meetings.pop(meeting_id)
    return jsonify({"id": meeting_id, "deleted_meeting": deleted})

# Creating a test POST route
meetings["1"] = {
    "attendees": ["Alice", "Bob"],
    "date": "2026-03-20",
    "time": "10:00",
    "topic": "Project kickoff"
}

if __name__ == "__main__":
    app.run(debug=True)