"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Brain, Upload, MessageSquare, BarChart3 } from "lucide-react";

export default function Navbar() {
  const pathname = usePathname();

  const links = [
    { href: "/", label: "Home", icon: Brain },
    { href: "/upload", label: "Upload", icon: Upload },
    { href: "/chat", label: "Tutor", icon: MessageSquare },
    { href: "/dashboard", label: "Progress", icon: BarChart3 },
  ];

  return (
    <nav className="border-b border-gray-200 bg-white sticky top-0 z-50">
      <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-2 font-semibold text-lg text-indigo-600">
          <Brain size={24} />
          AdaptIQ
        </Link>
        <div className="flex gap-1">
          {links.map(({ href, label, icon: Icon }) => (
            <Link
              key={href}
              href={href}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition ${
                pathname === href
                  ? "bg-indigo-50 text-indigo-600"
                  : "text-gray-600 hover:bg-gray-50"
              }`}
            >
              <Icon size={16} />
              {label}
            </Link>
          ))}
        </div>
      </div>
    </nav>
  );
}