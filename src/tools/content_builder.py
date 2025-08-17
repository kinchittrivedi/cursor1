import os
import re
import json
from typing import List, Dict, Tuple
from collections import Counter, defaultdict

STOPWORDS = set(
	"a an the is are was were be been being to of and or in on at from by with for as that this these those it its their them there here into over under about after before during between among not no yes you we they he she i his her our your which who whom whose what when where why how do does did done make makes made have has had more most many much few fewer little less than then so such because cause effect also may might can could should would will shall".split()
)


def normalize_space(text: str) -> str:
	return re.sub(r"\s+", " ", text).strip()


def split_chapters(full_text: str) -> List[Tuple[str, str]]:
	# Returns list of (title, text)
	pattern = re.compile(r"\n\s*(CHAPTER\s+\d+[:\.]?\s*.+?)\n", re.IGNORECASE)
	matches = list(pattern.finditer(full_text))
	if not matches:
		# fallback: split by 'Chapter ' case-insensitive
		pattern = re.compile(r"\n\s*(Chapter\s+\d+[:\.]?\s*.+?)\n", re.IGNORECASE)
		matches = list(pattern.finditer(full_text))

	chapters = []
	if not matches:
		return [("Chapter 1", full_text)]
	for idx, m in enumerate(matches):
		title = normalize_space(m.group(1))
		start = m.end()
		end = matches[idx + 1].start() if idx + 1 < len(matches) else len(full_text)
		chap_text = full_text[start:end]
		chapters.append((title, chap_text))
	return chapters


def tokenize(text: str) -> List[str]:
	words = re.findall(r"[A-Za-z][A-Za-z\-]+", text)
	return [w.lower() for w in words if w.lower() not in STOPWORDS and len(w) > 2]


def top_keywords(text: str, k: int = 20) -> List[str]:
	freq = Counter(tokenize(text))
	return [w for w, _ in freq.most_common(k)]


def sentences(text: str) -> List[str]:
	parts = re.split(r"(?<=[.!?])\s+", normalize_space(text))
	return [p.strip() for p in parts if len(p.strip()) > 0]


def pick_def_sentence(term: str, sents: List[str]) -> str:
	term_l = term.lower()
	for s in sents:
		if term_l in s.lower():
			return s
	return sents[0] if sents else term


def build_glossary(ch_text: str, k: int = 20) -> List[Dict[str, str]]:
	kw = top_keywords(ch_text, k)
	sents = sentences(ch_text)
	gloss = []
	seen = set()
	for term in kw:
		if term in seen:
			continue
		definition = pick_def_sentence(term, sents)
		gloss.append({"term": term.title(), "definition": definition})
		seen.add(term)
	return gloss


def build_learning_objectives(ch_text: str, n: int = 10) -> List[str]:
	sents = sentences(ch_text)[:200]
	objs = []
	for s in sents:
		if len(objs) >= n:
			break
		# Heuristic: start with verbs or contain "understand", "explain", "describe"
		if re.match(r"^(Understand|Explain|Describe|Identify|Compare|Differentiate|Apply|Illustrate|Evaluate|Analyze)", s, re.IGNORECASE) or any(
			key in s.lower() for key in ["understand", "explain", "describe", "identify", "compare", "differentiate", "apply", "illustrate", "evaluate", "analyze"]
		):
			objs.append(s)
	if len(objs) < n:
		# backfill with first sentences
		for s in sents:
			if len(objs) >= n:
				break
			if s not in objs:
				objs.append("Understand: " + s)
	return objs[:n]


def build_concept_map(ch_text: str) -> List[Tuple[str, str]]:
	# Co-occurrence based simple edges between top terms
	kw = top_keywords(ch_text, 12)
	edges = []
	for i in range(len(kw) - 1):
		edges.append((kw[i].title(), kw[i + 1].title()))
	return edges


def build_mcqs_from_glossary(glossary: List[Dict[str, str]], count: int = 30) -> List[Dict[str, str]]:
	items = []
	defs = [g["definition"] for g in glossary]
	for i, g in enumerate(glossary):
		if len(items) >= count:
			break
		correct = g["definition"]
		# pick distractors
		distractors = []
		for d in defs:
			if d != correct and len(distractors) < 3:
				distractors.append(d)
		options = distractors + [correct]
		# ensure 4 options
		while len(options) < 4:
			options.append(options[-1])
		# shuffle deterministically by index
		order = [0, 1, 2, 3]
		rot = i % 4
		order = order[rot:] + order[:rot]
		opts_ordered = [options[j] for j in order]
		answer_idx = order.index(3)
		answer_letter = chr(ord('A') + answer_idx)
		items.append({
			"id": f"mcq_{i+1:03d}",
			"question_type": "mcq",
			"skill_id": g["term"],
			"prompt": f"Which of the following best describes: {g['term']}?",
			"options": opts_ordered,
			"answer": answer_letter,
			"rationale": f"{g['term']} is defined as: {correct}",
			"misconception_tags": ["definition_confusion"],
		})
	return items


