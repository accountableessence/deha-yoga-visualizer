"""
DEHA — Real-Time Body Pose Tracker
====================================
Python 3.10.2 | MediaPipe Tasks API | OpenCV | NumPy

Place pose_landmarker_lite.task in the same folder as this script.

Controls:
  1  →  Mountain Pose
  2  →  Warrior I
  3  →  Warrior II
  4  →  Tree Pose
  5  →  Triangle Pose
  6  →  Eagle Pose
  7  →  Child's Pose
  8  →  Seated Forward Fold
  9  →  Lotus Pose
  0  →  Dancer's Pose
  D  →  Toggle debug angle display
  ESC → Quit
"""

import cv2
import mediapipe as mp
import numpy as np
import time
import math

# ─────────────────────────────────────────────────────────────────────────────
#  MEDIAPIPE TASKS SETUP
# ─────────────────────────────────────────────────────────────────────────────
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision

MODEL_PATH = "pose_landmarker_lite.task"

BaseOptions           = mp.tasks.BaseOptions
PoseLandmarker        = vision.PoseLandmarker
PoseLandmarkerOptions = vision.PoseLandmarkerOptions
VisionRunningMode     = vision.RunningMode

options = PoseLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=MODEL_PATH),
    running_mode=VisionRunningMode.VIDEO,
    num_poses=1,
    min_pose_detection_confidence=0.55,
    min_pose_presence_confidence=0.55,
    min_tracking_confidence=0.55,
)

# ─────────────────────────────────────────────────────────────────────────────
#  COLOUR PALETTE  (BGR for OpenCV)
# ─────────────────────────────────────────────────────────────────────────────
CLR_GREEN      = (80,  190, 100)
CLR_RED        = (60,   60, 210)
CLR_GOLD       = (30,  175, 212)
CLR_WHITE      = (235, 235, 235)
CLR_OFFWHITE   = (200, 195, 190)
CLR_PANEL      = (28,  18,  18)
CLR_PANEL2     = (42,  28,  28)
CLR_ROSE       = (145, 125, 180)
CLR_CYAN       = (200, 200,  60)

# ─────────────────────────────────────────────────────────────────────────────
#  LANDMARK INDEX SHORTCUTS
# ─────────────────────────────────────────────────────────────────────────────
IDX = {
    "nose":         0,
    "l_eye_inner":  1,  "l_eye":  2,  "l_eye_outer": 3,
    "r_eye_inner":  4,  "r_eye":  5,  "r_eye_outer": 6,
    "l_ear":        7,  "r_ear":  8,
    "l_mouth":      9,  "r_mouth": 10,
    "l_shoulder":  11,  "r_shoulder": 12,
    "l_elbow":     13,  "r_elbow":    14,
    "l_wrist":     15,  "r_wrist":    16,
    "l_pinky":     17,  "r_pinky":    18,
    "l_index":     19,  "r_index":    20,
    "l_thumb":     21,  "r_thumb":    22,
    "l_hip":       23,  "r_hip":      24,
    "l_knee":      25,  "r_knee":     26,
    "l_ankle":     27,  "r_ankle":    28,
    "l_heel":      29,  "r_heel":     30,
    "l_foot":      31,  "r_foot":     32,
}

# ─────────────────────────────────────────────────────────────────────────────
#  SKELETON CONNECTIONS
# ─────────────────────────────────────────────────────────────────────────────
SKELETON_CONNECTIONS = [
    ("l_ear",      "l_eye",       "head"),
    ("r_ear",      "r_eye",       "head"),
    ("l_eye",      "nose",        "head"),
    ("r_eye",      "nose",        "head"),
    ("l_shoulder", "r_shoulder",  "torso"),
    ("l_shoulder", "l_hip",       "torso"),
    ("r_shoulder", "r_hip",       "torso"),
    ("l_hip",      "r_hip",       "torso"),
    ("l_shoulder", "l_elbow",     "l_arm"),
    ("l_elbow",    "l_wrist",     "l_arm"),
    ("r_shoulder", "r_elbow",     "r_arm"),
    ("r_elbow",    "r_wrist",     "r_arm"),
    ("l_hip",      "l_knee",      "l_leg"),
    ("l_knee",     "l_ankle",     "l_leg"),
    ("l_ankle",    "l_heel",      "l_leg"),
    ("l_heel",     "l_foot",      "l_leg"),
    ("r_hip",      "r_knee",      "r_leg"),
    ("r_knee",     "r_ankle",     "r_leg"),
    ("r_ankle",    "r_heel",      "r_leg"),
    ("r_heel",     "r_foot",      "r_leg"),
]

