import Link from "next/link";
import { Brain, Upload, Sparkles } from "lucide-react";

export default function Home() {
  return (
    <div className="max-w-4xl mx-auto px-6 py-24 text-center">
      <div className="inline-flex items-center gap-2 bg-indigo-50 text-indigo-600 px-4 py-1.5 rounded-full text-sm font-medium mb-6">
        <Sparkles size={14} />
        Agentic AI Tutor
      </div>

      <h1 className="text-5xl font-semibold text-gray-900 mb-4 leading-tight">
        Study smarter with <span className="text-indigo-600">AdaptIQ</span>
      </h1>

      <p className="text-lg text-gray-500 mb-10 max-w-xl mx-auto">
        Upload your notes. Get a personalized study plan. Ask questions, take quizzes,
        and let AI track your weak spots — automatically.
      </p>

      <div className="flex gap-4 justify-center">
        <Link
          href="/upload"
          className="flex items-center gap-2 bg-indigo-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-indigo-700 transition"
        >
          <Upload size={18} />
          Get started
        </Link>
        <Link
          href="/chat"
          className="flex items-center gap-2 bg-white border border-gray-300 text-gray-700 px-6 py-3 rounded-lg font-medium hover:bg-gray-50 transition"
        >
          <Brain size={18} />
          Try the tutor
        </Link>
      </div>

      <div className="grid grid-cols-3 gap-6 mt-20 text-left">
        {[
          { title: "Multi-agent system", desc: "Planner, Tutor, Assessor, and Evaluator agents work together to guide your learning." },
          { title: "RAG-powered answers", desc: "Every explanation is grounded in your actual study material — not generic AI knowledge." },
          { title: "Adaptive quizzes", desc: "Quizzes adjust based on your weak areas, tracked automatically over time." },
        ].map((f) => (
          <div key={f.title} className="bg-white border border-gray-200 rounded-xl p-6">
            <h3 className="font-medium text-gray-900 mb-2">{f.title}</h3>
            <p className="text-sm text-gray-500">{f.desc}</p>
          </div>
        ))}
      </div>
    </div>
  );
}