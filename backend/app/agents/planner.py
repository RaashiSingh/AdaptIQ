from langchain_groq import ChatGroq
from app.core.config import settings
from app.rag.retriever import retrieve_relevant_chunks
import json

llm = ChatGroq(
    api_key=settings.GROQ_API_KEY,
    model_name="llama-3.3-70b-versatile",
    temperature=0.5
)

def planner_agent(state: dict) -> dict:
    print("[Planner] Building study plan...")
    user_id = state["user_id"]

    chunks = retrieve_relevant_chunks(
        "main topics key concepts overview",
        user_id,
        top_k=10
    )

    if not chunks:
        state["final_response"] = (
            "I don't see any uploaded study material yet. "
            "Please upload your notes or textbook PDF first, "
            "then I'll build a personalized study plan for you!"
        )
        state["next_agent"] = "end"
        return state

    context = "\n\n".join([c["text"] for c in chunks])

    prompt = f"""You are a study planner. Based on the following study material, create a structured study plan.

STUDY MATERIAL:
{context}

Create a study plan in this exact JSON format:
{{
  "title": "Study Plan Title",
  "estimated_hours": 10,
  "topics": [
    {{
      "order": 1,
      "topic": "Topic Name",
      "description": "What this covers",
      "estimated_minutes": 45,
      "difficulty": "beginner|intermediate|advanced"
    }}
  ],
  "recommendation": "One sentence advice for the student"
}}

Return only the JSON, nothing else."""

    response = llm.invoke(prompt)
    raw = response.content.strip().replace("```json", "").replace("```", "").strip()

    try:
        plan = json.loads(raw)
        state["study_plan"] = plan.get("topics", [])

        if plan.get("topics"):
            state["current_topic"] = plan["topics"][0]["topic"]

        readable = f"📚 **Your Personalized Study Plan**\n\n"
        readable += f"**{plan.get('title', 'Study Plan')}**\n"
        readable += f"Estimated time: {plan.get('estimated_hours', '?')} hours\n\n"

        for t in plan.get("topics", []):
            readable += f"{t['order']}. **{t['topic']}** ({t['estimated_minutes']} min) — {t['difficulty']}\n"
            readable += f"   {t['description']}\n\n"

        readable += f"\n💡 {plan.get('recommendation', '')}"
        readable += f"\n\nReady to start? Just ask me about any topic and I'll explain it!"

        state["final_response"] = readable

    except json.JSONDecodeError:
        state["final_response"] = f"Here's your study plan:\n\n{raw}"

    state["next_agent"] = "end"
    return state