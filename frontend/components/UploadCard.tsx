"use client";

import { useState, useCallback } from "react";
import { uploadFile, getUploadStatus } from "@/lib/api";
import {
  UploadCloud,
  FileText,
  CheckCircle2,
  Loader2,
} from "lucide-react";

interface UploadedDoc {
  filename: string;
  status: string;
}

export default function UploadCard({ userId }: { userId: string }) {
  const [dragging, setDragging] = useState(false);
  const [docs, setDocs] = useState<UploadedDoc[]>([]);

  const handleFile = useCallback(
    async (file: File) => {
      const result = await uploadFile(file, userId);

      const newDoc: UploadedDoc = {
        filename: result.filename,
        status: "processing",
      };

      // Prevent duplicate entries
      setDocs((prev) => {
        const exists = prev.some(
          (doc) => doc.filename === newDoc.filename
        );

        if (exists) {
          return prev.map((doc) =>
            doc.filename === newDoc.filename ? newDoc : doc
          );
        }

        return [...prev, newDoc];
      });

      const poll = setInterval(async () => {
        const statusRes = await getUploadStatus(result.filename);

        if (statusRes.status.startsWith("done")) {
          setDocs((prev) =>
            prev.map((d) =>
              d.filename === result.filename
                ? { ...d, status: "ready" }
                : d
            )
          );
          clearInterval(poll);
        } else if (statusRes.status.startsWith("error")) {
          setDocs((prev) =>
            prev.map((d) =>
              d.filename === result.filename
                ? { ...d, status: "error" }
                : d
            )
          );
          clearInterval(poll);
        }
      }, 2000);
    },
    [userId]
  );

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDragging(false);

    const file = e.dataTransfer.files[0];

    if (file) {
      handleFile(file);
    }
  };

  const handleSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];

    if (file) {
      handleFile(file);
    }

    // Allow selecting the same file again
    e.target.value = "";
  };

  return (
    <div className="space-y-4">
      <div
        onDragOver={(e) => {
          e.preventDefault();
          setDragging(true);
        }}
        onDragLeave={() => setDragging(false)}
        onDrop={handleDrop}
        className={`border-2 border-dashed rounded-xl p-10 text-center transition cursor-pointer ${
          dragging
            ? "border-indigo-500 bg-indigo-50"
            : "border-gray-300 bg-gray-50"
        }`}
        onClick={() => document.getElementById("file-input")?.click()}
      >
        <UploadCloud
          className="mx-auto mb-3 text-indigo-500"
          size={36}
        />

        <p className="text-gray-700 font-medium">
          Drag & drop your study material here
        </p>

        <p className="text-gray-400 text-sm mt-1">
          PDF, DOCX, or TXT — or click to browse
        </p>

        <input
          id="file-input"
          type="file"
          accept=".pdf,.docx,.txt"
          className="hidden"
          onChange={handleSelect}
        />
      </div>

      {docs.length > 0 && (
        <div className="space-y-2">
          {docs.map((doc, index) => (
            <div
              key={`${doc.filename}-${index}`}
              className="flex items-center justify-between bg-white border border-gray-200 rounded-lg px-4 py-3"
            >
              <div className="flex items-center gap-3">
                <FileText
                  size={18}
                  className="text-indigo-500"
                />

                <span className="text-sm text-gray-700">
                  {doc.filename}
                </span>
              </div>

              {doc.status === "processing" && (
                <span className="flex items-center gap-1 text-amber-600 text-xs">
                  <Loader2
                    size={14}
                    className="animate-spin"
                  />
                  Processing
                </span>
              )}

              {doc.status === "ready" && (
                <span className="flex items-center gap-1 text-green-600 text-xs">
                  <CheckCircle2 size={14} />
                  Ready
                </span>
              )}

              {doc.status === "error" && (
                <span className="text-red-500 text-xs">
                  Failed
                </span>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}