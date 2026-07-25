import axios from "axios";

const API_BASE = "http://127.0.0.1:8000/api";

export const api = axios.create({
  baseURL: API_BASE,
});

export interface ChatResponse {
  response: string;
  quiz_in_progress: boolean;
  quiz_score: number | null;
  weak_areas: string[];
  current_topic: string | null;
}

export async function sendMessage(userId: string, message: string): Promise<ChatResponse> {
  const res = await api.post("/chat/message", { user_id: userId, message });
  return res.data;
}

export async function uploadFile(file: File, userId: string) {
  const formData = new FormData();
  formData.append("file", file);
  const res = await api.post(`/upload/?user_id=${userId}`, formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return res.data;
}

export async function getUploadStatus(filename: string) {
  const res = await api.get(`/upload/status/${filename}`);
  return res.data;
}

export async function getProgress(userId: string) {
  const res = await api.get(`/progress/${userId}`);
  return res.data;
}

export async function getSession(userId: string) {
  const res = await api.get(`/chat/session/${userId}`);
  return res.data;
}