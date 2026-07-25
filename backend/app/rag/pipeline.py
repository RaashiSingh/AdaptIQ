from groq import Groq
from app.rag.ingestor import ingest_file
from app.rag.retriever import store_nodes, retrieve_relevant_chunks
from app.core.config import settings
import json

groq_client = Groq(api_key=settings.GROQ_API_KEY)


def process_uploaded_file(filename: str, user_id: str) -> dict:
    print(f"[Pipeline] Starting ingestion for {filename}...")
    nodes = ingest_file(filename)
    count = store_nodes(nodes, user_id, filename)

    return {
        "filename": filename,
        "chunks_stored": count,
        "status": "ready"
    }


def rag_query(question: str, user_id: str) -> dict:
    print(f"[Pipeline] RAG query from user {user_id}: {question[:60]}...")

    chunks = retrieve_relevant_chunks(
        question,
        user_id,
        top_k=5
    )

    if not chunks:
        return {
            "answer": "I couldn't find relevant information in your uploaded documents. Please upload study material first.",
            "sources": [],
            "context_used": False
        }

    context = "\n\n---\n\n".join(
        [
            f"Source: {c['source']}\n{c['text']}"
            for c in chunks
        ]
    )

    prompt = f"""
You are AdaptIQ, a personalized AI tutor.

CONTEXT:
{context}

QUESTION:
{question}

Instructions:
- Use the provided context.
- Answer clearly and accurately.
- Use numbered points if appropriate.
- If the context is incomplete, mention that and use general knowledge.
- End with a short follow-up question.
"""

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful AI tutor."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7,
        max_tokens=1024
    )

    answer = response.choices[0].message.content

    sources = list(
        set(
            [c["source"] for c in chunks]
        )
    )

    return {
        "answer": answer,
        "sources": sources,
        "context_used": True,
        "chunks_retrieved": len(chunks)
    }


def generate_quiz(
    topic: str,
    user_id: str,
    num_questions: int = 5
) -> dict:

    chunks = retrieve_relevant_chunks(
        topic,
        user_id,
        top_k=8
    )

    if not chunks:
        return {
            "error": "No study material found. Please upload documents first."
        }

    context = "\n\n".join(
        [c["text"] for c in chunks]
    )

    prompt = f"""
You are an expert educational assessment generator.

Based ONLY on the study material below, generate EXACTLY {num_questions} multiple-choice questions.

STUDY MATERIAL:
{context}

IMPORTANT RULES:
1. Generate EXACTLY {num_questions} questions.
2. The "questions" array MUST contain EXACTLY {num_questions} objects.
3. Every question must have 4 options.
4. Options must start with A), B), C), D).
5. Each question must have exactly one correct answer.
6. The correct answer field must contain only A, B, C, or D.
7. Include a short explanation.
8. Return ONLY valid JSON.
9. Do NOT include markdown.
10. Do NOT include ```json blocks.

Return JSON in this format:

{{
  "questions": [
    {{
      "question": "Question 1",
      "options": [
        "A) Option A",
        "B) Option B",
        "C) Option C",
        "D) Option D"
      ],
      "correct": "A",
      "explanation": "Short explanation"
    }},
    {{
      "question": "Question 2",
      "options": [
        "A) Option A",
        "B) Option B",
        "C) Option C",
        "D) Option D"
      ],
      "correct": "B",
      "explanation": "Short explanation"
    }}
  ]
}}
"""

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You generate educational quizzes and return only valid JSON."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
        max_tokens=4096
    )

    raw = response.choices[0].message.content.strip()

    raw = raw.replace("```json", "")
    raw = raw.replace("```", "")
    raw = raw.strip()

    try:
        quiz_data = json.loads(raw)

        questions = quiz_data.get("questions", [])

        print(f"[DEBUG] Quiz generated: {len(questions)} questions")

        if len(questions) == 0:
            return {
                "error": "No questions were generated."
            }

        return {
            "topic": topic,
            "quiz": quiz_data
        }

    except json.JSONDecodeError:
        print("[DEBUG] Failed to parse quiz JSON")
        print(raw)

        return {
            "topic": topic,
            "raw_quiz": raw,
            "error": "Could not parse quiz JSON"
        }