"use client";

import { useEffect, useState } from "react";
import { getProgress, getSession } from "@/lib/api";
import ProgressChart from "@/components/ProgressChart";
import { Flame, BookOpen, Target, AlertCircle } from "lucide-react";

export default function DashboardPage() {
  const [progress, setProgress] = useState<any>(null);
  const [session, setSession] = useState<any>(null);

  useEffect(() => {
    getProgress("student1").then(setProgress);
    getSession("student1").then(setSession);
  }, []);

  if (!progress) {
    return <div className="text-center py-20 text-gray-400">Loading your progress...</div>;
  }

  const stats = [
    { label: "Study streak", value: `${progress.streak_days || 0} days`, icon: Flame, color: "text-orange-500" },
    { label: "Topics covered", value: progress.topics_covered?.length || 0, icon: BookOpen, color: "text-indigo-500" },
    { label: "Total sessions", value: progress.total_sessions || 0, icon: Target, color: "text-green-500" },
    { label: "Weak areas", value: session?.weak_areas?.length || 0, icon: AlertCircle, color: "text-red-500" },
  ];

  return (
    <div className="max-w-5xl mx-auto px-6 py-12">
      <h1 className="text-2xl font-semibold text-gray-900 mb-8">Your progress</h1>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-10">
        {stats.map((s) => (
          <div key={s.label} className="bg-white border border-gray-200 rounded-xl p-5">
            <s.icon className={`${s.color} mb-2`} size={22} />
            <p className="text-2xl font-semibold text-gray-900">{s.value}</p>
            <p className="text-sm text-gray-500">{s.label}</p>
          </div>
        ))}
      </div>

      <div className="bg-white border border-gray-200 rounded-xl p-6 mb-8">
        <h2 className="font-medium text-gray-900 mb-4">Quiz performance</h2>
        <ProgressChart
          scores={(progress.quiz_scores || []).map((q: any) => ({ topic: q.topic, score: q.score }))}
        />
      </div>

      {session?.weak_areas?.length > 0 && (
        <div className="bg-amber-50 border border-amber-200 rounded-xl p-6">
          <h2 className="font-medium text-amber-900 mb-3 flex items-center gap-2">
            <AlertCircle size={18} /> Areas to review
          </h2>
          <ul className="space-y-2">
            {session.weak_areas.map((area: string, i: number) => (
              <li key={i} className="text-sm text-amber-800">• {area}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}