# ─────────────────────────────────────────────────────────────────────────────
#  ANGLE CALCULATION
# ─────────────────────────────────────────────────────────────────────────────
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
    return (int(lm.x * w), int(lm.y * h))


# ─────────────────────────────────────────────────────────────────────────────
#  POSE DEFINITIONS  (10 poses)
#  NOTE: Angle ranges are anatomically estimated.
#        Use debug mode (D key) to measure real values and tune.
# ─────────────────────────────────────────────────────────────────────────────
POSES = {

    # ── 1. MOUNTAIN POSE ──────────────────────────────────────────────────────
    "Mountain Pose": {
        "key": "1", "sanskrit": "Tadasana", "level": "Beginner",
        "checks": [
            {"points": ("l_shoulder", "l_hip", "l_knee"),  "range": (165, 195),
             "label": "Left hip alignment",  "fix": "Straighten left side — hip is not neutral"},
            {"points": ("r_shoulder", "r_hip", "r_knee"),  "range": (165, 195),
             "label": "Right hip alignment", "fix": "Straighten right side — hip is not neutral"},
            {"points": ("l_hip", "l_knee", "l_ankle"),     "range": (165, 195),
             "label": "Left knee",           "fix": "Straighten the left knee fully"},
            {"points": ("r_hip", "r_knee", "r_ankle"),     "range": (165, 195),
             "label": "Right knee",          "fix": "Straighten the right knee fully"},
            {"points": ("l_elbow", "l_shoulder", "l_hip"), "range": (150, 210),
             "label": "Left arm",            "fix": "Relax left arm straight alongside the body"},
            {"points": ("r_elbow", "r_shoulder", "r_hip"), "range": (150, 210),
             "label": "Right arm",           "fix": "Relax right arm straight alongside the body"},
        ],
    },

    # ── 2. WARRIOR I ──────────────────────────────────────────────────────────
    "Warrior I": {
        "key": "2", "sanskrit": "Virabhadrasana I", "level": "Beginner",
        "checks": [
            {"points": ("l_hip", "l_knee", "l_ankle"),     "range": (75, 105),
             "label": "Front knee bend",  "fix": "Bend front knee to 90 degrees over the ankle"},
            {"points": ("r_hip", "r_knee", "r_ankle"),     "range": (155, 185),
             "label": "Back leg",         "fix": "Straighten the back leg fully"},
            {"points": ("l_elbow", "l_shoulder", "l_hip"), "range": (155, 210),
             "label": "Left arm raise",   "fix": "Raise the left arm straight overhead"},
            {"points": ("r_elbow", "r_shoulder", "r_hip"), "range": (155, 210),
             "label": "Right arm raise",  "fix": "Raise the right arm straight overhead"},
            {"points": ("l_shoulder", "l_hip", "l_knee"),  "range": (155, 195),
             "label": "Torso upright",    "fix": "Keep torso upright — do not lean forward"},
        ],
    },

    # ── 3. WARRIOR II ─────────────────────────────────────────────────────────
    "Warrior II": {
        "key": "3", "sanskrit": "Virabhadrasana II", "level": "Beginner",
        "checks": [
            {"points": ("l_hip", "l_knee", "l_ankle"),          "range": (75, 105),
             "label": "Front knee",          "fix": "Bend front knee to 90 degrees — track over second toe"},
            {"points": ("r_hip", "r_knee", "r_ankle"),          "range": (155, 185),
             "label": "Back leg",            "fix": "Straighten the back leg completely"},
            {"points": ("l_elbow", "l_shoulder", "r_shoulder"), "range": (155, 205),
             "label": "Left arm extension",  "fix": "Extend left arm fully parallel to the floor"},
            {"points": ("r_elbow", "r_shoulder", "l_shoulder"), "range": (155, 205),
             "label": "Right arm extension", "fix": "Extend right arm fully parallel to the floor"},
        ],
    },

    # ── 4. TREE POSE ──────────────────────────────────────────────────────────
    "Tree Pose": {
        "key": "4", "sanskrit": "Vrksasana", "level": "Beginner",
        "checks": [
            {"points": ("l_hip", "l_knee", "l_ankle"),     "range": (155, 185),
             "label": "Standing leg",    "fix": "Straighten the standing leg fully"},
            {"points": ("r_hip", "r_knee", "r_ankle"),     "range": (30, 90),
             "label": "Raised leg",      "fix": "Bend raised knee outward and press foot to thigh"},
            {"points": ("l_elbow", "l_shoulder", "l_hip"), "range": (155, 210),
             "label": "Left arm",        "fix": "Raise left arm overhead — reach through fingertips"},
            {"points": ("r_elbow", "r_shoulder", "r_hip"), "range": (155, 210),
             "label": "Right arm",       "fix": "Raise right arm overhead — reach through fingertips"},
        ],
    },

    # ── 5. TRIANGLE POSE ──────────────────────────────────────────────────────
    "Triangle Pose": {
        "key": "5", "sanskrit": "Trikonasana", "level": "Beginner",
        "checks": [
            {"points": ("l_hip", "l_knee", "l_ankle"),          "range": (160, 185),
             "label": "Front leg straight",   "fix": "Keep front leg straight — do not bend the knee"},
            {"points": ("r_hip", "r_knee", "r_ankle"),          "range": (160, 185),
             "label": "Back leg straight",    "fix": "Straighten the back leg fully"},
            {"points": ("l_elbow", "l_shoulder", "r_shoulder"), "range": (150, 210),
             "label": "Top arm reach",        "fix": "Extend top arm straight up toward the ceiling"},
            {"points": ("r_elbow", "r_shoulder", "l_shoulder"), "range": (150, 210),
             "label": "Bottom arm reach",     "fix": "Reach bottom arm down toward the shin or floor"},
            {"points": ("l_shoulder", "l_hip", "l_knee"),       "range": (120, 160),
             "label": "Lateral bend",         "fix": "Deepen the side bend — hinge more from the hip"},
        ],
    },

    # ── 6. EAGLE POSE ─────────────────────────────────────────────────────────
    "Eagle Pose": {
        "key": "6", "sanskrit": "Garudasana", "level": "Intermediate",
        "checks": [
            {"points": ("l_hip", "l_knee", "l_ankle"),     "range": (120, 155),
             "label": "Standing leg bend",  "fix": "Bend standing knee deeper — sink into the pose"},
            {"points": ("r_hip", "r_knee", "r_ankle"),     "range": (30, 80),
             "label": "Wrapped leg",        "fix": "Hook raised foot behind the standing calf"},
            {"points": ("l_elbow", "l_shoulder", "l_hip"), "range": (60, 100),
             "label": "Arms wrapped",       "fix": "Wrap arms tightly — lift elbows to shoulder height"},
            {"points": ("r_elbow", "r_shoulder", "r_hip"), "range": (60, 100),
             "label": "Elbow height",       "fix": "Keep both elbows lifted level with the shoulders"},
        ],
    },

    # ── 7. CHILD'S POSE ───────────────────────────────────────────────────────
    "Child's Pose": {
        "key": "7", "sanskrit": "Balasana", "level": "Beginner",
        "checks": [
            {"points": ("l_shoulder", "l_hip", "l_knee"),  "range": (20, 65),
             "label": "Torso fold",         "fix": "Fold torso fully forward — bring chest toward thighs"},
            {"points": ("r_shoulder", "r_hip", "r_knee"),  "range": (20, 65),
             "label": "Torso fold right",   "fix": "Fold torso fully forward — relax the lower back"},
            {"points": ("l_hip", "l_knee", "l_ankle"),     "range": (20, 60),
             "label": "Left knee bend",     "fix": "Sit hips back toward heels — deepen the knee bend"},
            {"points": ("r_hip", "r_knee", "r_ankle"),     "range": (20, 60),
             "label": "Right knee bend",    "fix": "Sit hips back toward heels — deepen the knee bend"},
            {"points": ("l_elbow", "l_shoulder", "l_hip"), "range": (140, 200),
             "label": "Arms extended",      "fix": "Reach arms fully forward — lengthen through fingertips"},
        ],
    },

    # ── 8. SEATED FORWARD FOLD ────────────────────────────────────────────────
    "Seated Forward Fold": {
        "key": "8", "sanskrit": "Paschimottanasana", "level": "Beginner",
        "checks": [
            {"points": ("l_shoulder", "l_hip", "l_knee"),  "range": (30, 80),
             "label": "Forward fold depth", "fix": "Hinge deeper from hips — lengthen the spine first"},
            {"points": ("r_shoulder", "r_hip", "r_knee"),  "range": (30, 80),
             "label": "Torso over legs",    "fix": "Fold torso forward — keep back as flat as possible"},
            {"points": ("l_hip", "l_knee", "l_ankle"),     "range": (160, 185),
             "label": "Left leg straight",  "fix": "Keep both legs straight — flex feet toward you"},
            {"points": ("r_hip", "r_knee", "r_ankle"),     "range": (160, 185),
             "label": "Right leg straight", "fix": "Keep both legs straight — do not lock knees hard"},
            {"points": ("l_elbow", "l_shoulder", "l_hip"), "range": (130, 200),
             "label": "Arms reach",         "fix": "Reach hands toward feet — hold shins ankles or feet"},
        ],
    },

    # ── 9. LOTUS POSE ─────────────────────────────────────────────────────────
    "Lotus Pose": {
        "key": "9", "sanskrit": "Padmasana", "level": "Intermediate",
        "checks": [
            {"points": ("l_shoulder", "l_hip", "l_knee"),  "range": (75, 115),
             "label": "Seated upright",     "fix": "Sit tall — lengthen the spine upward"},
            {"points": ("r_shoulder", "r_hip", "r_knee"),  "range": (75, 115),
             "label": "Posture right",      "fix": "Keep the torso upright — open the chest"},
            {"points": ("l_hip", "l_knee", "l_ankle"),     "range": (25, 65),
             "label": "Left leg cross",     "fix": "Place left foot on right thigh — rotate knee outward"},
            {"points": ("r_hip", "r_knee", "r_ankle"),     "range": (25, 65),
             "label": "Right leg cross",    "fix": "Place right foot on left thigh — open the hip"},
        ],
    },

    # ── 0. DANCER'S POSE ──────────────────────────────────────────────────────
    "Dancer's Pose": {
        "key": "0", "sanskrit": "Natarajasana", "level": "Intermediate",
        "checks": [
            {"points": ("l_hip", "l_knee", "l_ankle"),     "range": (155, 185),
             "label": "Standing leg",       "fix": "Keep the standing leg straight and grounded"},
            {"points": ("r_hip", "r_knee", "r_ankle"),     "range": (55, 100),
             "label": "Raised leg bend",    "fix": "Bend the raised leg — kick foot into your hand"},
            {"points": ("r_shoulder", "r_hip", "r_knee"),  "range": (120, 165),
             "label": "Backbend lift",      "fix": "Lift the raised leg higher — open through the chest"},
            {"points": ("l_elbow", "l_shoulder", "l_hip"), "range": (140, 200),
             "label": "Reach arm forward",  "fix": "Extend the free arm straight forward for balance"},
        ],
    },
}

