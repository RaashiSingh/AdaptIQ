from langchain_groq import ChatGroq
from app.core.config import settings
from app.rag.pipeline import generate_quiz
import json

llm = ChatGroq(
    api_key=settings.GROQ_API_KEY,
    model_name="llama-3.3-70b-versatile",
    temperature=0.4
)

def assessor_agent(state: dict) -> dict:
    print("[Assessor] Generating quiz...")
    user_id = state["user_id"]
    message = state["user_message"].lower()
    current_topic = state.get("current_topic", "general concepts")

    topic = current_topic
    for word in ["quiz", "test", "questions", "assess", "on", "about"]:
        message = message.replace(word, "").strip()
    if message.strip():
        topic = message.strip()

    num_questions = 5
    if "3" in state["user_message"]:
        num_questions = 3
    elif "10" in state["user_message"]:
        num_questions = 10

    result = generate_quiz(topic, user_id, num_questions)

    if "error" in result:
        state["final_response"] = result["error"]
        state["next_agent"] = "end"
        return state

    quiz_data = result.get("quiz", {})
    questions = quiz_data.get("questions", [])

    state["current_quiz"] = {
        "topic": topic,
        "questions": questions,
        "current_question_index": 0
    }
    state["quiz_in_progress"] = True

    if not questions:
        state["final_response"] = "I couldn't generate a quiz from your study material. Try uploading more content."
        state["next_agent"] = "end"
        return state

    first_q = questions[0]
    response = f"🎯 **Quiz: {topic.title()}**\n\n"
    response += f"**Question 1 of {len(questions)}:**\n\n"
    response += f"{first_q['question']}\n\n"
    for option in first_q["options"]:
        response += f"{option}\n"
    response += f"\n*Type your answer (A, B, C, or D)*"

    state["final_response"] = response
    state["next_agent"] = "end"
    return state


def handle_quiz_answer(state: dict) -> dict:
    print("[Assessor] Checking quiz answer...")
    quiz = state.get("current_quiz", {})
    questions = quiz.get("questions", [])
    idx = quiz.get("current_question_index", 0)
    answers = state.get("quiz_answers", [])
    user_answer = state["user_message"].strip().upper()

    print("\n===== QUIZ DEBUG =====")
    print("questions length:", len(questions))
    print("current index:", idx)
    print("user answer:", user_answer)
    print("======================\n")

    if not questions or idx >= len(questions):
        state["quiz_in_progress"] = False
        state["next_agent"] = "evaluator"
        return state

    current_q = questions[idx]
    correct = current_q["correct"].upper()
    is_correct = user_answer == correct

    answers.append({
        "question": current_q["question"],
        "user_answer": user_answer,
        "correct_answer": correct,
        "is_correct": is_correct,
        "explanation": current_q.get("explanation", "")
    })
    state["quiz_answers"] = answers

    feedback = "✅ Correct!" if is_correct else f"❌ Incorrect. The answer was **{correct}**."
    feedback += f"\n{current_q.get('explanation', '')}\n\n"

    next_idx = idx + 1
    state["current_quiz"]["current_question_index"] = next_idx

    print("next_idx:", next_idx)
    print("len_questions:", len(questions))
    print("will_continue:", next_idx < len(questions))

    if next_idx < len(questions):
        next_q = questions[next_idx]
        feedback += f"**Question {next_idx + 1} of {len(questions)}:**\n\n"
        feedback += f"{next_q['question']}\n\n"
        for option in next_q["options"]:
            feedback += f"{option}\n"
        feedback += f"\n*Type your answer (A, B, C, or D)*"
        state["final_response"] = feedback
        state["next_agent"] = "end"
    else:
        state["quiz_in_progress"] = False
        state["final_response"] = feedback
        state["next_agent"] = "evaluator"

    return state