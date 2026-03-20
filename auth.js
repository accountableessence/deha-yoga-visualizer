/* ============================================================
   DEHA — AUTH PAGE LOGIC (Firebase Auth)
   ============================================================ */

import { auth } from './firebase.js';
import {
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  onAuthStateChanged
} from "https://www.gstatic.com/firebasejs/12.11.0/firebase-auth.js";

/* ── Redirect if already logged in ── */
onAuthStateChanged(auth, (user) => {
  if (user) window.location.href = 'profile.html';
});

/* ── Flip between sign in / sign up ── */
window.doFlip = function () {
  const card = document.getElementById('flipCard');
  card.classList.toggle('flipped');
};

/* ── Password visibility toggle ── */
window.togglePassword = function (inputId, btn) {
  const input = document.getElementById(inputId);
  if (!input) return;
  const isHidden = input.type === 'password';
  input.type = isHidden ? 'text' : 'password';
  btn.innerHTML = isHidden
    ? `<svg width="16" height="16" viewBox="0 0 16 16" fill="none">
         <path d="M2 2l12 12M6.5 6.6A2.5 2.5 0 0 0 9.4 9.5M4.2 4.3C2.5 5.4 1 8 1 8s2.5 5 7 5c1.4 0 2.7-.4 3.8-1M7 3.1C7.3 3 7.7 3 8 3c4.5 0 7 5 7 5s-.7 1.4-1.8 2.6" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" fill="none"/>
       </svg>`
    : `<svg width="16" height="16" viewBox="0 0 16 16" fill="none">
         <path d="M1 8s2.5-5 7-5 7 5 7 5-2.5 5-7 5-7-5-7-5Z" stroke="currentColor" stroke-width="1.3" fill="none"/>
         <circle cx="8" cy="8" r="2.5" stroke="currentColor" stroke-width="1.3" fill="none"/>
       </svg>`;
};

/* ── Password strength ── */
const signupPassword = document.getElementById('signupPassword');
if (signupPassword) {
  signupPassword.addEventListener('input', () => {
    const val   = signupPassword.value;
    const fill  = document.getElementById('strengthFill');
    const label = document.getElementById('strengthLabel');
    if (!fill || !label) return;

    let strength = 'weak';
    if (val.length >= 12 && /[A-Z]/.test(val) && /[0-9]/.test(val) && /[^A-Za-z0-9]/.test(val)) {
      strength = 'strong';
    } else if (val.length >= 8 && (/[A-Z]/.test(val) || /[0-9]/.test(val))) {
      strength = 'medium';
    }

    fill.className  = 'auth-strength-fill '  + (val.length ? strength : '');
    label.className = 'auth-strength-label ' + (val.length ? strength : '');
    label.textContent = val.length === 0 ? '' :
      strength === 'strong' ? 'Strong password' :
      strength === 'medium' ? 'Getting there…' :
      'Too weak — add numbers & symbols';
  });
}

/* ── Show / clear error ── */
function showError(id, msg) {
  const el = document.getElementById(id);
  if (!el) return;
  el.textContent = msg;
  el.style.display = 'block';
}
function clearError(id) {
  const el = document.getElementById(id);
  if (el) el.style.display = 'none';
}

/* ── Firebase error messages ── */
function friendlyError(code) {
  switch (code) {
    case 'auth/user-not-found':       return 'No account found for that email. Create one first!';
    case 'auth/wrong-password':       return 'Incorrect password. Please try again.';
    case 'auth/email-already-in-use': return 'An account with that email already exists. Try signing in!';
    case 'auth/weak-password':        return 'Password must be at least 6 characters.';
    case 'auth/invalid-email':        return 'Please enter a valid email address.';
    case 'auth/invalid-credential':   return 'Incorrect email or password. Please try again.';
    default:                          return 'Something went wrong. Please try again.';
  }
}

/* ── LOGIN handler ── */
window.handleLogin = async function (e) {
  e.preventDefault();
  clearError('loginError');

  const email = document.getElementById('loginEmail')?.value.trim();
  const pass  = document.getElementById('loginPassword')?.value;
  const btn   = e.target.querySelector('button[type="submit"]');

  btn.disabled = true;
  btn.textContent = 'Signing in…';

  try {
    await signInWithEmailAndPassword(auth, email, pass);
    // onAuthStateChanged will handle redirect
  } catch (err) {
    showError('loginError', friendlyError(err.code));
    btn.disabled = false;
    btn.innerHTML = 'Sign In <svg width="15" height="15" viewBox="0 0 15 15" fill="none"><path d="M3 7.5h9M8.5 4l3.5 3.5L8.5 11" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>';
  }
};

/* ── SIGNUP handler ── */
window.handleSignup = async function (e) {
  e.preventDefault();
  clearError('signupError');

  const email   = document.getElementById('signupEmail')?.value.trim();
  const pass    = document.getElementById('signupPassword')?.value;
  const confirm = document.getElementById('signupConfirm')?.value;
  const btn     = e.target.querySelector('button[type="submit"]');

  if (pass !== confirm) {
    showError('signupError', "Passwords don't match. Please check and try again.");
    return;
  }
  if (pass.length < 8) {
    showError('signupError', 'Password must be at least 8 characters.');
    return;
  }

  btn.disabled = true;
  btn.textContent = 'Creating account…';

  try {
    await createUserWithEmailAndPassword(auth, email, pass);
    // onAuthStateChanged will handle redirect
  } catch (err) {
    showError('signupError', friendlyError(err.code));
    btn.disabled = false;
    btn.innerHTML = 'Create Account <svg width="15" height="15" viewBox="0 0 15 15" fill="none"><path d="M3 7.5h9M8.5 4l3.5 3.5L8.5 11" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>';
  }
};