POSE_NAMES = list(POSES.keys())
KEY_MAP    = {data["key"]: i for i, (_, data) in enumerate(POSES.items())}


# ─────────────────────────────────────────────────────────────────────────────
#  BUILD JOINT STATUS
# ─────────────────────────────────────────────────────────────────────────────
def build_joint_status(landmarks, pose_name, w, h):
    checks       = POSES[pose_name]["checks"]
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
            if name not in joint_status:
                joint_status[name] = ok
            else:
                joint_status[name] = joint_status[name] and ok

    score = int((passed / len(checks)) * 100) if checks else 100
    return joint_status, feedback, score


# ─────────────────────────────────────────────────────────────────────────────
#  DEBUG — show live angles for every check in the current pose
# ─────────────────────────────────────────────────────────────────────────────
def draw_debug_angles(frame, landmarks, pose_name, w, h):
    checks = POSES[pose_name]["checks"]
    FONT   = cv2.FONT_HERSHEY_SIMPLEX
    cv2.rectangle(frame, (0, 0), (340, 22 + len(checks) * 22), (10, 10, 10), -1)
    cv2.putText(frame, "DEBUG ANGLES", (8, 18), FONT, 0.48, CLR_CYAN, 1, cv2.LINE_AA)
    for i, check in enumerate(checks):
        a_name, b_name, c_name = check["points"]
        a      = get_pt(landmarks, a_name, w, h)
        b      = get_pt(landmarks, b_name, w, h)
        c      = get_pt(landmarks, c_name, w, h)
        angle  = calc_angle(a, b, c)
        lo, hi = check["range"]
        ok     = lo <= angle <= hi
        color  = CLR_GREEN if ok else CLR_RED
        text   = f"{check['label']}: {angle:.1f}  [{lo}-{hi}]"
        cv2.putText(frame, text, (8, 30 + i * 22), FONT, 0.40, color, 1, cv2.LINE_AA)


