/* ============================================================
   DEHA — Firebase Configuration
   Central file — imported by auth.js, session.js, profile.js
   ============================================================ */

import { initializeApp } from "https://www.gstatic.com/firebasejs/12.11.0/firebase-app.js";
import { getAuth } from "https://www.gstatic.com/firebasejs/12.11.0/firebase-auth.js";
import { getFirestore } from "https://www.gstatic.com/firebasejs/12.11.0/firebase-firestore.js";

const firebaseConfig = {
  apiKey:            "AIzaSyB7dFI3lFWKKAUIpgmocSbIu1jxwtdxV9w",
  authDomain:        "deha-yoga-visualizer.firebaseapp.com",
  projectId:         "deha-yoga-visualizer",
  storageBucket:     "deha-yoga-visualizer.firebasestorage.app",
  messagingSenderId: "810827625057",
  appId:             "1:810827625057:web:c848b6c83bd273b35c7020"
};

const app = initializeApp(firebaseConfig);

export const auth = getAuth(app);
export const db   = getFirestore(app);