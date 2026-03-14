"""
DEHA — Flask Backend
====================
Receives base64 frames from session.html via WebSocket,
runs MediaPipe pose detection + angle checks,
streams feedback back to the browser in real time.
"""

import base64
import math

import cv2
import mediapipe as mp
import numpy as np
from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_socketio import SocketIO, emit

app = Flask(__name__, static_folder=".", static_url_path="")
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision

MODEL_PATH = "pose_landmarker_lite.task"

BaseOptions           = mp.tasks.BaseOptions
PoseLandmarker        = vision.PoseLandmarker
PoseLandmarkerOptions = vision.PoseLandmarkerOptions
VisionRunningMode     = vision.RunningMode

options = PoseLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=MODEL_PATH),
    running_mode=VisionRunningMode.IMAGE,
    num_poses=1,
    min_pose_detection_confidence=0.55,
    min_pose_presence_confidence=0.55,
    min_tracking_confidence=0.55,
)

landmarker = PoseLandmarker.create_from_options(options)

IDX = {
    "nose": 0,
    "l_shoulder": 11, "r_shoulder": 12,
    "l_elbow": 13,    "r_elbow": 14,
    "l_wrist": 15,    "r_wrist": 16,
    "l_hip": 23,      "r_hip": 24,
    "l_knee": 25,     "r_knee": 26,
    "l_ankle": 27,    "r_ankle": 28,
    "l_heel": 29,     "r_heel": 30,
    "l_foot": 31,     "r_foot": 32,
}

SKELETON_CONNECTIONS = [
    ("l_shoulder", "r_shoulder"),
    ("l_shoulder", "l_hip"),
    ("r_shoulder", "r_hip"),
    ("l_hip", "r_hip"),
    ("l_shoulder", "l_elbow"),
    ("l_elbow", "l_wrist"),
    ("r_shoulder", "r_elbow"),
    ("r_elbow", "r_wrist"),
    ("l_hip", "l_knee"),
    ("l_knee", "l_ankle"),
    ("l_ankle", "l_heel"),
    ("l_heel", "l_foot"),
    ("r_hip", "r_knee"),
    ("r_knee", "r_ankle"),
    ("r_ankle", "r_heel"),
    ("r_heel", "r_foot"),
]

