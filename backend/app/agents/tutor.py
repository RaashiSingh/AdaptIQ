from langchain_groq import ChatGroq
from app.core.config import settings
from app.rag.pipeline import rag_query

llm = ChatGroq(
    api_key=settings.GROQ_API_KEY,
    model_name="llama-3.3-70b-versatile",
    temperature=0.7
)

def tutor_agent(state: dict) -> dict:
    print("[Tutor] Explaining concept...")

    user_id = state["user_id"]
    question = state["user_message"]

    history = state.get("chat_history", [])
    weak_areas = state.get("weak_areas", [])
    current_topic = state.get("current_topic")

    search_query = question

    if current_topic:
        search_query = f"{current_topic} {question}"

    result = rag_query(search_query, user_id)

    base_answer = result["answer"]
    sources = result.get("sources", [])

    history_text = ""

    if history:
        last_turns = history[-6:]

        history_text = "\n".join([
            f"{m['role'].upper()}: {m['content'][:200]}"
            for m in last_turns
        ])

    weak_text = ""

    if weak_areas:
        weak_text = (
            f"\nStudent previously struggled with: "
            f"{', '.join(weak_areas[:3])}"
        )
    prompt = f"""
You are AdaptIQ, a patient and encouraging AI tutor.

CURRENT STUDY TOPIC:
{current_topic}

PREVIOUS CONVERSATION:
{history_text}

STUDY MATERIAL:
{base_answer}

{weak_text}

IMPORTANT RULES:
1. Answer ONLY using the study material provided.
2. Stay focused on the CURRENT STUDY TOPIC.
3. Do NOT introduce unrelated topics.
4. If the answer is not found in the material, say:
   "I couldn't find that in the uploaded material."
5. Explain concepts in simple language.
6. Use examples if helpful.
7. End with ONE short follow-up question.

Student Question:
{question}

Provide a clear tutoring response.
"""

    response = llm.invoke(prompt)

    answer = response.content

    if sources:
        answer += f"\n\n📖 Based on: {', '.join(sources)}"

    state["final_response"] = answer

    state["chat_history"] = history + [
        {
            "role": "user",
            "content": question
        },
        {
            "role": "assistant",
            "content": answer
        }
    ]

    
    state["current_topic"] = current_topic

    state["next_agent"] = "end"

    return state