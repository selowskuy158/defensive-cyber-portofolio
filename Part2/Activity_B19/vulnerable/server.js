// VULNERABLE: stored XSS in a tiny Node.js/Express todo app.
// User-supplied task text is concatenated directly into HTML output, so a payload
// like  <script>alert(document.cookie)</script>  executes in every viewer's browser.
//
//   npm install express
//   node server.js                  # http://127.0.0.1:3001
//
// Demonstrate:
//   curl -X POST -d 'task=<script>alert(1)</script>' http://127.0.0.1:3001/add
//   curl http://127.0.0.1:3001/      # script tag is in the response

const express = require('express');
const app = express();
app.use(express.urlencoded({ extended: false }));

const tasks = [];   // in-memory store

app.get('/', (req, res) => {
  // BUG: tasks injected into HTML without any escaping
  const list = tasks.map(t => `<li>${t}</li>`).join('');
  res.send(`<!doctype html><meta charset="utf-8">
    <title>Todo (vulnerable)</title>
    <h1>My Todos</h1>
    <ul>${list}</ul>
    <form method="POST" action="/add">
      <input name="task" placeholder="new task">
      <button>add</button>
    </form>`);
});

app.post('/add', (req, res) => {
  tasks.push(req.body.task || '');   // no validation, no sanitisation
  res.redirect('/');
});

app.listen(3001, () => console.log('VULNERABLE app on http://127.0.0.1:3001'));
