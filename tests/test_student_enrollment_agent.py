from app.agent import StudentEnrollmentAssistant


def test_get_program_info_returns_program_details():
    agent = StudentEnrollmentAssistant()
    result = agent.get_program_info("Computer Science")

    assert result["program_name"] == "Computer Science"
    assert result["degree"] == "BSc"
    assert result["application_deadline"] == "2026-08-31"


def test_check_application_status_returns_status():
    agent = StudentEnrollmentAssistant()
    result = agent.check_application_status("APP-1042")

    assert result["status"] == "Under Review"
    assert "Government ID" in result["missing_documents"]


def test_get_deadlines_returns_dates():
    agent = StudentEnrollmentAssistant()
    result = agent.get_deadlines("Business Analytics")

    assert result["application_deadline"] == "2026-09-10"
    assert result["decision_notification_date"] == "2026-09-25"


def test_handle_message_responds_to_program_query():
    agent = StudentEnrollmentAssistant()
    response = agent.handle_message("Hi, what programs do you offer in computer science?")

    assert "Computer Science" in response
    assert "Math" in response


def test_5_turn_conversation_flow():
    agent = StudentEnrollmentAssistant()
    session_id = "demo-session"

    turn1 = agent.handle_message("Hi, what programs do you offer in computer science?", session_id)
    turn2 = agent.handle_message("What's the application deadline for that?", session_id)
    turn3 = agent.handle_message("I already applied. My ID is APP-1042. What's my status?", session_id)
    turn4 = agent.handle_message("Can I get a fee waiver?", session_id)
    turn5 = agent.handle_message("What documents do I still need to submit?", session_id)

    assert "Computer Science" in turn1
    assert "2026-08-31" in turn2
    assert "Under Review" in turn3
    assert "enrollment counselor" in turn4.lower()
    assert "Transcript" in turn5 or "Government ID" in turn5



#to run the server, use the following command in your terminal:
'''
 cd "c:\Users\ShreeS\.vscode\EDMOAssig.py"
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8001

'''