import os
import json
import asyncio
import pytest
from httpx import AsyncClient
from src.app.main import app

CONTENT_ROOT = "/workspace/content"


def test_content_structure_minimal():
	# ensure two chapters exist as templates
	chapters = [d for d in os.listdir(CONTENT_ROOT) if os.path.isdir(os.path.join(CONTENT_ROOT, d))]
	assert len(chapters) >= 2, "At least two chapters should exist"
	for c in chapters[:2]:
		base = os.path.join(CONTENT_ROOT, c)
		for fname in [
			"overview.md",
			"exposition.md",
			"questions.json",
			"numericals.json",
			"activities.md",
			"misconceptions.md",
			"glossary.json",
			"tests.json",
		]:
			assert os.path.exists(os.path.join(base, fname)), f"Missing {fname} in {c}"


@pytest.mark.asyncio
async def test_gamification_flow(tmp_path):
	async with AsyncClient(app=app, base_url="http://test") as ac:
		# create student
		resp = await ac.post("/api/students/", json={"name": "Test"})
		assert resp.status_code == 200
		sid = resp.json()["id"]
		# start and answer a question for chapter ch01
		resp = await ac.post("/api/study/start", json={"student_id": sid, "chapter_id": "ch01", "mode": "study"})
		assert resp.status_code == 200
		q = resp.json()
		# submit incorrect answer to test hearts decrease
		resp = await ac.post("/api/study/submit", json={
			"student_id": sid,
			"chapter_id": "ch01",
			"skill_id": q.get("metadata", {}).get("skill_id", "general"),
			"question_id": q["id"],
			"answer": "Z"
		})
		assert resp.status_code == 200
		payload = resp.json()
		assert "hearts_remaining" in payload
		# fetch gamification state
		resp = await ac.get(f"/api/gamify/state/{sid}")
		assert resp.status_code == 200
		state = resp.json()
		assert "xp" in state and "streak_days" in state