import React from "react";
import { createRoot } from "react-dom/client";

function App() {
  return (
    <main style={{fontFamily: "system-ui", maxWidth: 900, margin: "60px auto", padding: 24}}>
      <h1>AI-Based Road Accident Detection System</h1>
      <p>Phase A foundation is ready. Backend APIs, computer-vision services, authentication, and dashboard modules will be added in the next phases.</p>
      <p>Backend health endpoint: <code>/api/health</code></p>
    </main>
  );
}

createRoot(document.getElementById("root")).render(<App />);