# ─────────────────────────────────────────────────────────────────────────────
#  DRAWING HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def draw_rounded_rect(img, x1, y1, x2, y2, radius, color, alpha=0.80):
    overlay = img.copy()
    cv2.rectangle(overlay, (x1 + radius, y1), (x2 - radius, y2), color, -1)
    cv2.rectangle(overlay, (x1, y1 + radius), (x2, y2 - radius), color, -1)
    for cx, cy in [(x1+radius, y1+radius), (x2-radius, y1+radius),
                   (x1+radius, y2-radius), (x2-radius, y2-radius)]:
        cv2.circle(overlay, (cx, cy), radius, color, -1)
    cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)


def draw_text_with_shadow(img, text, pos, font, scale, color, thickness=1):
    x, y = pos
    cv2.putText(img, text, (x+1, y+1), font, scale, (10, 10, 10), thickness + 1, cv2.LINE_AA)
    cv2.putText(img, text, pos,         font, scale, color,        thickness,     cv2.LINE_AA)


def draw_skeleton(frame, landmarks, joint_status, w, h):
    BONE_THICKNESS  = 3
    JOINT_RADIUS    = 6

    for (name_a, name_b, _) in SKELETON_CONNECTIONS:
        if name_a not in IDX or name_b not in IDX:
            continue
        pt_a  = get_pt(landmarks, name_a, w, h)
        pt_b  = get_pt(landmarks, name_b, w, h)
        ok_a  = joint_status.get(name_a, True)
        ok_b  = joint_status.get(name_b, True)
        color = CLR_GREEN if (ok_a and ok_b) else CLR_RED
        cv2.line(frame, pt_a, pt_b, color, BONE_THICKNESS, cv2.LINE_AA)

    for name in IDX:
        lm = landmarks[IDX[name]]
        if name in ("l_eye_inner", "r_eye_inner", "l_eye_outer", "r_eye_outer",
                    "l_mouth", "r_mouth", "l_pinky", "r_pinky",
                    "l_index", "r_index", "l_thumb", "r_thumb"):
            continue
        px    = int(lm.x * w)
        py    = int(lm.y * h)
        ok    = joint_status.get(name, True)
        color = CLR_GREEN if ok else CLR_RED
        cv2.circle(frame, (px, py), JOINT_RADIUS + 3, color, 1,  cv2.LINE_AA)
        cv2.circle(frame, (px, py), JOINT_RADIUS,     color, -1, cv2.LINE_AA)
        cv2.circle(frame, (px, py), 2,                CLR_WHITE, -1, cv2.LINE_AA)


