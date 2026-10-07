# AI-Based Road Accident Detection System

An academic BSc CSE project for detecting potential road accidents from traffic video using computer vision, vehicle tracking, temporal analysis, and an extensible AI pipeline.

> **Current status:** Phase A foundation. No trained accident-detection model or experimental accuracy is claimed yet.

## Planned architecture

Video source → frame extraction → vehicle detection → multi-object tracking → motion/interaction analysis → temporal confirmation → accident event → evidence → database → dashboard.

## Technology stack

- Backend: Python, FastAPI, Pydantic, SQLAlchemy
- Computer vision: OpenCV, Ultralytics YOLO, NumPy
- Frontend: React, Vite
- Data: SQLite for development, PostgreSQL-ready architecture
- Testing: pytest
- DevOps: Docker Compose and GitHub Actions

## Repository structure

```text
backend/        FastAPI application and tests
frontend/       React dashboard
ai/             Detection/tracking interfaces and future training code
data/           Local runtime data (ignored by Git)
docs/           Project and research documentation
```

## Development

### Backend
```bash
cd backend
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API health: `GET /api/health`

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Docker
```bash
docker compose up --build
```

## Research integrity

All model metrics must come from reproducible experiments. Accuracy, precision, recall, F1, mAP, IoU, FPS, latency, and confusion matrices will not be fabricated or presented as measured results until the relevant experiments are actually completed.

## Roadmap

- [x] Phase A — project foundation
- [ ] Phase B — backend APIs and database
- [ ] Phase C — vehicle detection, tracking, and accident logic
- [ ] Phase D — evidence and event persistence
- [ ] Phase E — React dashboard
- [ ] Phase F — dataset training and evaluation
- [ ] Phase G — final testing and academic documentation
