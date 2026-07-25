# AdaptIQ — Personalized AI Tutor

An agentic AI-powered learning platform that adapts to how students learn by generating personalized study plans, explaining concepts using uploaded notes, conducting adaptive quizzes, and tracking learning progress.

![AdaptIQ](https://img.shields.io/badge/AI-Agentic-indigo)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-green)
![Next.js](https://img.shields.io/badge/Frontend-Next.js-black)
![LangGraph](https://img.shields.io/badge/Agents-LangGraph-purple)

---

# What it does

AdaptIQ allows students to upload their notes or textbooks and receive AI-powered personalized learning assistance.

Features include:

- Upload PDF, DOCX and TXT study materials
- Personalized study plan generation
- Context-aware explanations using Retrieval Augmented Generation (RAG)
- Adaptive quiz generation
- Automatic quiz evaluation
- Weak area identification
- Learning progress tracking
- Multi-agent workflow using LangGraph

---

# Architecture

```
Student
    │
    ▼
Next.js Frontend
    │
    ▼
FastAPI Backend
    │
    ▼
LangGraph Agent Orchestrator
    ├── Planner Agent → Builds study plans
    ├── Tutor Agent → Explains concepts using RAG
    ├── Assessor Agent → Generates quizzes
    └── Evaluator Agent → Scores answers & identifies weak areas
    │
    ▼
RAG Pipeline (LlamaIndex)
    ├── Document Parser
    ├── Embedding Model (BAAI/bge-small-en-v1.5)
    ├── Qdrant Vector Database
    └── Groq LLM (Llama 3 70B)
```

---

# Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | Next.js 14, React, Tailwind CSS, Recharts |
| Backend | FastAPI, Python 3.11 |
| AI Agents | LangGraph, LangChain |
| RAG | LlamaIndex |
| Embeddings | BAAI/bge-small-en-v1.5 |
| Vector Database | Qdrant |
| LLM | Groq (Llama 3 70B) |
| Authentication | Supabase |
| Deployment | Railway (Backend), Vercel (Frontend) |

---

# Local Setup

## Prerequisites

- Python 3.11+
- Node.js 18+
- Docker Desktop

---

## Backend Setup

```bash
cd backend

python -m venv venv

# Windows
venv\Scripts\activate

pip install -r requirements.txt
```

Create a `.env` file inside the **backend** folder.

```env
GROQ_API_KEY=your_key
SUPABASE_URL=your_url
SUPABASE_KEY=your_key
DATABASE_URL=your_database_url
SECRET_KEY=your_secret_key
QDRANT_HOST=localhost
QDRANT_PORT=6333
```

Start the backend server.

```bash
uvicorn app.main:app --reload
```

---

## Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

Open:

```
http://localhost:3000
```

---

## Qdrant

Run Qdrant using Docker.

```bash
docker run -d \
-p 6333:6333 \
--name qdrant_local \
qdrant/qdrant
```

Dashboard:

```
http://localhost:6333/dashboard
```

---

# Usage

1. Upload your study notes.
2. Wait for document processing.
3. Ask questions related to your uploaded material.
4. Generate personalized study plans.
5. Take adaptive quizzes.
6. Review quiz scores and weak areas from the Progress Dashboard.

---

# Project Structure

```
adaptiq/
│
├── backend/
│   ├── app/
│   │   ├── agents/
│   │   ├── rag/
│   │   ├── api/
│   │   ├── models/
│   │   ├── core/
│   │   └── main.py
│   │
│   ├── uploads/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── app/
│   ├── components/
│   ├── lib/
│   ├── public/
│   └── package.json
│
├── docker-compose.yml
├── README.md
└── requirements.txt
```

---

# Current Features

- Document Upload
- PDF Parsing
- RAG-based Question Answering
- Personalized Study Plans
- Adaptive Quiz Generation
- Quiz Evaluation
- Weak Area Detection
- Progress Dashboard
- Qdrant Vector Search
- LangGraph Multi-Agent Workflow

---

# Planned Improvements

- User Authentication
- Persistent Learning History
- Flashcard Generation
- Voice-based Tutor
- Learning Analytics
- Study Reminders
- Multi-language Support
- Cloud Deployment

---

# Author

**Raashi Singh**

B.Tech Computer Science and System Engineering

KIIT University

---

## License

This project is intended for educational and portfolio purposes.