POSES = {
    "mountain": {
        "name": "Palm Tree Pose", "sanskrit": "Tadasana", "level": "Beginner",
        "checks": [
            {"points": ("l_shoulder", "l_hip", "l_knee"),  "range": (165, 195), "label": "Left hip alignment",  "fix": "Straighten left side — hip is not neutral"},
            {"points": ("r_shoulder", "r_hip", "r_knee"),  "range": (165, 195), "label": "Right hip alignment", "fix": "Straighten right side — hip is not neutral"},
            {"points": ("l_hip", "l_knee", "l_ankle"),     "range": (165, 195), "label": "Left knee",           "fix": "Straighten the left knee fully"},
            {"points": ("r_hip", "r_knee", "r_ankle"),     "range": (165, 195), "label": "Right knee",          "fix": "Straighten the right knee fully"},
            {"points": ("l_elbow", "l_shoulder", "l_hip"), "range": (150, 210), "label": "Left arm",            "fix": "Relax left arm straight alongside the body"},
            {"points": ("r_elbow", "r_shoulder", "r_hip"), "range": (150, 210), "label": "Right arm",           "fix": "Relax right arm straight alongside the body"},
        ],
    },
    "warrior1": {
        "name": "Warrior I", "sanskrit": "Virabhadrasana I", "level": "Beginner",
        "checks": [
            {"points": ("l_hip", "l_knee", "l_ankle"),     "range": (75, 105),  "label": "Front knee bend", "fix": "Bend front knee to 90 degrees over the ankle"},
            {"points": ("r_hip", "r_knee", "r_ankle"),     "range": (155, 185), "label": "Back leg",        "fix": "Straighten the back leg fully"},
            {"points": ("l_elbow", "l_shoulder", "l_hip"), "range": (155, 210), "label": "Left arm raise",  "fix": "Raise the left arm straight overhead"},
            {"points": ("r_elbow", "r_shoulder", "r_hip"), "range": (155, 210), "label": "Right arm raise", "fix": "Raise the right arm straight overhead"},
            {"points": ("l_shoulder", "l_hip", "l_knee"),  "range": (155, 195), "label": "Torso upright",   "fix": "Keep torso upright — do not lean forward"},
        ],
    },
    "warrior2": {
        "name": "Warrior II", "sanskrit": "Virabhadrasana II", "level": "Beginner",
        "checks": [
            {"points": ("l_hip", "l_knee", "l_ankle"),          "range": (75, 105),  "label": "Front knee",          "fix": "Bend front knee to 90 degrees — track over second toe"},
            {"points": ("r_hip", "r_knee", "r_ankle"),          "range": (155, 185), "label": "Back leg",            "fix": "Straighten the back leg completely"},
            {"points": ("l_elbow", "l_shoulder", "r_shoulder"), "range": (155, 205), "label": "Left arm extension",  "fix": "Extend left arm fully parallel to the floor"},
            {"points": ("r_elbow", "r_shoulder", "l_shoulder"), "range": (155, 205), "label": "Right arm extension", "fix": "Extend right arm fully parallel to the floor"},
        ],
    },
    "tree": {
        "name": "Tree Pose", "sanskrit": "Vrksasana", "level": "Beginner",
        "checks": [
            {"points": ("l_hip", "l_knee", "l_ankle"),     "range": (155, 185), "label": "Standing leg", "fix": "Straighten the standing leg fully"},
            {"points": ("r_hip", "r_knee", "r_ankle"),     "range": (30, 90),   "label": "Raised leg",   "fix": "Bend raised knee outward and press foot to thigh"},
            {"points": ("l_elbow", "l_shoulder", "l_hip"), "range": (155, 210), "label": "Left arm",     "fix": "Raise left arm overhead — reach through fingertips"},
            {"points": ("r_elbow", "r_shoulder", "r_hip"), "range": (155, 210), "label": "Right arm",    "fix": "Raise right arm overhead — reach through fingertips"},
        ],
    },
    "triangle": {
        "name": "Triangle Pose", "sanskrit": "Trikonasana", "level": "Beginner",
        "checks": [
            {"points": ("l_hip", "l_knee", "l_ankle"),          "range": (160, 185), "label": "Front leg straight", "fix": "Keep front leg straight — do not bend the knee"},
            {"points": ("r_hip", "r_knee", "r_ankle"),          "range": (160, 185), "label": "Back leg straight",  "fix": "Straighten the back leg fully"},
            {"points": ("l_elbow", "l_shoulder", "r_shoulder"), "range": (150, 210), "label": "Top arm reach",      "fix": "Extend top arm straight up toward the ceiling"},
            {"points": ("r_elbow", "r_shoulder", "l_shoulder"), "range": (150, 210), "label": "Bottom arm reach",   "fix": "Reach bottom arm down toward the shin or floor"},
            {"points": ("l_shoulder", "l_hip", "l_knee"),       "range": (120, 160), "label": "Lateral bend",       "fix": "Deepen the side bend — hinge more from the hip"},
        ],
    },
    "eagle": {
        "name": "Eagle Pose", "sanskrit": "Garudasana", "level": "Intermediate",
        "checks": [
            {"points": ("l_hip", "l_knee", "l_ankle"),     "range": (120, 155), "label": "Standing leg bend", "fix": "Bend standing knee deeper — sink into the pose"},
            {"points": ("r_hip", "r_knee", "r_ankle"),     "range": (30, 80),   "label": "Wrapped leg",       "fix": "Hook raised foot behind the standing calf"},
            {"points": ("l_elbow", "l_shoulder", "l_hip"), "range": (60, 100),  "label": "Arms wrapped",      "fix": "Wrap arms tightly — lift elbows to shoulder height"},
            {"points": ("r_elbow", "r_shoulder", "r_hip"), "range": (60, 100),  "label": "Elbow height",      "fix": "Keep both elbows lifted level with the shoulders"},
        ],
    },
    "child": {
        "name": "Child's Pose", "sanskrit": "Balasana", "level": "Beginner",
        "checks": [
            {"points": ("l_shoulder", "l_hip", "l_knee"),  "range": (20, 65),   "label": "Torso fold",       "fix": "Fold torso fully forward — bring chest toward thighs"},
            {"points": ("r_shoulder", "r_hip", "r_knee"),  "range": (20, 65),   "label": "Torso fold right", "fix": "Fold torso fully forward — relax the lower back"},
            {"points": ("l_hip", "l_knee", "l_ankle"),     "range": (20, 60),   "label": "Left knee bend",   "fix": "Sit hips back toward heels — deepen the knee bend"},
            {"points": ("r_hip", "r_knee", "r_ankle"),     "range": (20, 60),   "label": "Right knee bend",  "fix": "Sit hips back toward heels — deepen the knee bend"},
            {"points": ("l_elbow", "l_shoulder", "l_hip"), "range": (140, 200), "label": "Arms extended",    "fix": "Reach arms fully forward — lengthen through fingertips"},
        ],
    },
    "lotus": {
        "name": "Lotus Pose", "sanskrit": "Padmasana", "level": "Intermediate",
        "checks": [
            {"points": ("l_shoulder", "l_hip", "l_knee"),  "range": (75, 115), "label": "Seated upright",  "fix": "Sit tall — lengthen the spine upward"},
            {"points": ("r_shoulder", "r_hip", "r_knee"),  "range": (75, 115), "label": "Posture right",   "fix": "Keep the torso upright — open the chest"},
            {"points": ("l_hip", "l_knee", "l_ankle"),     "range": (25, 65),  "label": "Left leg cross",  "fix": "Place left foot on right thigh — rotate knee outward"},
            {"points": ("r_hip", "r_knee", "r_ankle"),     "range": (25, 65),  "label": "Right leg cross", "fix": "Place right foot on left thigh — open the hip"},
        ],
    },
    "seated": {
        "name": "Seated Forward Fold", "sanskrit": "Paschimottanasana", "level": "Beginner",
        "checks": [
            {"points": ("l_shoulder", "l_hip", "l_knee"),  "range": (30, 80),   "label": "Forward fold depth", "fix": "Hinge deeper from hips — lengthen the spine first"},
            {"points": ("r_shoulder", "r_hip", "r_knee"),  "range": (30, 80),   "label": "Torso over legs",    "fix": "Fold torso forward — keep back as flat as possible"},
            {"points": ("l_hip", "l_knee", "l_ankle"),     "range": (160, 185), "label": "Left leg straight",  "fix": "Keep both legs straight — flex feet toward you"},
            {"points": ("r_hip", "r_knee", "r_ankle"),     "range": (160, 185), "label": "Right leg straight", "fix": "Keep both legs straight — do not lock knees hard"},
            {"points": ("l_elbow", "l_shoulder", "l_hip"), "range": (130, 200), "label": "Arms reach",         "fix": "Reach hands toward feet — hold shins ankles or feet"},
        ],
    },
    "dancer": {
        "name": "Dancer's Pose", "sanskrit": "Natarajasana", "level": "Intermediate",
        "checks": [
            {"points": ("l_hip", "l_knee", "l_ankle"),     "range": (155, 185), "label": "Standing leg",      "fix": "Keep the standing leg straight and grounded"},
            {"points": ("r_hip", "r_knee", "r_ankle"),     "range": (55, 100),  "label": "Raised leg bend",   "fix": "Bend the raised leg — kick foot into your hand"},
            {"points": ("r_shoulder", "r_hip", "r_knee"),  "range": (120, 165), "label": "Backbend lift",     "fix": "Lift the raised leg higher — open through the chest"},
            {"points": ("l_elbow", "l_shoulder", "l_hip"), "range": (140, 200), "label": "Reach arm forward", "fix": "Extend the free arm straight forward for balance"},
        ],
    },
}


