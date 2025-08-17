from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from .routers import study, gamify, teacher, students
from .db import init_engine_and_session
from .models import Base
from .routers import upload

app = FastAPI(title="Gamified Agentic AI Tutor - Class 8 Science")

# Mount static UI
app.mount("/ui/student", StaticFiles(directory="/workspace/ui/student", html=True), name="student_ui")
app.mount("/ui/teacher", StaticFiles(directory="/workspace/ui/teacher", html=True), name="teacher_ui")

# Initialize DB engine and create tables
engine = init_engine_and_session()
Base.metadata.create_all(engine)

# Routers
app.include_router(students.router, prefix="/api/students", tags=["students"])
app.include_router(study.router, prefix="/api/study", tags=["study"])
app.include_router(gamify.router, prefix="/api/gamify", tags=["gamification"])
app.include_router(teacher.router, prefix="/api/teacher", tags=["teacher"]) 
app.include_router(upload.router, prefix="/api/upload", tags=["upload"]) 


@app.get("/", response_class=HTMLResponse)
async def root():
	return """
	<!doctype html>
	<html>
	<head><title>Class 8 Tutor</title></head>
	<body>
		<h2>Gamified Agentic AI Tutor - Class 8 Science</h2>
		<ul>
			<li><a href="/ui/student/">Student App</a></li>
			<li><a href="/ui/teacher/">Teacher Dashboard</a></li>
		</ul>
	</body>
	</html>
	"""