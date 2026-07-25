from langchain_groq import ChatGroq
from app.core.config import settings

llm = ChatGroq(
    api_key=settings.GROQ_API_KEY,
    model_name="llama-3.3-70b-versatile",
    temperature=0.3
)

def evaluator_agent(state: dict) -> dict:
    print("[Evaluator] Evaluating quiz results...")
    answers = state.get("quiz_answers", [])

    if not answers:
        state["final_response"] = "No quiz answers to evaluate yet."
        state["next_agent"] = "end"
        return state

    correct = sum(1 for a in answers if a["is_correct"])
    total = len(answers)
    score = round((correct / total) * 100, 1)
    state["quiz_score"] = score

    wrong_answers = [a for a in answers if not a["is_correct"]]
    weak_areas = state.get("weak_areas", [])

    for a in wrong_answers:
        topic_hint = a["question"][:60]
        if topic_hint not in weak_areas:
            weak_areas.append(topic_hint)

    state["weak_areas"] = weak_areas[:10]

    answers_summary = "\n".join([
        f"Q: {a['question'][:80]}\nStudent answered: {a['user_answer']} | Correct: {a['correct_answer']} | {'✓' if a['is_correct'] else '✗'}"
        for a in answers
    ])

    prompt = f"""A student just completed a quiz. Analyze their performance and give personalized feedback.

QUIZ RESULTS:
Score: {score}% ({correct}/{total} correct)

DETAILED ANSWERS:
{answers_summary}

Write a short, encouraging feedback message (under 200 words) that:
1. Acknowledges their score with appropriate encouragement
2. Points out 1-2 specific weak areas they should review
3. Suggests what to study next
4. Ends with a motivational line

Be warm and supportive, not harsh."""

    response = llm.invoke(prompt)
    feedback = response.content

    emoji = "🏆" if score >= 80 else "📈" if score >= 60 else "💪"

    final = f"{emoji} **Quiz Complete!**\n\n"
    final += f"**Score: {score}% ({correct}/{total} correct)**\n\n"
    final += feedback

    if weak_areas:
        final += f"\n\n📌 **Topics to review:** {', '.join(weak_areas[:3])}"

    state["final_response"] = final
    state["quiz_answers"] = []
    state["current_quiz"] = None
    state["next_agent"] = "end"
    return state