def calc_angle(a, b, c):
    ax, ay = a[0] - b[0], a[1] - b[1]
    cx, cy = c[0] - b[0], c[1] - b[1]
    dot    = ax * cx + ay * cy
    mag_a  = math.hypot(ax, ay)
    mag_c  = math.hypot(cx, cy)
    if mag_a * mag_c == 0:
        return 0.0
    cosine = max(-1.0, min(1.0, dot / (mag_a * mag_c)))
    return math.degrees(math.acos(cosine))


def get_pt(landmarks, name, w, h):
    lm = landmarks[IDX[name]]
    return (lm.x * w, lm.y * h)


def build_joint_status(landmarks, pose_key, w, h):
    checks       = POSES[pose_key]["checks"]
    joint_status = {}
    feedback     = []
    passed       = 0

    for check in checks:
        a_name, b_name, c_name = check["points"]
        a     = get_pt(landmarks, a_name, w, h)
        b     = get_pt(landmarks, b_name, w, h)
        c     = get_pt(landmarks, c_name, w, h)
        angle = calc_angle(a, b, c)
        lo, hi = check["range"]
        ok     = lo <= angle <= hi

        if ok:
            passed += 1
        else:
            feedback.append(check["fix"])

        for name in (a_name, b_name, c_name):
            joint_status[name] = joint_status.get(name, True) and ok

    score = int((passed / len(checks)) * 100) if checks else 100
    return joint_status, feedback, score


@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(".", path)


@socketio.on("frame")
def handle_frame(data):
    pose_key = data.get("pose", "mountain")
    if pose_key not in POSES:
        pose_key = "mountain"

    try:
        b64 = data["frame"].split(",")[-1]
        img_bytes = base64.b64decode(b64)
        np_arr    = np.frombuffer(img_bytes, np.uint8)
        frame     = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        if frame is None:
            raise ValueError("Failed to decode image")
    except Exception as e:
        emit("feedback", {"error": str(e)})
        return

    H, W = frame.shape[:2]

    rgb    = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_img = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
    result = landmarker.detect(mp_img)

    if not result.pose_landmarks or len(result.pose_landmarks) == 0:
        emit("feedback", {
            "score":        0,
            "feedback":     ["Move into frame — body not detected"],
            "landmarks":    [],
            "joint_status": {},
            "detected":     False,
        })
        return

    landmarks    = result.pose_landmarks[0]
    joint_status, feedback, score = build_joint_status(landmarks, pose_key, W, H)

    lm_list = [{"x": lm.x, "y": lm.y, "z": lm.z} for lm in landmarks]

    emit("feedback", {
        "score":        score,
        "feedback":     feedback if feedback else [],
        "landmarks":    lm_list,
        "joint_status": joint_status,
        "detected":     True,
        "connections":  SKELETON_CONNECTIONS,
    })


if __name__ == "__main__":
    print("\n  Deha Flask server starting...")
    print("  Open http://localhost:5000 in your browser\n")
    socketio.run(app, host="0.0.0.0", port=5000, debug=False)