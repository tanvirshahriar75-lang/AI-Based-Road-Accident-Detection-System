import React, { useEffect, useMemo, useState } from "react";

const API = (import.meta.env.VITE_API_BASE_URL || "http://localhost:8000").replace(/\/$/, "");

async function request(path, token, options = {}) {
  const headers = { ...(options.headers || {}) };
  if (token) headers.Authorization = `Bearer ${token}`;
  const response = await fetch(`${API}${path}`, { ...options, headers });
  if (!response.ok) {
    let message = `Request failed (${response.status})`;
    try { const body = await response.json(); message = body.detail || message; } catch {}
    throw new Error(message);
  }
  if (response.status === 204) return null;
  return response.json();
}

function App() {
  const [token, setToken] = useState(() => localStorage.getItem("roadwatch_token") || "");
  const [user, setUser] = useState(null);
  const [mode, setMode] = useState("login");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [fullName, setFullName] = useState("");
  const [videos, setVideos] = useState([]);
  const [selectedVideo, setSelectedVideo] = useState(null);
  const [accidents, setAccidents] = useState([]);
  const [file, setFile] = useState(null);
  const [busy, setBusy] = useState(false);
  const [notice, setNotice] = useState("");
  const [error, setError] = useState("");

  const selected = useMemo(() => videos.find((v) => v.id === selectedVideo) || null, [videos, selectedVideo]);

  async function loadVideos(auth = token) {
    const result = await request("/api/v1/videos", auth);
    setVideos(result.items || []);
    if (selectedVideo && !(result.items || []).some((v) => v.id === selectedVideo)) {
      setSelectedVideo(null); setAccidents([]);
    }
  }

  async function loadAccidents(videoId, auth = token) {
    const result = await request(`/api/v1/videos/${videoId}/accidents`, auth);
    setAccidents(result.items || []);
  }

  useEffect(() => {
    if (!token) return;
    request("/api/v1/auth/me", token)
      .then((profile) => { setUser(profile); return loadVideos(token); })
      .catch(() => { localStorage.removeItem("roadwatch_token"); setToken(""); setUser(null); });
  }, [token]);

  useEffect(() => {
    if (selectedVideo && token) loadAccidents(selectedVideo).catch((e) => setError(e.message));
  }, [selectedVideo, token]);

  async function authenticate(event) {
    event.preventDefault(); setBusy(true); setError(""); setNotice("");
    try {
      if (mode === "register") {
        await request("/api/v1/auth/register", "", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ email, password, full_name: fullName || null }) });
      }
      const result = await request("/api/v1/auth/login", "", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ email, password }) });
      localStorage.setItem("roadwatch_token", result.access_token); setToken(result.access_token); setNotice("Signed in successfully.");
    } catch (e) { setError(e.message); } finally { setBusy(false); }
  }

  async function uploadVideo(event) {
    event.preventDefault(); if (!file) return;
    setBusy(true); setError(""); setNotice("");
    try {
      const data = new FormData(); data.append("file", file);
      await request("/api/v1/videos/upload", token, { method: "POST", body: data });
      setFile(null); event.target.reset(); await loadVideos(); setNotice("Video uploaded. Select it below to request processing.");
    } catch (e) { setError(e.message); } finally { setBusy(false); }
  }

  async function processSelected() {
    if (!selected) return;
    setBusy(true); setError(""); setNotice("");
    try {
      await request(`/api/v1/videos/${selected.id}/process`, token, { method: "POST" });
      await loadVideos(); setNotice("Processing request queued. The current backend endpoint queues the video; it does not yet run the full AI pipeline.");
    } catch (e) { setError(e.message); } finally { setBusy(false); }
  }

  function logout() {
    localStorage.removeItem("roadwatch_token"); setToken(""); setUser(null); setVideos([]); setSelectedVideo(null); setAccidents([]); setNotice("Signed out.");
  }

  if (!token || !user) return <div className="auth-shell"><div className="auth-card"><div className="brand-mark">RW</div><p className="eyebrow">ROAD SAFETY INTELLIGENCE</p><h1>RoadWatch AI</h1><p className="muted">Sign in to manage traffic videos and review detected events.</p><form onSubmit={authenticate} className="stack">{mode === "register" && <label>Full name<input value={fullName} onChange={(e) => setFullName(e.target.value)} placeholder="Your name" /></label>}<label>Email address<input type="email" required value={email} onChange={(e) => setEmail(e.target.value)} placeholder="name@example.com" /></label><label>Password<input type="password" required minLength={mode === "register" ? 8 : 1} value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Enter your password" /></label><button disabled={busy}>{busy ? "Please wait…" : mode === "login" ? "Sign in" : "Create account"}</button></form><button className="link-button" onClick={() => { setMode(mode === "login" ? "register" : "login"); setError(""); }}>{mode === "login" ? "New here? Create an account" : "Already registered? Sign in"}</button>{error && <p className="alert error">{error}</p>}{notice && <p className="alert success">{notice}</p>}<p className="tiny">API: {API}</p></div></div>;

  return <div className="app-shell"><aside className="sidebar"><div className="brand"><span className="brand-mark small">RW</span><div><strong>RoadWatch AI</strong><small>Accident detection platform</small></div></div><div className="nav-label">WORKSPACE</div><div className="nav-item active">▦ <span>Dashboard</span></div><div className="side-note"><strong>Detection pipeline</strong><p>Upload → Queue → Review events</p><span className="status-dot" /> API-connected workspace</div><div className="profile"><div className="avatar">{(user.full_name || user.email || "U").slice(0, 1).toUpperCase()}</div><div className="profile-text"><strong>{user.full_name || "User"}</strong><small>{user.email}</small></div><button className="logout" onClick={logout} title="Sign out">↗</button></div></aside><main className="main"><header className="topbar"><div><p className="eyebrow">OVERVIEW</p><h1>Detection dashboard</h1><p className="muted">Manage uploaded traffic footage and review accident events.</p></div><button className="secondary" onClick={() => loadVideos().catch((e) => setError(e.message))}>↻ Refresh</button></header>{error && <div className="alert error">{error}</div>}{notice && <div className="alert success">{notice}</div>}<section className="stats"><div className="stat-card"><span className="stat-icon">▤</span><p>Total videos</p><strong>{videos.length}</strong><small>In your workspace</small></div><div className="stat-card"><span className="stat-icon amber">◷</span><p>Queued / processing</p><strong>{videos.filter((v) => ["queued", "processing"].includes(v.status)).length}</strong><small>Awaiting pipeline execution</small></div><div className="stat-card"><span className="stat-icon red">⚑</span><p>Recorded events</p><strong>{accidents.length}</strong><small>{selected ? `For video #${selected.id}` : "Select a video to view events"}</small></div></section><section className="content-grid"><div className="panel upload-panel"><div className="panel-heading"><div><p className="eyebrow">NEW ANALYSIS</p><h2>Upload traffic video</h2></div><span className="pill">MP4 · AVI · MOV · WEBM</span></div><form onSubmit={uploadVideo}><label className="dropzone"><span className="upload-icon">↑</span><strong>{file ? file.name : "Choose a video file"}</strong><small>{file ? `${(file.size / (1024 * 1024)).toFixed(1)} MB selected` : "Select a file from your computer"}</small><input type="file" accept="video/mp4,video/avi,video/x-msvideo,video/quicktime,video/webm,video/mpeg" onChange={(e) => setFile(e.target.files?.[0] || null)} /></label><button disabled={busy || !file}>{busy ? "Working…" : "Upload video"}</button></form><p className="hint">Maximum upload size is controlled by the backend configuration.</p></div><div className="panel pipeline-panel"><p className="eyebrow">SYSTEM FLOW</p><h2>Analysis pipeline</h2><div className="pipeline"><div className="pipeline-step done"><span>1</span><div><strong>Video upload</strong><small>File stored securely</small></div></div><div className="pipeline-line" /><div className="pipeline-step"><span>2</span><div><strong>Processing queue</strong><small>Request can be queued</small></div></div><div className="pipeline-line" /><div className="pipeline-step"><span>3</span><div><strong>AI event review</strong><small>Awaiting pipeline integration</small></div></div></div></div></section><section className="panel videos-panel"><div className="panel-heading"><div><p className="eyebrow">YOUR LIBRARY</p><h2>Uploaded videos <span className="count">{videos.length}</span></h2></div></div>{videos.length === 0 ? <div className="empty"><span>▤</span><strong>No videos uploaded yet</strong><p>Upload a traffic video to start your workspace.</p></div> : <div className="table-wrap"><table><thead><tr><th>VIDEO</th><th>STATUS</th><th>UPLOADED</th><th>ACTION</th></tr></thead><tbody>{videos.map((v) => <tr key={v.id} className={selectedVideo === v.id ? "selected-row" : ""}><td><strong>{v.filename}</strong><small>Video #{v.id}</small></td><td><span className={`badge ${v.status}`}>{v.status}</span></td><td>{new Date(v.created_at).toLocaleString()}</td><td><button className="text-button" onClick={() => setSelectedVideo(v.id)}>View events →</button></td></tr>)}</tbody></table></div>}</section><section className="panel events-panel"><div className="panel-heading"><div><p className="eyebrow">EVENT REVIEW</p><h2>{selected ? `Accident events · ${selected.filename}` : "Accident events"}</h2></div>{selected && <button className="secondary" disabled={busy || ["queued", "processing"].includes(selected.status)} onClick={processSelected}>Queue processing</button>}</div>{!selected ? <div className="empty compact"><span>⚑</span><strong>Select a video</strong><p>Choose a video above to inspect its recorded accident events.</p></div> : accidents.length === 0 ? <div className="empty compact"><span>✓</span><strong>No recorded events</strong><p>No accident records are currently associated with this video.</p></div> : <div className="table-wrap"><table><thead><tr><th>EVENT</th><th>CONFIDENCE</th><th>VIDEO TIME</th><th>REASON</th></tr></thead><tbody>{accidents.map((a) => <tr key={a.id}><td>#{a.id}</td><td>{(a.confidence * 100).toFixed(1)}%</td><td>{a.detected_at_seconds == null ? "—" : `${a.detected_at_seconds.toFixed(2)}s`}</td><td>{a.description || "—"}</td></tr>)}</tbody></table></div>}</section><footer>RoadWatch AI · Academic project workspace <span>Backend API: {API}</span></footer></main></div>;
}

export default App;
