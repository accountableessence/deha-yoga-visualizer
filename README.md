# Deha — Real-Time Yoga Pose Correction System

> *Move with intention.*

Deha is a browser-based AI yoga assistant that provides real-time posture correction using your webcam. No app installation required — open, log in, and practice.

---

## Overview

Deha captures your webcam feed, analyses your body pose frame by frame using MediaPipe, calculates joint angles, and tells you exactly what to fix — in real time. Every session is saved to the cloud so you can track your progress over time.

---

## Key Features

- **Live skeleton overlay** — green joints for correct alignment, red for joints needing correction
- **Real-time accuracy score** — Good / Fair / Adjust, updated every frame
- **Specific correction messages** — up to 3 per frame telling you exactly what to fix
- **10 yoga poses** — beginner to intermediate
- **Mid-session pose switching** — no camera restart needed
- **Tutorial popup** — step-by-step instructions + YouTube reference before each pose
- **Session summary** — accuracy, stability score, duration, most corrected area
- **Firebase Authentication** — secure email/password login and signup
- **Firestore session history** — every session saved and displayed in your profile
- **Practice pattern analysis** — streak, average accuracy, recurring weak areas
- **Delete account** — full data wipe with confirmation

---

## Poses Supported

| Category | Poses |
|----------|-------|
| Standing | Palm Tree (Tadasana), Warrior I, Warrior II, Tree Pose, Triangle Pose |
| Balance | Eagle Pose, Dancer's Pose |
| Floor | Child's Pose, Lotus Pose, Seated Forward Fold |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML, CSS, JavaScript (ES Modules) |
| Real-time comms | Socket.IO (WebSocket) |
| Backend | Python, Flask, Flask-SocketIO |
| Pose detection | MediaPipe PoseLandmarker (VIDEO mode) |
| Frame processing | OpenCV, NumPy |
| Authentication | Firebase Authentication |
| Database | Firebase Firestore |

---

## Project Structure

```
deha/
├── index.html               # Landing page
├── session.html             # Live session page
├── profile.html             # User profile + session history
├── auth.html                # Login and signup
├── style.css                # Global styles
├── session.css              # Session page styles
├── session.js               # Session logic + WebSocket + Firebase save
├── profile.css              # Profile page styles
├── profile.js               # Profile logic — Firestore integration
├── auth.css                 # Auth page styles
├── auth.js                  # Firebase Authentication logic
├── firebase.js              # Firebase config (not committed — see setup)
├── firebase.example.js      # Template for firebase.js
├── splash.css               # Splash screen styles
├── splash.js                # Splash screen logic
├── app.py                   # Flask backend — MediaPipe + WebSocket server
├── pose_test.py             # Standalone pose calibration tool
├── requirements.txt         # Python dependencies
├── Procfile                 # For future cloud deployment
├── pose_landmarker_lite.task  # MediaPipe model file
└── assets/                  # Pose tutorial images + logo
```

---

## How It Works

```
Browser (webcam)
    │
    │  base64 JPEG frames (~6-7 fps via WebSocket)
    ▼
Flask backend (app.py)
    │
    ├── OpenCV + NumPy — decode frame
    ├── MediaPipe — detect 33 body landmarks
    └── Angle checker — compute joint angles, compare against pose ranges
    │
    │  landmarks + joint status + corrections (via WebSocket)
    ▼
Browser (session.js)
    │
    ├── HTML Canvas — draw colour-coded skeleton overlay
    ├── Feedback panel — display corrections + score
    └── Firebase Firestore — save session on end
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- A webcam
- Chrome browser (recommended)
- A Firebase project (see setup below)

### 1. Clone the repo

```bash
git clone https://github.com/your-username/deha.git
cd deha
```

### 2. Install Python dependencies

```bash
pip install flask flask-cors flask-socketio mediapipe opencv-python numpy
```

### 3. Download the MediaPipe model

Download `pose_landmarker_lite.task` from the [MediaPipe Models page](https://developers.google.com/mediapipe/solutions/vision/pose_landmarker) and place it in the project root alongside `app.py`.

### 4. Set up Firebase

1. Go to [Firebase Console](https://console.firebase.google.com) and create a project
2. Enable **Authentication** → Email/Password
3. Enable **Firestore Database** → Start in test mode
4. Go to Project Settings → Add a web app → Copy the config
5. Copy `firebase.example.js` to `firebase.js` and fill in your config:

```bash
cp firebase.example.js firebase.js
```

```js
const firebaseConfig = {
  apiKey:            "YOUR_API_KEY",
  authDomain:        "YOUR_AUTH_DOMAIN",
  projectId:         "YOUR_PROJECT_ID",
  storageBucket:     "YOUR_STORAGE_BUCKET",
  messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
  appId:             "YOUR_APP_ID"
};
```

> `firebase.js` is in `.gitignore` — never commit it to GitHub.

### 5. Set Firestore security rules

In Firebase Console → Firestore → Rules:

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /users/{userId}/{document=**} {
      allow read, write: if request.auth != null
                         && request.auth.uid == userId;
    }
  }
}
```

### 6. Run the app

```bash
python app.py
```

Open [http://localhost:5000](http://localhost:5000) in your browser.

---

## Firestore Data Structure

```
users/
└── {uid}/
    ├── profile/
    │   └── data        → { username, email, gender, height }
    └── sessions/
        └── {autoId}    → { pose, accuracy, stability, duration,
                            durationSecs, topArea, createdAt }
```

---

## Results

When correct form is held and the full skeleton turns green, the system consistently reports **90–100% accuracy** across all ten poses. Detection is most reliable for standing poses with clear landmark visibility (Tadasana, Warrior II, Triangle) and slightly less reliable for poses involving wrapped or occluded limbs (Eagle Pose, Dancer's Pose).

---

## Known Limitations

- Frame rate limited to ~6–7 fps due to WebSocket base64 encoding overhead
- Detection accuracy drops under poor lighting or with low-contrast clothing
- Requires localhost — Python backend cannot run on static hosting platforms

---

## License

Built as an academic project. Not licensed for commercial use.

---

*Built with MediaPipe · Flask · Firebase · HTML/CSS/JS*
