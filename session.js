/* ============================================================
   DEHA — SESSION PAGE JAVASCRIPT
   ============================================================ */

(function () {
  'use strict';

  /* ── Pose data ── */
  const POSES = {
    mountain: {
      name: 'Palm Tree Pose',
      sanskrit: 'Tadasana',
      tip: 'Stand tall, raise arms overhead and rise onto your toes. Balance and breathe.',
      corrections: [
        { area: 'Arms',    text: 'Raise both arms fully overhead, palms facing each other', sev: 'error' },
        { area: 'Balance', text: 'Rise onto the balls of your feet — engage the core to stabilise', sev: 'error' },
        { area: 'Spine',   text: 'Lengthen through the crown — do not arch the lower back', sev: 'correct' },
        { area: 'Gaze',    text: 'Fix gaze forward or gently upward to steady the balance', sev: 'error' },
        { area: 'Legs',    text: 'Keep both legs straight and squeeze the inner thighs', sev: 'correct' },
        { area: 'Breath',  text: 'Inhale as you rise, exhale as you lower — keep it flowing', sev: 'correct' },
      ]
    },
    warrior1: {
      name: 'Warrior I',
      sanskrit: 'Virabhadrasana I',
      tip: 'Strong lunge with hips squared forward and arms lifted overhead.',
      corrections: [
        { area: 'Hips',       text: 'Square both hips toward the front of your mat', sev: 'error' },
        { area: 'Front Knee', text: 'Bend the front knee to 90° directly over the ankle', sev: 'error' },
        { area: 'Arms',       text: 'Reach actively through the fingertips with shoulders drawing down', sev: 'correct' },
        { area: 'Back Foot',  text: 'Press the outer edge of the back foot firmly into the mat', sev: 'error' },
        { area: 'Torso',      text: 'Lift the torso upright — resist leaning forward', sev: 'correct' },
        { area: 'Gaze',       text: 'Look forward or gently upward between your hands', sev: 'correct' },
      ]
    },
    warrior2: {
      name: 'Warrior II',
      sanskrit: 'Virabhadrasana II',
      tip: 'Open hip stance with arms extended parallel to the floor.',
      corrections: [
        { area: 'Front Knee', text: 'Track the knee directly over the second toe', sev: 'error' },
        { area: 'Arms',       text: 'Keep both arms actively parallel and energised', sev: 'correct' },
        { area: 'Hips',       text: 'Open the hips wide — do not let them tip forward', sev: 'error' },
        { area: 'Torso',      text: 'Stack the torso over the pelvis, not leaning to either side', sev: 'correct' },
        { area: 'Gaze',       text: 'Gaze steadily over the front middle finger', sev: 'correct' },
        { area: 'Shoulders',  text: 'Relax the shoulders — they tend to creep up here', sev: 'error' },
      ]
    },
    tree: {
      name: 'Tree Pose',
      sanskrit: 'Vrksasana',
      tip: 'Balance on one foot. Place the other foot on the inner thigh.',
      corrections: [
        { area: 'Standing Hip', text: 'Keep the standing hip neutral — do not hike it up', sev: 'error' },
        { area: 'Raised Foot',  text: 'Press foot firmly into thigh and thigh back into foot', sev: 'error' },
        { area: 'Arms',         text: 'Reach through the fingertips, lift through the chest', sev: 'correct' },
        { area: 'Gaze',         text: 'Fix your gaze on one still point ahead to steady the balance', sev: 'error' },
        { area: 'Core',         text: 'Engage the core gently — it is your anchor here', sev: 'correct' },
        { area: 'Spine',        text: 'Grow tall through the crown — avoid collapsing sideways', sev: 'error' },
      ]
    },
    triangle: {
      name: 'Triangle Pose',
      sanskrit: 'Trikonasana',
      tip: 'Wide-leg stance with a lateral stretch and spinal rotation.',
      corrections: [
        { area: 'Spine',      text: 'Lengthen first, then tilt — do not crunch into the side body', sev: 'error' },
        { area: 'Top Arm',    text: 'Stack the top arm directly above the bottom arm', sev: 'error' },
        { area: 'Hips',       text: 'Open both hips toward the long edge of the mat', sev: 'correct' },
        { area: 'Front Leg',  text: 'Keep the front leg straight but do not lock the knee', sev: 'error' },
        { area: 'Gaze',       text: 'Look up toward the upper hand, but keep the neck relaxed', sev: 'correct' },
        { area: 'Chest',      text: 'Open the chest — rotate the top shoulder back and upward', sev: 'error' },
      ]
    },
    eagle: {
      name: 'Eagle Pose',
      sanskrit: 'Garudasana',
      tip: 'Wrap one arm under the other and one leg over the other. Sink and balance.',
      corrections: [
        { area: 'Arms',         text: 'Wrap arms completely — lift the elbows to shoulder height', sev: 'error' },
        { area: 'Legs',         text: 'Squeeze the thighs together and lower the hips deeper', sev: 'error' },
        { area: 'Standing Heel',text: 'Ground through the standing heel actively', sev: 'correct' },
        { area: 'Gaze',         text: 'Fix gaze on a single point ahead to stabilise', sev: 'error' },
        { area: 'Spine',        text: 'Keep the spine tall — resist rounding forward', sev: 'correct' },
      ]
    },
    dancer: {
      name: "Dancer's Pose",
      sanskrit: 'Natarajasana',
      tip: 'Stand on one leg. Reach back for the lifted foot. Extend the opposite arm forward.',
      corrections: [
        { area: 'Standing Leg', text: 'Root the standing leg firmly — knee soft, not locked', sev: 'correct' },
        { area: 'Lifted Leg',   text: 'Kick the foot actively into the hand rather than just pulling', sev: 'error' },
        { area: 'Reach Arm',    text: 'Extend the front arm forward and upward energetically', sev: 'error' },
        { area: 'Hips',         text: 'Keep both hips squared forward — do not open to the side', sev: 'error' },
        { area: 'Gaze',         text: 'Soft, steady gaze forward to maintain balance', sev: 'correct' },
      ]
    },
    child: {
      name: "Child's Pose",
      sanskrit: 'Balasana',
      tip: 'A resting fold. Hips toward heels, arms extended, forehead down.',
      corrections: [
        { area: 'Hips',     text: 'Sink hips back toward the heels completely', sev: 'error' },
        { area: 'Forehead', text: 'Rest the forehead gently on the mat and release the neck', sev: 'correct' },
        { area: 'Arms',     text: 'Extend arms fully forward and relax the shoulders', sev: 'error' },
        { area: 'Breath',   text: 'Breathe into the back body — let the ribs expand sideways', sev: 'correct' },
        { area: 'Neck',     text: 'Release all tension from the neck and jaw completely', sev: 'correct' },
      ]
    },
    lotus: {
      name: 'Lotus Pose',
      sanskrit: 'Padmasana',
      tip: 'Seated cross-leg with each foot resting on the opposite thigh.',
      corrections: [
        { area: 'Spine',     text: 'Sit tall — do not let the lower back collapse or round', sev: 'error' },
        { area: 'Knees',     text: 'Both knees should rest naturally toward the floor', sev: 'error' },
        { area: 'Hands',     text: 'Rest hands on knees, palms facing up or in Chin Mudra', sev: 'correct' },
        { area: 'Shoulders', text: 'Release the shoulders — let them fall away from the ears', sev: 'correct' },
        { area: 'Chin',      text: 'Tuck the chin very slightly to lengthen the back of the neck', sev: 'error' },
      ]
    },
    seated: {
      name: 'Seated Forward Fold',
      sanskrit: 'Paschimottanasana',
      tip: 'Sit tall, hinge forward from the hips, and reach toward the feet.',
      corrections: [
        { area: 'Spine',     text: 'Hinge from the hips — do not round the upper back to reach further', sev: 'error' },
        { area: 'Legs',      text: 'Press the backs of both legs firmly and evenly into the mat', sev: 'error' },
        { area: 'Reach',     text: 'Reach through the hands actively rather than just grabbing', sev: 'correct' },
        { area: 'Shoulders', text: 'Draw the shoulders down and away from the ears', sev: 'correct' },
        { area: 'Feet',      text: 'Flex the feet so toes point upward toward the ceiling', sev: 'error' },
      ]
    },
  };

  const TUTORIAL_DATA = {
    mountain: {
      level:   'Beginner',
      image:   'assets/Palm-tut.jpg',
      videoId: 'V_bSLebtVJs&list=LL&index=9',   // "Tadasana / Palm Tree Pose" tutorial
      steps: [
        'Stand with feet hip-width apart, arms relaxed at your sides.',
        'Inhale and raise both arms overhead, interlocking your fingers with palms facing up.',
        'Rise up onto your toes, stretching your whole body upward.',
        'Fix your gaze on a point slightly above eye level and hold for 3–5 breaths.',
      ]
    },
    warrior1: {
      level:   'Beginner',
      image:   'assets/WarriorI-tut.jpg',
      videoId: '98h26Ayke0s&list=LL&index=8',   // Warrior I beginner tutorial
      steps: [
        'Step your left foot back into a wide lunge, back heel angled at 45°.',
        'Bend the front knee to 90°, keeping it directly over the ankle.',
        'Square your hips forward and raise both arms overhead, palms facing each other.',
        'Lift the chest and hold for 5 steady breaths. Repeat on the other side.',
      ]
    },
    warrior2: {
      level:   'Beginner',
      image:   'assets/WarriorII-tut.jpg',
      videoId: 'YSjBJDkA6zg',   // Warrior II tutorial
      steps: [
        'Step feet wide apart. Turn the front foot out 90° and back foot in slightly.',
        'Bend the front knee to 90° directly over the ankle.',
        'Extend both arms parallel to the floor, palms facing down.',
        'Open hips to the side, gaze over your front fingertips. Hold for 5 breaths.',
      ]
    },
    tree: {
      level:   'Beginner',
      image:   'assets/Tree-tut.jpg',
      videoId: 'sxymAjTuUx0&list=LL&index=8',   // Tree Pose tutorial
      steps: [
        'Stand on your left leg, engage the core and find a fixed gaze point.',
        'Place the sole of your right foot on your left inner thigh (not on the knee).',
        'Press foot and thigh firmly against each other for stability.',
        'Bring hands to prayer at chest or raise overhead. Hold for 5 breaths each side.',
      ]
    },
    triangle: {
      level:   'Beginner',
      image:   'assets/Triangle-tut.jpg',
      videoId: 'Kh_tTk5_EGk&list=LL&index=3',   // Triangle Pose tutorial
      steps: [
        'Stand with feet wide apart. Turn front foot out 90°, back foot in slightly.',
        'Extend arms wide at shoulder height, then hinge sideways from the hip.',
        'Lower front hand to shin, ankle or the mat — keep the spine long.',
        'Stack top arm directly above bottom arm and gaze upward. Hold 5 breaths each side.',
      ]
    },
    eagle: {
      level:   'Intermediate',
      image:   'assets/Eagle-tut.jpg',
      videoId: 'Sq8o6BBi9uE&list=LL&index=4',   // Eagle Pose tutorial
      steps: [
        'Bend both knees slightly. Wrap the right leg over the left, hooking foot behind calf.',
        'Wrap right arm under left, lifting elbows to shoulder height.',
        'Sink hips deeper and squeeze thighs together for balance.',
        'Fix gaze on one steady point. Hold for 5 breaths then switch sides.',
      ]
    },
    dancer: {
      level:   'Intermediate',
      image:   'assets/Dancer-tut.jpg',
      videoId: '2HJvzYzjaP0&list=LL&index=6',   // Dancer's Pose tutorial
      steps: [
        'Stand on your left leg, reach back and hold your right ankle or foot.',
        'Kick the foot actively into your hand to create the backbend.',
        'Extend the left arm forward and upward for counterbalance.',
        'Keep hips squared forward. Hold for 5 breaths each side.',
      ]
    },
    child: {
      level:   'Beginner',
      image:   'assets/Child-tut.jpg',
      videoId: 'nMp3MlTz9fA&list=LL&index=7',   // Child's Pose tutorial
      steps: [
        'Kneel on the mat with big toes together, knees wide apart.',
        'Sink your hips back toward your heels and fold your torso forward.',
        'Extend arms fully forward, forehead resting gently on the mat.',
        'Breathe into the back body and hold as long as comfortable.',
      ]
    },
    lotus: {
      level:   'Intermediate',
      image:   'assets/Lotus-tut.jpg',
      videoId: 'ddnFSRprsdg&list=LL&index=2',   // Lotus Pose tutorial
      steps: [
        'Sit cross-legged and place your right foot on your left thigh.',
        'Then place your left foot on your right thigh, sole facing upward.',
        'Sit tall with the spine erect — do not let the lower back collapse.',
        'Rest hands on knees, close your eyes and breathe deeply for 1–3 minutes.',
      ]
    },
    seated: {
      level:   'Beginner',
      image:   'assets/Forward-tut.jpg',
      videoId: 'T8sgVyF4Ux4&list=LL&index=5',   // Seated Forward Fold tutorial
      steps: [
        'Sit with both legs extended straight in front, feet flexed.',
        'Inhale and lengthen the spine upward — grow as tall as possible.',
        'Exhale and hinge forward from the hips, keeping the back flat.',
        'Hold shins, ankles or feet. Breathe into the stretch for 5–10 breaths.',
      ]
    },
  };



  /* ── State ── */
  let sessionActive  = false;
  let videoStream    = null;
  let confirmedName  = '';
  let selectedPose   = '';
  let feedbackTimer  = null;
  let scoreTimer     = null;
  let sessionClock   = null;
  let sessionSecs    = 0;
  let currentScore   = 72;
  let scoreHistory   = [];
  let correctionLog  = {};
  let posesPracticed = [];
  let allScores      = {};   // scores per pose
  let skipTutorial_  = false; // skip tutorial checkbox state

  /* ── DOM refs ── */
  const nameInput       = document.getElementById('nameInput');
  const nameConfirmed   = document.getElementById('nameConfirmed');
  const nameDisplay     = document.getElementById('nameDisplay');
  const poseSelect      = document.getElementById('poseSelect');
  const poseBrief       = document.getElementById('poseBrief');
  const poseBriefName   = document.getElementById('poseBriefName');
  const poseBriefTip    = document.getElementById('poseBriefTip');
  const btnStart        = document.getElementById('btnStart');
  const startNote       = document.querySelector('.start-note');
  const ctrlPanel       = document.getElementById('ctrlPanel');
  const feedbackPanel   = document.getElementById('feedbackPanel');
  const summaryPanel    = document.getElementById('summaryPanel');
  const cameraPlaceholder = document.getElementById('cameraPlaceholder');
  const cameraLive      = document.getElementById('cameraLive');
  const videoEl         = document.getElementById('videoEl');
  const skeletonCanvas  = document.getElementById('skeletonCanvas');
  const stopModal       = document.getElementById('stopModal');
  const statusDot       = document.getElementById('statusDot');
  const statusText      = document.getElementById('statusText');
  const fpiName         = document.getElementById('fpiName');
  const scorePill       = document.getElementById('scorePill');

  /* ── Pose change ── */
  window.onPoseChange = function () {
    selectedPose = poseSelect.value;
    if (selectedPose && POSES[selectedPose]) {
      const p = POSES[selectedPose];
      poseBriefName.textContent = p.name + ' — ' + p.sanskrit;
      poseBriefTip.textContent  = p.tip;
      poseBrief.style.display   = 'block';
      btnStart.disabled = false;
      startNote.textContent = '';
    } else {
      poseBrief.style.display = 'none';
      btnStart.disabled = true;
      startNote.textContent = 'Select a pose above to begin';
    }
  };

  /* ── Start Session ── */
  window.startSession = async function () {
    if (!selectedPose) return;

    const user = localStorage.getItem('deha_current_user');
    if (!user) {
      const startNote = document.querySelector('.start-note');
      startNote.innerHTML = 'Please <a href="auth.html" style="color:var(--gold);font-weight:600;">sign in</a> or <a href="auth.html" style="color:var(--gold);font-weight:600;">create an account</a> to begin.';
      return;
    }

    // Show tutorial popup instead of starting camera directly
    openTutorial();
  };



  /* ── Stop modal ── */
  window.openStopModal  = () => stopModal.classList.add('open');
  window.closeStopModal = () => stopModal.classList.remove('open');

  window.confirmStop = function () {
    closeStopModal();
    endSession();
  };

  /* ── End session ── */
  function endSession() {
    // Stop camera
    if (videoStream) {
      videoStream.getTracks().forEach(t => t.stop());
      videoStream = null;
    }
    videoEl.srcObject = null;

    // Clear intervals
    clearInterval(feedbackTimer);
    clearInterval(scoreTimer);
    clearInterval(sessionClock);
    sessionActive = false;

    // Clear skeleton
    const ctx = skeletonCanvas.getContext('2d');
    ctx.clearRect(0, 0, skeletonCanvas.width, skeletonCanvas.height);
    window.removeEventListener('resize', resizeCanvas);

    // Status
    statusDot.classList.remove('live');
    statusText.textContent = 'Ended';

    // Hide camera, show placeholder end state
    cameraLive.style.display = 'none';
    cameraPlaceholder.style.display = 'flex';
    cameraPlaceholder.querySelector('.ph-title').textContent = 'Session ended';
    cameraPlaceholder.querySelector('.ph-desc').textContent =
      'Your summary is shown on the right. Start a new session when ready.';

    // Swap panels
    feedbackPanel.style.display = 'none';
    summaryPanel.style.display  = 'block';

    buildSummary();
  }

  /* ── Build summary ── */
  function buildSummary() {
    // Save final pose score
    allScores[selectedPose] = scoreHistory.length
      ? Math.round(scoreHistory.reduce((a, b) => a + b, 0) / scoreHistory.length)
      : Math.round(currentScore);

    // Average across all poses
    const allScoreValues = Object.values(allScores);
    const avg = allScoreValues.length
      ? Math.round(allScoreValues.reduce((a, b) => a + b, 0) / allScoreValues.length)
      : Math.round(currentScore);

    const stability = Math.min(99, Math.max(40, avg + Math.round((Math.random() - 0.4) * 10)));

    const mins = Math.floor(sessionSecs / 60);
    const secs = sessionSecs % 60;
    const durStr = mins > 0 ? `${mins}m ${secs}s` : `${secs}s`;

    const pose = POSES[selectedPose];

    // Most corrected area
    let topArea = null, topCount = 0;
    Object.entries(correctionLog).forEach(([area, count]) => {
      if (count > topCount) { topArea = area; topCount = count; }
    });

    document.getElementById('sumAccuracy').textContent  = avg + '%';
    document.getElementById('sumStability').textContent = stability + '%';
    document.getElementById('sumDuration').textContent  = durStr;
    document.getElementById('sumPose').textContent = posesPracticed.length > 0
      ? posesPracticed.map(k => POSES[k]?.name).filter(Boolean).join(', ')
      : pose ? pose.name : '—';

    const nameStr = confirmedName ? confirmedName : 'you';
    const congrats = avg >= 80
      ? `Wonderful work, ${nameStr}! Your form was consistent and your body alignment stayed on point throughout the session.`
      : avg >= 60
        ? `Good effort, ${nameStr}! You kept at it and made real progress. A little more attention to the highlighted areas will have you nailing this pose.`
        : `Keep going, ${nameStr} — every session builds the muscle memory. Focus on the areas flagged below in your next practice.`;

    document.getElementById('summaryCongrats').textContent = congrats;

    const hlText = topArea && topCount > 0
      ? `Most worked area: ${topArea} — corrected ${topCount} time${topCount > 1 ? 's' : ''} during the session.`
      : 'Your form was consistent throughout the session. Keep building on this.';
    document.getElementById('sumHighlight').textContent = hlText;
  }

  /* ── Reset (new session) ── */
  window.resetSession = function () {
    summaryPanel.style.display = 'none';
    ctrlPanel.style.display    = 'block';

    cameraPlaceholder.querySelector('.ph-title').textContent = 'Camera will activate here';
    cameraPlaceholder.querySelector('.ph-desc').textContent  =
      'Fill in the controls on the right, then click Start Session to begin your practice.';
    cameraPlaceholder.style.display = 'flex';

    poseSelect.value = '';
    poseBrief.style.display = 'none';
    btnStart.disabled = true;
    startNote.textContent = 'Select a pose above to begin';
    nameInput.value = '';
    nameConfirmed.style.display = 'none';
    confirmedName = '';
    selectedPose   = '';
    posesPracticed = [];
    allScores      = {};
    skipTutorial_  = false;

    statusDot.classList.remove('live');
    statusText.textContent = 'Ready';
  };

  /* ── Pose switcher pills ── */
  function buildPoseSwitcher() {
    const container = document.getElementById('poseSwitcher');
    if (!container) return;
    container.innerHTML = Object.entries(POSES).map(([key, pose]) => `
      <button
        class="pose-pill ${key === selectedPose ? 'active' : ''}"
        id="pill-${key}"
        onclick="switchPoseTo('${key}')"
      >${pose.name}</button>
    `).join('');
  }

  window.switchPoseTo = function(key) {
    if (key === selectedPose) return;
    window._pendingPose = key;
    if (skipTutorial_) {
      // Skip popup, switch directly
      closeTutorialAndStart();
    } else {
      openTutorial(key);
    }
  };

  function updatePosePills() {
    document.querySelectorAll('.pose-pill').forEach(btn => {
      btn.classList.toggle('active', btn.id === `pill-${selectedPose}`);
    });
  }

  /* ── Feedback loop ── */
  function startFeedbackLoop() {
    updateFeedback();
    feedbackTimer = setInterval(updateFeedback, 3600);
  }

  function updateFeedback() {
    const pool = POSES[selectedPose]?.corrections || [];
    if (!pool.length) return;

    const shuffled = [...pool].sort(() => Math.random() - 0.5).slice(0, 3);

    shuffled.forEach(c => {
      if (c.sev === 'error') {
        correctionLog[c.area] = (correctionLog[c.area] || 0) + 1;
      }
    });

    ['slot0', 'slot1', 'slot2'].forEach((id, i) => {
      const el = document.getElementById(id);
      const c  = shuffled[i];
      if (!c) {
        el.className = 'feedback-slot empty';
        el.innerHTML = '';
        return;
      }
      el.className = `feedback-slot ${c.sev}`;
      el.innerHTML = `
        <div class="slot-dot"></div>
        <div>
          <div class="slot-area">${c.area}</div>
          <div class="slot-text">${c.text}</div>
        </div>
      `;
    });
  }

  /* ── Score loop ── */
  function startScoreLoop() {
    updateScore();
    scoreTimer = setInterval(updateScore, 2800);
  }

  function updateScore() {
    const delta = (Math.random() - 0.45) * 14;
    currentScore = Math.max(36, Math.min(97, currentScore + delta));
    const s = Math.round(currentScore);
    scoreHistory.push(s);

    if (s >= 80) {
      scorePill.textContent = s + '% — Good';
      scorePill.style.color = '#7DC49A';
      scorePill.style.borderColor = 'rgba(80,160,110,0.30)';
      scorePill.style.background  = 'rgba(80,160,110,0.10)';
    } else if (s >= 60) {
      scorePill.textContent = s + '% — Fair';
      scorePill.style.color = 'var(--gold)';
      scorePill.style.borderColor = 'rgba(212,175,55,0.30)';
      scorePill.style.background  = 'rgba(212,175,55,0.10)';
    } else {
      scorePill.textContent = s + '% — Adjust';
      scorePill.style.color = '#D98080';
      scorePill.style.borderColor = 'rgba(200,80,80,0.30)';
      scorePill.style.background  = 'rgba(200,80,80,0.10)';
    }
  }

  /* ── Skeleton canvas ── */
  function resizeCanvas() {
    skeletonCanvas.width  = cameraLive.offsetWidth;
    skeletonCanvas.height = cameraLive.offsetHeight;
  }

  const ERROR_JOINTS = new Set(['lHip', 'rHip', 'lKnee']);

  function drawSkeletonLoop() {
    if (!sessionActive) return;

    const canvas = skeletonCanvas;
    const ctx    = canvas.getContext('2d');
    const W = canvas.width, H = canvas.height;
    ctx.clearRect(0, 0, W, H);

    const t = Date.now() / 1000;
    const sway = Math.sin(t * 0.35) * 0.014;
    const bob  = Math.sin(t * 0.55) * 0.007;

    const J = {
      nose:      [0.50 + sway, 0.11 + bob],
      lShoulder: [0.38 + sway, 0.24 + bob],
      rShoulder: [0.62 + sway, 0.24 + bob],
      lElbow:    [0.30 + sway, 0.36],
      rElbow:    [0.70 + sway, 0.36],
      lWrist:    [0.24 + sway, 0.49],
      rWrist:    [0.76 + sway, 0.49],
      lHip:      [0.42 + sway, 0.50 + bob],
      rHip:      [0.58 + sway, 0.50 + bob],
      lKnee:     [0.40 + sway, 0.67],
      rKnee:     [0.60 + sway, 0.67],
      lAnkle:    [0.40 + sway, 0.84],
      rAnkle:    [0.60 + sway, 0.84],
    };

    const CONNECTIONS = [
      ['lShoulder','rShoulder'],
      ['lShoulder','lElbow'],['lElbow','lWrist'],
      ['rShoulder','rElbow'],['rElbow','rWrist'],
      ['lShoulder','lHip'],['rShoulder','rHip'],
      ['lHip','rHip'],
      ['lHip','lKnee'],['lKnee','lAnkle'],
      ['rHip','rKnee'],['rKnee','rAnkle'],
    ];

    const px = (key) => [J[key][0] * W, J[key][1] * H];

    CONNECTIONS.forEach(([a, b]) => {
      const errA = ERROR_JOINTS.has(a);
      const errB = ERROR_JOINTS.has(b);
      ctx.beginPath();
      ctx.moveTo(...px(a));
      ctx.lineTo(...px(b));
      ctx.strokeStyle = (errA || errB)
        ? 'rgba(200,80,80,0.65)'
        : 'rgba(80,160,110,0.60)';
      ctx.lineWidth   = 2.4;
      ctx.lineCap     = 'round';
      ctx.stroke();
    });

    Object.keys(J).forEach(key => {
      const [x, y] = px(key);
      const isErr  = ERROR_JOINTS.has(key);
      ctx.beginPath();
      ctx.arc(x, y, 5.5, 0, Math.PI * 2);
      ctx.fillStyle   = isErr ? 'rgba(217,83,79,0.88)' : 'rgba(80,160,110,0.88)';
      ctx.fill();
      ctx.strokeStyle = isErr ? 'rgba(217,83,79,0.25)' : 'rgba(80,160,110,0.25)';
      ctx.lineWidth   = 3.5;
      ctx.stroke();
    });

    requestAnimationFrame(drawSkeletonLoop);
  }

  /* ── Tutorial popup ── */
  window.openTutorial = function(poseKey) {
    const key  = poseKey || selectedPose;
    const tut  = TUTORIAL_DATA[key];
    const pose = POSES[key];
    if (!tut || !pose) return;

    document.getElementById('tutTitle').textContent    = pose.name;
    document.getElementById('tutSanskrit').textContent = pose.sanskrit;
    document.getElementById('tutLevel').textContent    = tut.level;
    document.getElementById('tutImg').src              = tut.image;
    document.getElementById('tutImg').alt              = pose.name;

    document.getElementById('tutVideoLink').href =
      `https://www.youtube.com/watch?v=${tut.videoId}`;
    document.getElementById('tutVideoThumb').src =
      `https://img.youtube.com/vi/${tut.videoId}/hqdefault.jpg`;

    const list = document.getElementById('tutStepsList');
    list.innerHTML = tut.steps.map(s => `<li>${s}</li>`).join('');

    document.getElementById('tutModal').classList.add('open');
  }

  window.skipTutorial = function () {
    closeTutorialAndStart();
  };

  window.beginAfterTutorial = function () {
    closeTutorialAndStart();
  };

  async function closeTutorialAndStart() {
    const modal = document.getElementById('tutModal');
    modal.classList.remove('open');
    document.getElementById('tutVideoThumb').src = '';

    // Save checkbox state
    const cb = document.getElementById('skipTutCheck');
    if (cb) skipTutorial_ = cb.checked;

    // Mid-session pose switch — no camera request needed
    if (sessionActive && window._pendingPose) {
      // Save current pose score before switching
      allScores[selectedPose] = scoreHistory.length
        ? Math.round(scoreHistory.reduce((a, b) => a + b, 0) / scoreHistory.length)
        : Math.round(currentScore);

      selectedPose = window._pendingPose;
      window._pendingPose = null;

      if (!posesPracticed.includes(selectedPose)) posesPracticed.push(selectedPose);

      fpiName.textContent = POSES[selectedPose].name;
      currentScore  = 72;
      scoreHistory  = [];
      clearInterval(feedbackTimer);
      clearInterval(scoreTimer);
      startFeedbackLoop();
      startScoreLoop();
      updatePosePills();
      return;
    }

    window._pendingPose = null;

    // Fresh session start — request camera only once
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: 'user', width: { ideal: 1280 }, height: { ideal: 720 } }
      });
      videoStream = stream;
      videoEl.srcObject = stream;

      try {
        const p = JSON.parse(localStorage.getItem('deha_profile'));
        confirmedName = p?.username || '';
      } catch (e) { confirmedName = ''; }

      const nametag = document.getElementById('cameraNametag');
      if (confirmedName) {
        nametag.textContent   = confirmedName;
        nametag.style.display = 'block';
      }

      cameraPlaceholder.style.display = 'none';
      cameraLive.style.display        = 'flex';
      ctrlPanel.style.display         = 'none';
      feedbackPanel.style.display     = 'block';

      statusDot.classList.add('live');
      statusText.textContent = 'Live';
      fpiName.textContent    = POSES[selectedPose].name;

      resizeCanvas();
      window.addEventListener('resize', resizeCanvas);

      sessionActive  = true;
      sessionSecs    = 0;
      currentScore   = 72;
      scoreHistory   = [];
      correctionLog  = {};
      posesPracticed = [selectedPose];
      allScores      = {};
      skipTutorial_  = false;

      sessionClock = setInterval(() => sessionSecs++, 1000);
      startFeedbackLoop();
      startScoreLoop();
      drawSkeletonLoop();
      buildPoseSwitcher();

    } catch (err) {
      alert('Camera access was denied. Please allow camera permission and try again.');
    }
  }

  /* ── Auth check on load ── */
  window.addEventListener('DOMContentLoaded', () => {
    const user      = localStorage.getItem('deha_current_user');
    const btnStart  = document.getElementById('btnStart');
    const startNote = document.querySelector('.start-note');
    if (!user) {
      btnStart.disabled = true;
      startNote.innerHTML = 'Please <a href="auth.html" style="color:var(--gold);font-weight:600;">sign in</a> to begin your session';
    }
  });

})();