def draw_feedback_panel(frame, pose_name, feedback, score, fps, H, W):
    PANEL_W = 300
    PANEL_X = W - PANEL_W
    MARGIN  = 14
    FONT    = cv2.FONT_HERSHEY_SIMPLEX
    FONT_SM = 0.42
    FONT_MD = 0.52
    FONT_LG = 0.72

    draw_rounded_rect(frame, PANEL_X, 0, W, H, 0, CLR_PANEL, alpha=0.82)
    cv2.rectangle(frame, (PANEL_X, 0), (W, 3), CLR_GOLD, -1)

    y = 28
    draw_text_with_shadow(frame, "DEHA", (PANEL_X + MARGIN, y), FONT, FONT_LG, CLR_GOLD, 2)
    y += 26
    cv2.line(frame, (PANEL_X + MARGIN, y), (W - MARGIN, y), CLR_GOLD, 1, cv2.LINE_AA)
    y += 14

    sanskrit = POSES[pose_name].get("sanskrit", "")
    draw_text_with_shadow(frame, sanskrit, (PANEL_X + MARGIN, y), FONT, FONT_SM, CLR_ROSE, 1)
    y += 16

    # Pose name (word wrap)
    words = pose_name.split()
    line  = ""
    for word in words:
        test = line + word + " "
        size = cv2.getTextSize(test, FONT, FONT_MD, 1)[0][0]
        if size > PANEL_W - 2 * MARGIN and line:
            draw_text_with_shadow(frame, line.strip(), (PANEL_X + MARGIN, y), FONT, FONT_MD, CLR_WHITE, 1)
            y    += 20
            line  = word + " "
        else:
            line = test
    if line.strip():
        draw_text_with_shadow(frame, line.strip(), (PANEL_X + MARGIN, y), FONT, FONT_MD, CLR_WHITE, 1)
    y += 24

    level    = POSES[pose_name].get("level", "")
    lv_color = CLR_GREEN if level == "Beginner" else (CLR_GOLD if level == "Intermediate" else CLR_RED)
    draw_text_with_shadow(frame, level, (PANEL_X + MARGIN, y), FONT, FONT_SM, lv_color, 1)
    y += 20

    cv2.line(frame, (PANEL_X + MARGIN, y), (W - MARGIN, y), CLR_PANEL2, 1)
    y += 14
    draw_text_with_shadow(frame, "Accuracy", (PANEL_X + MARGIN, y), FONT, FONT_SM, CLR_ROSE, 1)
    y += 18

    score_color = CLR_GREEN if score >= 70 else (CLR_GOLD if score >= 40 else CLR_RED)
    draw_text_with_shadow(frame, f"{score}%", (PANEL_X + MARGIN, y), FONT, FONT_LG, score_color, 2)
    y += 8

    bar_x1 = PANEL_X + MARGIN
    bar_x2 = W - MARGIN
    bar_h  = 6
    fill_w = int((bar_x2 - bar_x1) * score / 100)
    cv2.rectangle(frame, (bar_x1, y), (bar_x2, y + bar_h), CLR_PANEL2, -1)
    cv2.rectangle(frame, (bar_x1, y), (bar_x1 + fill_w, y + bar_h), score_color, -1)
    y += bar_h + 16

    cv2.line(frame, (PANEL_X + MARGIN, y), (W - MARGIN, y), CLR_PANEL2, 1)
    y += 14
    draw_text_with_shadow(frame, "Corrections", (PANEL_X + MARGIN, y), FONT, FONT_SM, CLR_ROSE, 1)
    y += 18

    if not feedback:
        draw_text_with_shadow(frame, "Form looks good — hold it!", (PANEL_X + MARGIN, y),
                               FONT, FONT_SM, CLR_GREEN, 1)
        y += 20
    else:
        for msg in feedback[:3]:
            cv2.circle(frame, (PANEL_X + MARGIN + 4, y - 4), 3, CLR_RED, -1)
            words = msg.split()
            line  = ""
            for word in words:
                test  = line + word + " "
                size  = cv2.getTextSize(test, FONT, FONT_SM, 1)[0][0]
                max_w = PANEL_W - 2 * MARGIN - 14
                if size > max_w and line:
                    draw_text_with_shadow(frame, line.strip(), (PANEL_X + MARGIN + 14, y),
                                          FONT, FONT_SM, CLR_OFFWHITE, 1)
                    y    += 16
                    line  = word + " "
                else:
                    line = test
            if line.strip():
                draw_text_with_shadow(frame, line.strip(), (PANEL_X + MARGIN + 14, y),
                                      FONT, FONT_SM, CLR_OFFWHITE, 1)
                y += 20

    y += 4
    cv2.line(frame, (PANEL_X + MARGIN, y), (W - MARGIN, y), CLR_PANEL2, 1)
    y += 14

    draw_text_with_shadow(frame, "Switch pose:", (PANEL_X + MARGIN, y), FONT, FONT_SM, CLR_ROSE, 1)
    y += 16
    for name, data in POSES.items():
        short = name.split("(")[0].strip()
        hint  = f"[{data['key']}] {short}"
        draw_text_with_shadow(frame, hint, (PANEL_X + MARGIN, y), FONT, 0.38, CLR_ROSE, 1)
        y += 15

    y += 4
    cv2.line(frame, (PANEL_X + MARGIN, y), (W - MARGIN, y), CLR_PANEL2, 1)
    y += 14
    draw_text_with_shadow(frame, f"FPS: {fps:.0f}", (PANEL_X + MARGIN, y), FONT, FONT_SM, CLR_ROSE, 1)
    draw_text_with_shadow(frame, "D=debug  ESC=quit", (PANEL_X + MARGIN + 65, y), FONT, 0.36, CLR_ROSE, 1)


