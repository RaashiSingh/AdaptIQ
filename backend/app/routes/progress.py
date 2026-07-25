from fastapi import APIRouter

router = APIRouter()

mock_progress = {
    "topics_covered": ["Photosynthesis", "Cell Division", "DNA Replication"],
    "quiz_scores": [
        {"topic": "Photosynthesis", "score": 80, "date": "2024-01-10"},
        {"topic": "Cell Division", "score": 65, "date": "2024-01-11"},
    ],
    "weak_areas": ["Mitosis phases", "Calvin cycle"],
    "total_sessions": 5,
    "streak_days": 3
}

@router.get("/{user_id}")
def get_progress(user_id: str):
    return {"user_id": user_id, **mock_progress}

@router.get("/{user_id}/weak-areas")
def get_weak_areas(user_id: str):
    return {"user_id": user_id, "weak_areas": mock_progress["weak_areas"]}