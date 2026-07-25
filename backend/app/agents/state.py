from typing import TypedDict, List, Optional, Literal

class AgentState(TypedDict):
    # Student info
    user_id: str
    user_message: str

    # Conversation
    chat_history: List[dict]

    # Study plan
    study_plan: Optional[List[dict]]
    current_topic: Optional[str]

    # Quiz state
    current_quiz: Optional[dict]
    quiz_answers: Optional[List[dict]]
    quiz_score: Optional[float]

    # Weak areas tracked over time
    weak_areas: Optional[List[str]]

    # Which agent should handle this turn
    next_agent: Optional[Literal["planner", "tutor", "assessor", "evaluator", "end"]]

    # Final response to send back to student
    final_response: Optional[str]

    # Internal flags
    documents_available: bool
    needs_quiz: bool
    quiz_in_progress: bool