def draw_top_badge(frame, pose_name, score, W):
    FONT   = cv2.FONT_HERSHEY_SIMPLEX
    FONT_S = 0.45
    text   = f"  {pose_name}   {score}%  "
    color  = CLR_GREEN if score >= 70 else (CLR_GOLD if score >= 40 else CLR_RED)
    (tw, th), _ = cv2.getTextSize(text, FONT, FONT_S, 1)
    draw_rounded_rect(frame, 10, 10, tw + 20, th + 22, 6, CLR_PANEL, alpha=0.75)
    cv2.putText(frame, text, (15, 28), FONT, FONT_S, color, 1, cv2.LINE_AA)


# ─────────────────────────────────────────────────────────────────────────────
#  MAIN LOOP
# ─────────────────────────────────────────────────────────────────────────────
def main():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,  1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    cap.set(cv2.CAP_PROP_FPS,          30)

    if not cap.isOpened():
        print("[ERROR] Cannot open camera. Check that your webcam is connected.")
        return

    WIN = "Deha — Pose Tracker"
    cv2.namedWindow(WIN, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(WIN, 1280, 720)

    current_pose_idx  = 0
    fps_prev_time     = time.time()
    fps               = 0.0
    debug_mode        = False
    SCORE_BUFFER_SIZE = 6
    score_buffer      = []
    start_ns          = time.time_ns()

    print(f"\n  Deha Pose Tracker started — {len(POSES)} poses loaded.")
    print("  Keys 1-0 to switch pose  |  D = debug angles  |  ESC = quit\n")

    with PoseLandmarker.create_from_options(options) as landmarker:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("[WARNING] Empty camera frame. Retrying...")
                continue

            frame = cv2.flip(frame, 1)
            H, W  = frame.shape[:2]

            rgb    = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_img = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
            ts_ms  = (time.time_ns() - start_ns) // 1_000_000

            result = landmarker.detect_for_video(mp_img, ts_ms)

            pose_name = POSE_NAMES[current_pose_idx]
            feedback  = ["Waiting for body detection..."]
            score     = 0

            if result.pose_landmarks and len(result.pose_landmarks) > 0:
                landmarks = result.pose_landmarks[0]
                joint_status, feedback, score = build_joint_status(landmarks, pose_name, W, H)

                score_buffer.append(score)
                if len(score_buffer) > SCORE_BUFFER_SIZE:
                    score_buffer.pop(0)
                score = int(sum(score_buffer) / len(score_buffer))

                draw_skeleton(frame, landmarks, joint_status, W, H)

                if debug_mode:
                    draw_debug_angles(frame, landmarks, pose_name, W, H)
            else:
                score_buffer.clear()

            now           = time.time()
            fps           = 1.0 / max(now - fps_prev_time, 1e-6)
            fps_prev_time = now

            draw_feedback_panel(frame, pose_name, feedback, score, fps, H, W)
            draw_top_badge(frame, pose_name, score, W)

            cv2.imshow(WIN, frame)

            key  = cv2.waitKey(1) & 0xFF
            char = chr(key).upper() if 32 <= key <= 126 else None

            if key == 27:
                break
            elif char == 'D':
                debug_mode = not debug_mode
                print(f"  Debug mode: {'ON' if debug_mode else 'OFF'}")
            elif char and char in KEY_MAP:
                new_idx = KEY_MAP[char]
                if new_idx != current_pose_idx:
                    current_pose_idx = new_idx
                    score_buffer.clear()
                    print(f"  Switched to: {POSE_NAMES[current_pose_idx]}")

    cap.release()
    cv2.destroyAllWindows()
    print("  Session ended.")


if __name__ == "__main__":
    main()