def build_short_long_answers(ch_text: str, count: int = 10) -> List[Dict[str, str]]:
	sents = sentences(ch_text)
	qs = []
	for i in range(min(count, max(5, len(sents)//15))):
		q = f"Explain: {sents[i*5][:80]}..."
		ans = " ".join(sents[i*5:i*5+4])
		qs.append({"question": q, "answer": ans})
	return qs


def build_numericals_generic(ch_text: str, count: int = 10) -> List[Dict[str, str]]:
	# Generic numericals independent of chapter specifics
	items = []
	for i in range(count):
		items.append({
			"id": f"num_{i+1:02d}",
			"skill_id": "Problem Solving",
			"problem": f"If a quantity increases by {10+i}% from 100 units, what is the new value?",
			"solution_steps": [f"Increase = {(10+i)/100:.2f} * 100 = {10+i}", f"New value = 100 + {10+i} = {110+i}"],
			"answer": f"{110+i}",
		})
	return items


def build_activities(ch_title: str) -> str:
	topic = ch_title.split(":")[-1].strip() if ":" in ch_title else ch_title
	return (
		f"1) Inquiry on {topic}\n- Question: What are key variables affecting {topic.lower()}?\n- Method: Design a small investigation focusing on one variable.\n- Safety: Use protective gear and follow lab rules.\n\n"
		f"2) Data Collection on {topic}\n- Question: How does one factor influence outcomes in {topic.lower()}?\n- Method: Collect and chart observations over time.\n- Safety: Handle tools properly.\n\n"
		f"3) Application Project\n- Question: Apply {topic.lower()} concept in daily life.\n- Method: Build a simple model or demonstration.\n- Safety: Adult supervision for cutting/heating.\n"
	)


def build_misconceptions(ch_text: str) -> str:
	kw = top_keywords(ch_text, 5)
	lines = []
	for k in kw:
		lines.append(f"Misconception: {k.title()} always means more/better.\nCorrection: Context matters; optimize {k.lower()} rather than maximize it.\n")
	return "\n".join(lines)


def make_tests_from_mcqs(mcqs: List[Dict[str, str]]) -> Dict[str, List[str]]:
	ids = [q["id"] for q in mcqs]
	if len(ids) < 25:
		ids = (ids * 25)[:25]
	return {
		"tests": [
			{"id": "test1", "items": ids[:25]},
			{"id": "test2", "items": ids[:25]},
		]
	}


def write_chapter_dir(root: str, chapter_id: str, title: str, ch_text: str) -> None:
	os.makedirs(os.path.join(root, chapter_id), exist_ok=True)
	overview = ["# "+title, "", "Learning Objectives"] + ["- "+o for o in build_learning_objectives(ch_text)]
	concept_edges = build_concept_map(ch_text)
	overview += ["", "Concept Map"] + [f"- {a} -> {b}" for a,b in concept_edges]
	overview += ["", "Summary", sentences(ch_text)[0] if sentences(ch_text) else ""]
	with open(os.path.join(root, chapter_id, "overview.md"), "w", encoding="utf-8") as f:
		f.write("\n".join(overview))
	with open(os.path.join(root, chapter_id, "exposition.md"), "w", encoding="utf-8") as f:
		f.write(ch_text)
	gloss = build_glossary(ch_text, 25)
	with open(os.path.join(root, chapter_id, "glossary.json"), "w", encoding="utf-8") as f:
		json.dump(gloss, f, ensure_ascii=False, indent=2)
	mcqs = build_mcqs_from_glossary(gloss, 30)
	with open(os.path.join(root, chapter_id, "questions.json"), "w", encoding="utf-8") as f:
		json.dump(mcqs, f, ensure_ascii=False, indent=2)
	nums = build_numericals_generic(ch_text, 10)
	with open(os.path.join(root, chapter_id, "numericals.json"), "w", encoding="utf-8") as f:
		json.dump(nums, f, ensure_ascii=False, indent=2)
	with open(os.path.join(root, chapter_id, "activities.md"), "w", encoding="utf-8") as f:
		f.write(build_activities(title))
	with open(os.path.join(root, chapter_id, "misconceptions.md"), "w", encoding="utf-8") as f:
		f.write(build_misconceptions(ch_text))
	shortlong = build_short_long_answers(ch_text, 10)
	with open(os.path.join(root, chapter_id, "short_long_answers.json"), "w", encoding="utf-8") as f:
		json.dump(shortlong, f, ensure_ascii=False, indent=2)
	tests = make_tests_from_mcqs(mcqs)
	with open(os.path.join(root, chapter_id, "tests.json"), "w", encoding="utf-8") as f:
		json.dump(tests, f, ensure_ascii=False, indent=2)