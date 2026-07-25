from fastapi import APIRouter
from app.api.routes.chat import get_session

router = APIRouter()


@router.get("/{user_id}")
def get_progress(user_id: str):

    session = get_session(user_id)

    return {
        "user_id": user_id,
        "topics_covered": session["topics_covered"],
        "quiz_scores": session["quiz_scores"],
        "weak_areas": session["weak_areas"],
        "total_sessions": session["total_sessions"],
        "streak_days": session["streak_days"]
    }


@router.get("/{user_id}/weak-areas")
def get_weak_areas(user_id: str):

    session = get_session(user_id)

    return {
        "user_id": user_id,
        "weak_areas": session["weak_areas"]
    }


@router.post("/{user_id}/quiz-score")
def save_quiz_score(user_id: str, topic: str, score: float):

    session = get_session(user_id)

    session["latest_quiz_score"] = score

    session["quiz_scores"].append({
        "topic": topic,
        "score": score
    })

    if topic not in session["topics_covered"]:
        session["topics_covered"].append(topic)

    session["total_sessions"] += 1

    return {
        "message": "Quiz score saved successfully.",
        "quiz_scores": session["quiz_scores"]
    }