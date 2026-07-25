from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from typing import Optional, List
from app.agents.graph import run_agent
import json

router = APIRouter()

user_sessions = {}

class ChatRequest(BaseModel):
    user_id: str
    message: str

class SessionState(BaseModel):
    chat_history: List[dict] = []
    study_plan: Optional[List[dict]] = None
    current_topic: Optional[str] = None
    weak_areas: List[str] = []
    quiz_in_progress: bool = False
    current_quiz: Optional[dict] = None
    quiz_answers: List[dict] = []

    # NEW
    quiz_scores: List[dict] = []
    latest_quiz_score: Optional[float] = None
    topics_covered: List[str] = []
    total_sessions: int = 0
    streak_days: int = 1


def get_session(user_id: str) -> dict:
    if user_id not in user_sessions:
        user_sessions[user_id] = {
            "chat_history": [],
            "study_plan": None,
            "current_topic": None,
            "weak_areas": [],
            "quiz_in_progress": False,
            "current_quiz": None,
            "quiz_answers": [],

            
            "quiz_scores": [],
            "latest_quiz_score": None,
            "topics_covered": [],
            "total_sessions": 0,
            "streak_days": 1
        }

    return user_sessions[user_id]


def update_session(user_id: str, result: dict):
    session = get_session(user_id)

    print("\n========== UPDATE SESSION ==========")
    print("quiz_in_progress:", result.get("quiz_in_progress"))
    print("current_quiz exists:", result.get("current_quiz") is not None)

    if result.get("current_quiz"):
        print(
            "questions saved:",
            len(result["current_quiz"].get("questions", []))
        )

    session["chat_history"] = result.get(
        "chat_history",
        session["chat_history"]
    )

    session["study_plan"] = result.get(
        "study_plan",
        session["study_plan"]
    )

    session["current_topic"] = result.get(
        "current_topic",
        session["current_topic"]
    )

    session["weak_areas"] = result.get(
        "weak_areas",
        session["weak_areas"]
    )

    session["quiz_in_progress"] = result.get(
        "quiz_in_progress",
        False
    )

    session["current_quiz"] = result.get(
        "current_quiz",
        None
    )

    session["quiz_answers"] = result.get(
        "quiz_answers",
        []
    )

    
    quiz_score = result.get("quiz_score")

    if quiz_score is not None:

        session["latest_quiz_score"] = quiz_score

        topic = result.get("current_topic") or "General"

        session["quiz_scores"].append({
            "topic": topic,
            "score": quiz_score
        })

        if topic not in session["topics_covered"]:
            session["topics_covered"].append(topic)

        session["total_sessions"] += 1


@router.post("/message")
def send_message(req: ChatRequest):

    session = get_session(req.user_id)

    print("\n========== BEFORE RUN_AGENT ==========")
    print("user:", req.user_id)
    print("message:", req.message)
    print("quiz_in_progress:", session["quiz_in_progress"])
    print("current_quiz exists:", session["current_quiz"] is not None)

    if session["current_quiz"]:
        print(
            "questions:",
            len(session["current_quiz"].get("questions", []))
        )

    result = run_agent(
        user_id=req.user_id,
        message=req.message,
        chat_history=session["chat_history"],
        study_plan=session["study_plan"],
        current_topic=session["current_topic"],
        weak_areas=session["weak_areas"],
        quiz_in_progress=session["quiz_in_progress"],
        current_quiz=session["current_quiz"],
        quiz_answers=session["quiz_answers"]
    )

    update_session(req.user_id, result)

    return {
        "response": result.get("final_response", "I didn't understand that."),
        "quiz_in_progress": result.get("quiz_in_progress", False),
        "quiz_score": result.get("quiz_score"),
        "weak_areas": result.get("weak_areas", []),
        "current_topic": result.get("current_topic")
    }


@router.get("/session/{user_id}")
def get_session_info(user_id: str):

    session = get_session(user_id)

    return {
        "user_id": user_id,
        "chat_history_length": len(session["chat_history"]),
        "current_topic": session["current_topic"],
        "weak_areas": session["weak_areas"],
        "quiz_in_progress": session["quiz_in_progress"],
        "has_study_plan": session["study_plan"] is not None,

        # NEW
        "quiz_scores": session["quiz_scores"],
        "latest_quiz_score": session["latest_quiz_score"],
        "topics_covered": session["topics_covered"],
        "total_sessions": session["total_sessions"],
        "streak_days": session["streak_days"]
    }


@router.delete("/session/{user_id}")
def clear_session(user_id: str):
    if user_id in user_sessions:
        del user_sessions[user_id]

    return {"message": f"Session cleared for {user_id}"}


@router.websocket("/ws/{user_id}")
async def chat_websocket(websocket: WebSocket, user_id: str):

    await websocket.accept()
    print(f"[WS] User {user_id} connected")

    try:

        while True:

            message = await websocket.receive_text()

            session = get_session(user_id)

            result = run_agent(
                user_id=user_id,
                message=message,
                chat_history=session["chat_history"],
                study_plan=session["study_plan"],
                current_topic=session["current_topic"],
                weak_areas=session["weak_areas"],
                quiz_in_progress=session["quiz_in_progress"],
                current_quiz=session["current_quiz"],
                quiz_answers=session["quiz_answers"]
            )

            update_session(user_id, result)

            response = result.get(
                "final_response",
                "I didn't understand that."
            )

            await websocket.send_text(response)

    except WebSocketDisconnect:
        print(f"[WS] User {user_id} disconnected")