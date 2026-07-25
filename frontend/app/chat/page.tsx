"use client";

import ChatWindow from "@/components/ChatWindow";

export default function ChatPage() {
  return (
    <div className="max-w-3xl mx-auto px-6 py-8">
      <h1 className="text-2xl font-semibold text-gray-900 mb-2">Chat with your tutor</h1>
      <p className="text-gray-500 mb-6 text-sm">
        Try: "make me a study plan", "explain photosynthesis", or "quiz me on chapter 2"
      </p>
      <ChatWindow userId="student1" />
    </div>
  );
}