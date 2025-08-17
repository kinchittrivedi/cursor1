# Gamified, Agentic AI Tutor for CBSE Class 8 Science

Production-grade, syllabus-aligned, gamified AI tutor with multi-agent orchestration, RAG over content corpus, and teacher analytics.

## Quickstart

1) Create venv and install deps
```
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

2) Initialize DB and build retrieval index
```
python -m src.scripts.init_db
python -m src.scripts.build_index
```

3) Run API server
```
uvicorn src.app.main:app --reload --host 0.0.0.0 --port 8000
```

4) Open UI
- Student: http://localhost:8000/ui/student/
- Teacher: http://localhost:8000/ui/teacher/

## Repo Layout
```
/content/<chapter_id>/
  overview.md
  exposition.md
  questions.json
  numericals.json
  activities.md
  misconceptions.md
  glossary.json
  tests.json
/src/
  app/        # FastAPI app, routers, models, schemas
  agents/     # planner, tutor, evaluator, coach, orchestrator
  tools/      # retrieval (FAISS), librarian, progress store, grader
  gamification/ # xp, streaks, badges, quests, leaderboards, events
  scripts/    # utilities: init_db, build_index, seed_demo
/tests/
  test_acceptance.py
/ui/
  student/    # minimal student web UI
  teacher/    # minimal teacher dashboard
```

## Notes
- Content for two chapters is included fully as a template. Use `src/scripts/seed_demo.py` to add more.
- Feature flags for gamification live in `src/gamification/config.py`.
- DB defaults to SQLite at `data/tutor.db`. Set `DATABASE_URL` to use Postgres.
