from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.agent import StudentEnrollmentAssistant

app = FastAPI(title="Student Enrollment Assistant")
assistant = StudentEnrollmentAssistant()


class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"


@app.get("/health")
def health():
    return {"status": "ok", "service": "student-enrollment-assistant"}


@app.post("/chat")
def chat(request: ChatRequest):
    try:
        response = assistant.handle_message(request.message, request.session_id)
        return {"response": response, "session_id": request.session_id}
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.get("/conversation")
def conversation(session_id: str = "default"):
    return {"session_id": session_id, "history": assistant.session.get(session_id, {}).history}


@app.get("/applicants/{applicant_id}")
def applicant_status(applicant_id: str):
    try:
        return assistant.check_application_status(applicant_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.get("/programs/{program_name}")
def program_info(program_name: str):
    try:
        return assistant.get_program_info(program_name)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
