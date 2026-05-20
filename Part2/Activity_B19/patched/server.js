// PATCHED: same todo app with three layers of defence against stored XSS.
//
// Layer 1 -- Input validation (allow-list character pattern + length cap).
// Layer 2 -- Contextual HTML-entity encoding when rendering.
// Layer 3 -- Restrictive Content-Security-Policy header (no inline scripts).
//
//   npm install express
//   node server.js                  # http://127.0.0.1:3002

const express = require('express');
const app = express();
app.use(express.urlencoded({ extended: false }));

const tasks = [];
const MAX_TASK_LEN = 200;
const SAFE_TASK_RE = /^[\w\s.,!?'"-]{1,200}$/;   // letters, digits, basic punctuation

function escapeHtml(s) {
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

// Layer 3 -- defence-in-depth header
app.use((req, res, next) => {
  res.setHeader('Content-Security-Policy',
    "default-src 'self'; script-src 'none'; style-src 'self' 'unsafe-inline'; object-src 'none'; base-uri 'none'");
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('X-Frame-Options', 'DENY');
  next();
});

app.get('/', (req, res) => {
  // Layer 2 -- escape every task before injection
  const list = tasks.map(t => `<li>${escapeHtml(t)}</li>`).join('');
  res.send(`<!doctype html><meta charset="utf-8">
    <title>Todo (patched)</title>
    <h1>My Todos</h1>
    <ul>${list}</ul>
    <form method="POST" action="/add">
      <input name="task" placeholder="new task" maxlength="200">
      <button>add</button>
    </form>`);
});

app.post('/add', (req, res) => {
  const task = (req.body.task || '').trim();
  // Layer 1 -- reject anything that isn't plain text
  if (!SAFE_TASK_RE.test(task)) {
    return res.status(400).send('Rejected: task must be 1-200 chars of letters/digits/basic punctuation.');
  }
  tasks.push(task);
  res.redirect('/');
});

app.listen(3002, () => console.log('PATCHED app on http://127.0.0.1:3002'));
