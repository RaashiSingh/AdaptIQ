from langgraph.graph import StateGraph, END
from app.agents.state import AgentState
from app.agents.planner import planner_agent
from app.agents.tutor import tutor_agent
from app.agents.assessor import assessor_agent, handle_quiz_answer
from app.agents.evaluator import evaluator_agent

def router(state: AgentState) -> str:
    message = state["user_message"].lower().strip()

    if state.get("next_agent") == "evaluator":
        return "evaluator"

    if state.get("quiz_in_progress"):
        if message in ["a", "b", "c", "d"]:
            return "assessor_answer"

    plan_triggers = ["study plan", "plan", "what should i study", "where do i start", "syllabus", "schedule"]
    if any(t in message for t in plan_triggers):
        return "planner"

    quiz_triggers = ["quiz", "test me", "test my", "questions on", "mcq", "assess"]
    if any(t in message for t in quiz_triggers):
        return "assessor"

    return "tutor"

def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("planner",        planner_agent)
    graph.add_node("tutor",          tutor_agent)
    graph.add_node("assessor",       assessor_agent)
    graph.add_node("assessor_answer",handle_quiz_answer)
    graph.add_node("evaluator",      evaluator_agent)

    graph.set_conditional_entry_point(
        router,
        {
            "planner":         "planner",
            "tutor":           "tutor",
            "assessor":        "assessor",
            "assessor_answer": "assessor_answer",
            "evaluator":       "evaluator",
        }
    )

    graph.add_edge("planner",         END)
    graph.add_edge("tutor",           END)
    graph.add_edge("assessor",        END)
    graph.add_conditional_edges(
    "assessor_answer",
    lambda state: state.get("next_agent", "end"),
    {
        "evaluator": "evaluator",
        "end": END
    }
)
    graph.add_edge("evaluator",       END)

    return graph.compile()

adaptiq_graph = build_graph()

def run_agent(
    user_id: str,
    message: str,
    chat_history: list = None,
    study_plan: list = None,
    current_topic: str = None,
    weak_areas: list = None,
    quiz_in_progress: bool = False,
    current_quiz: dict = None,
    quiz_answers: list = None
) -> dict:

    state = AgentState(
        user_id=user_id,
        user_message=message,
        chat_history=chat_history or [],
        study_plan=study_plan,
        current_topic=current_topic,
        weak_areas=weak_areas or [],
        quiz_in_progress=quiz_in_progress,
        current_quiz=current_quiz,
        quiz_answers=quiz_answers or [],
        quiz_score=None,
        next_agent=None,
        final_response=None,
        documents_available=True,
        needs_quiz=False
    )

    result = adaptiq_graph.invoke(state)
    return result