"use client";

import UploadCard from "@/components/UploadCard";

export default function UploadPage() {
  return (
    <div className="max-w-2xl mx-auto px-6 py-12">
      <h1 className="text-2xl font-semibold text-gray-900 mb-2">Upload your study material</h1>
      <p className="text-gray-500 mb-8">
        Upload your notes, textbook chapters, or syllabus. AdaptIQ will build a personalized
        study plan and answer questions based on this material.
      </p>
      <UploadCard userId="student1" />
    </div>
  );
}