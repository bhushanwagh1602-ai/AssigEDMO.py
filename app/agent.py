from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Any, List
import re


PROGRAMS = {
    "computer science": {
        "name": "Computer Science",
        "degree": "BSc",
        "duration": "4 years",
        "tuition_fee": "$12,500/year",
        "requirements": ["High school diploma", "Math", "English"],
        "application_deadline": "2026-08-31",
        "document_submission_deadline": "2026-08-25",
        "decision_notification_date": "2026-09-20",
    },
    "data science": {
        "name": "Data Science",
        "degree": "BSc",
        "duration": "4 years",
        "tuition_fee": "$13,200/year",
        "requirements": ["High school diploma", "Math", "Statistics"],
        "application_deadline": "2026-09-15",
        "document_submission_deadline": "2026-09-08",
        "decision_notification_date": "2026-09-30",
    },
    "business analytics": {
        "name": "Business Analytics",
        "degree": "BBA",
        "duration": "3 years",
        "tuition_fee": "$10,800/year",
        "requirements": ["High school diploma", "English", "Math"],
        "application_deadline": "2026-09-10",
        "document_submission_deadline": "2026-09-03",
        "decision_notification_date": "2026-09-25",
    },
}

APPLICATIONS = {
    "APP-1042": {
        "applicant_id": "APP-1042",
        "applicant_name": "Jordan Smith",
        "program": "Computer Science",
        "status": "Under Review",
        "next_step": "Admissions is currently reviewing your transcript and ID documents.",
        "missing_documents": ["Transcript", "Government ID"],
    },
    "APP-2049": {
        "applicant_id": "APP-2049",
        "applicant_name": "Rina Patel",
        "program": "Data Science",
        "status": "Accepted",
        "next_step": "Please complete the enrollment confirmation form.",
        "missing_documents": [],
    },
    "APP-3105": {
        "applicant_id": "APP-3105",
        "applicant_name": "Marcus Chen",
        "program": "Business Analytics",
        "status": "Documents Pending",
        "next_step": "Please upload your final transcript before the document deadline.",
        "missing_documents": ["Final Transcript"],
    },
}


@dataclass
class AssistantSession:
    history: List[str] = field(default_factory=list)
    current_program: str | None = None
    applicant_id: str | None = None
    last_intent: str | None = None


class StudentEnrollmentAssistant:
    def __init__(self):
        self.session: Dict[str, AssistantSession] = {}

    def _get_session(self, session_id: str) -> AssistantSession:
        if session_id not in self.session:
            self.session[session_id] = AssistantSession()
        return self.session[session_id]

    def _match_program_name(self, message: str) -> str | None:
        lower = message.lower()
        for key in PROGRAMS:
            if key in lower:
                return PROGRAMS[key]["name"]
        return None

    def get_program_info(self, program_name: str) -> Dict[str, Any]:
        normalized = program_name.strip().lower()
        match = None
        for key, value in PROGRAMS.items():
            if normalized in key or normalized == value["name"].lower():
                match = key
                break
        if not match:
            raise ValueError(f"Program '{program_name}' not found.")

        program = PROGRAMS[match]
        return {
            "program_name": program["name"],
            "degree": program["degree"],
            "duration": program["duration"],
            "tuition_fee": program["tuition_fee"],
            "requirements": program["requirements"],
            "application_deadline": program["application_deadline"],
            "document_submission_deadline": program["document_submission_deadline"],
            "decision_notification_date": program["decision_notification_date"],
        }

    def check_application_status(self, applicant_id: str) -> Dict[str, Any]:
        app = APPLICATIONS.get(applicant_id.strip().upper())
        if not app:
            raise ValueError(f"Applicant '{applicant_id}' not found.")

        return {
            "applicant_id": app["applicant_id"],
            "applicant_name": app["applicant_name"],
            "program_applied_to": app["program"],
            "status": app["status"],
            "next_step": app["next_step"],
            "missing_documents": app["missing_documents"],
        }

    def get_deadlines(self, program_name: str) -> Dict[str, Any]:
        program = self.get_program_info(program_name)
        return {
            "program_name": program["program_name"],
            "application_deadline": program["application_deadline"],
            "document_submission_deadline": program["document_submission_deadline"],
            "decision_notification_date": program["decision_notification_date"],
        }

    def handle_message(self, message: str, session_id: str = "default") -> str:
        session = self._get_session(session_id)
        text = message.strip()
        session.history.append(text)
        lower = text.lower()

        applicant_match = re.search(r"\bAPP-\d+\b", text, re.IGNORECASE)
        if applicant_match:
            session.applicant_id = applicant_match.group(0).upper()

        program_name = self._match_program_name(lower)
        if program_name:
            session.current_program = program_name

        if any(word in lower for word in ["hello", "hi", "hey"]) and not (
            "program" in lower or "offer" in lower or "computer science" in lower or "data science" in lower or "business analytics" in lower
        ):
            return "Hello! I can help with program information, applicant status, deadlines, and document requirements."

        if "program" in lower or "offer" in lower or "computer science" in lower or "data science" in lower or "business analytics" in lower:
            if program_name:
                info = self.get_program_info(program_name)
                session.last_intent = "program_info"
                return (
                    f"{info['program_name']} is a {info['degree']} program lasting {info['duration']}. "
                    f"Tuition is {info['tuition_fee']} and the prerequisites are {', '.join(info['requirements'])}."
                )
            return "We offer Computer Science, Data Science, and Business Analytics. Which program would you like to know more about?"

        if "deadline" in lower:
            if session.current_program:
                deadline_info = self.get_deadlines(session.current_program)
                session.last_intent = "deadline"
                return (
                    f"The application deadline for {deadline_info['program_name']} is {deadline_info['application_deadline']}. "
                    f"Document submission closes on {deadline_info['document_submission_deadline']} and decisions are sent by {deadline_info['decision_notification_date']}."
                )
            if program_name:
                deadline_info = self.get_deadlines(program_name)
                return (
                    f"The application deadline for {deadline_info['program_name']} is {deadline_info['application_deadline']}."
                )
            return "The application deadlines are: Computer Science — 2026-08-31, Data Science — 2026-09-15, Business Analytics — 2026-09-10."

        if "status" in lower or "applied" in lower:
            if applicant_match:
                status = self.check_application_status(applicant_match.group(0))
                session.last_intent = "status"
                return (
                    f"{status['applicant_name']} is currently {status['status']} for {status['program_applied_to']}. "
                    f"{status['next_step']}"
                )
            if session.applicant_id:
                status = self.check_application_status(session.applicant_id)
                return (
                    f"{status['applicant_name']} is currently {status['status']} for {status['program_applied_to']}. "
                    f"{status['next_step']}"
                )
            return "I can check your status once you share your applicant ID, such as APP-1042."

        if "fee waiver" in lower or "waiver" in lower:
            return "I'd recommend speaking with an enrollment counselor for that. Would you like me to connect you?"

        if "document" in lower or "submit" in lower or "still need" in lower:
            if session.applicant_id:
                status = self.check_application_status(session.applicant_id)
                missing = status["missing_documents"]
                if missing:
                    return f"You still need to submit: {', '.join(missing)}."
                return "You have submitted all required documents for your application."
            return "I can check your document checklist once you share your applicant ID."

        if "escalate" in lower or "counselor" in lower or "connect" in lower:
            return "I'd recommend speaking with an enrollment counselor for that. Would you like me to connect you?"

        return "I can help with program information, applicant status, deadlines, and document requirements."


StudentAdmissionsAssistant = StudentEnrollmentAssistant
