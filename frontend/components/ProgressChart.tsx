"use client";

import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
} from "recharts";

interface QuizScore {
  topic: string;
  score: number;
}

interface ProgressChartProps {
  scores: QuizScore[];
}

export default function ProgressChart({
  scores,
}: ProgressChartProps) {
  if (!scores || scores.length === 0) {
    return (
      <div className="flex items-center justify-center h-[320px] text-gray-400">
        No quiz data yet. Take a quiz to see your progress!
      </div>
    );
  }

  // Display Quiz 1, Quiz 2, Quiz 3...
  const chartData = scores.map((item, index) => ({
    quiz: `Quiz ${index + 1}`,
    score: item.score,
    topic: item.topic,
  }));

  return (
    <ResponsiveContainer width="100%" height={320}>
      <LineChart
        data={chartData}
        margin={{
          top: 20,
          right: 20,
          left: 10,
          bottom: 10,
        }}
      >
        <CartesianGrid
          strokeDasharray="3 3"
          stroke="#e5e7eb"
        />

        <XAxis
          dataKey="quiz"
          tick={{ fontSize: 12 }}
        />

        <YAxis
          domain={[0, 100]}
          ticks={[0, 20, 40, 60, 80, 100]}
          tick={{ fontSize: 12 }}
        />

        {/* Using the default tooltip to avoid TypeScript compatibility issues */}
        <Tooltip />

        <Line
          type="monotone"
          dataKey="score"
          stroke="#4f46e5"
          strokeWidth={3}
          dot={{
            r: 6,
            fill: "#4f46e5",
          }}
          activeDot={{
            r: 8,
          }}
        />
      </LineChart>
    </ResponsiveContainer>
  );
}