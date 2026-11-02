# AI-Based Road Accident Detection System

An academic BSc CSE project for detecting potential road accidents from traffic video using computer vision, vehicle tracking, temporal analysis, and an extensible AI pipeline.

> **Current status:** Backend APIs and the initial React dashboard are implemented. Video processing is currently queue-only. Phase I now provides dataset preparation, leakage-safe split tooling, an event annotation schema, and evaluation scaffolding. No trained accident-detection model or experimental accuracy is claimed yet.

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
ai/             Detection/tracking interfaces, dataset and training workflow
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
# Optional: set VITE_API_BASE_URL in frontend/.env.local (default: http://localhost:8000)
npm run dev
```

Open the Vite URL (normally `http://localhost:5173`). Register an account, sign in, upload a supported traffic video, and review any accident records returned by the API. The dashboard currently queues processing requests; it does not yet execute the complete video-to-AI pipeline.

### Dataset and evaluation (Phase I)

Read [ai/dataset/README.md](ai/dataset/README.md) before collecting data. Create a video manifest with `video_id,label` columns and run:

```bash
python ai/scripts/split_dataset.py --input videos.csv --output-dir datasets/accident_events/splits --seed 42
```

Annotate ground-truth and predicted events as JSONL using [ai/dataset/annotations.schema.json](ai/dataset/annotations.schema.json), then evaluate:

```bash
python ai/scripts/evaluate_events.py --ground-truth ground_truth.jsonl --predictions predictions.jsonl --tolerance 2
```

See [ai/training/README.md](ai/training/README.md) for the vehicle-detector training workflow. These scripts are scaffolding; no dataset or trained weights are included.

### Docker
```bash
docker compose up --build
```

## Research integrity

All model metrics must come from reproducible experiments. Accuracy, precision, recall, F1, mAP, IoU, FPS, latency, and confusion matrices will not be fabricated or presented as measured results until the relevant experiments are actually completed.

## Roadmap

- [x] Phase A — project foundation
- [x] Phase B — backend APIs and database
- [x] Phase C — video management backend
- [x] Phase D — vehicle detection
- [x] Phase E — vehicle tracking
- [x] Phase F — accident detection baseline
- [x] Phase G — accident event persistence and snapshot storage
- [x] Phase H — initial React dashboard and API integration
- [x] Phase I — dataset preparation and evaluation scaffolding
- [ ] Phase J — final testing and academic documentation
