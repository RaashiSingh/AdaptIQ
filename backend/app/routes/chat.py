from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from groq import Groq
from app.core.config import settings

router = APIRouter()
client = Groq(api_key=settings.GROQ_API_KEY)

SYSTEM_PROMPT = """You are AdaptIQ, a personalized AI tutor.
Your job is to:
1. Explain concepts clearly based on the student's uploaded study material
2. Ask follow-up questions to check understanding
3. Generate quizzes when the student asks
4. Track weak areas and revisit them
Always be encouraging, clear, and structured in your responses."""

@router.websocket("/ws/{user_id}")
async def chat_websocket(websocket: WebSocket, user_id: str):
    await websocket.accept()
    history = []
    print(f"User {user_id} connected")
    try:
        while True:
            message = await websocket.receive_text()
            history.append({"role": "user", "content": message})

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    *history[-20:]
                ]
            )
            reply = response.choices[0].message.content
            history.append({"role": "assistant", "content": reply})
            await websocket.send_text(reply)

    except WebSocketDisconnect:
        print(f"User {user_id} disconnected")

@router.post("/message")
async def send_message(user_id: str, message: str):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": message}
        ]
    )
    return {"reply": response.choices[0].message.content}